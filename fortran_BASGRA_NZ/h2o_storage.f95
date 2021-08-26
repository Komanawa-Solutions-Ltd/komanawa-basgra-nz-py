module h2o_storage_system

    use parameters_site
    use environment

contains

    ! ##### input sub routines #####

    Subroutine storage_runoff()
        if (runoff_from_rain) then
            store_runoff_in = (RAIN / 1000) * (runoff_area * 10000) * runoff_frac
            h2o_store_vol = h2o_store_vol + store_runoff_in

        else
            store_runoff_in = external_inflow
            h2o_store_vol = h2o_store_vol + external_inflow
            h2o_store_vol = max(0.0, h2o_store_vol) ! prevent negative storage if external inflow is used to remove water
        end if
        if (h2o_store_vol > h2o_store_max_vol) then
            store_runoff_in = store_runoff_in - (h2o_store_vol - h2o_store_max_vol)
            h2o_store_vol = min(h2o_store_max_vol, h2o_store_vol)
        end if
    End Subroutine storage_runoff


    subroutine storage_refil_from_scheme(MAX_IRR, irrig_scheme)
        real :: MAX_IRR, irrig_scheme

        if ((MAX_IRR - irrig_scheme) >= stor_refill_min) then
            store_scheme_in = (MAX_IRR - irrig_scheme) / 1000 * (1 - stor_refill_losses) * (irrigated_area * 10000)
            store_scheme_in_loss = (MAX_IRR - irrig_scheme) / 1000 * (stor_refill_losses) * (irrigated_area * 10000)
            h2o_store_vol = h2o_store_vol + store_scheme_in
            if (h2o_store_vol > h2o_store_max_vol) then
                store_scheme_in_loss = store_scheme_in - (h2o_store_vol - h2o_store_max_vol)
                h2o_store_vol = min(h2o_store_max_vol, h2o_store_vol)
            end if
        else
            store_scheme_in = 0
            store_scheme_in_loss = 0
        endif

    end subroutine storage_refil_from_scheme

    subroutine storage_full_refil(doy)
        integer :: doy
        if (doy == stor_full_refil_doy) then
            h2o_store_vol = h2o_store_max_vol
        end if
    end subroutine storage_full_refil


    ! #####  out storage sub routines #####

    subroutine storage_evap()
        ! evaporation from the storage system
        store_evap_out = 0
        ! TODO This is a holder, storage evap is not implemented
    end subroutine storage_evap

    subroutine storage_loss_leakage()
        ! losses from storage time and condition invarient
        if (h2o_store_vol > stor_leakage) then
            store_leak_out = stor_leakage
            h2o_store_vol = h2o_store_vol - stor_leakage

        else
            store_leak_out = h2o_store_vol
            h2o_store_vol = 0
        end if
    end subroutine storage_loss_leakage

    subroutine irrigate_storage_usage(PAW, irr_trig, irr_targ, irrig_dem, INFILTOT, WAFC, WAWP, MXPAW, EVAP, TRAN, &
            WAL, irrigate, DRAIN, FREEZEL, RUNOFF, THAWS, doy, nirr, doy_irr, IRRIG, MAX_IRR, irrig_store, irrig_scheme)
        ! calculate the usage from storage

        integer :: doy, nirr
        integer, dimension(nirr) :: doy_irr
        real :: IRRIG
        real :: irrig_scheme, irrig_store
        real :: MAX_IRR, IRRIG_DEM

        real :: EVAP, TRAN, WAL, temp
        real :: DRAIN, FREEZEL, RUNOFF, THAWS
        real :: IRR_TRIG, IRR_TARG
        real :: INFILTOT, WAFC, WAWP, MXPAW, PAW
        logical :: irrigate
        real :: temp_stor_vol

        if (Irr_frm_PAW) then ! calculate irrigation demand and trigger from PAW
            irrigate = (PAW <= irr_trig * MXPAW)

            IRRIG_DEM = ((MXPAW * IRR_TARG + WAWP - WAL) / DELT - &
                    (INFILTOT - EVAP - TRAN - FREEZEL + THAWS - DRAIN - RUNOFF))  ! = mm d-1 Irrigation demand to IRR_TARG

        else ! calculate irrigation demand and trigger from field capacity
            irrigate = (((WAL + (INFILTOT - EVAP - TRAN - FREEZEL + THAWS - DRAIN - RUNOFF) * DELT) / WAFC) <= irr_trig)

            IRRIG_DEM = ((WAFC * IRR_TARG - WAL) / DELT - &
                    (INFILTOT - EVAP - TRAN - FREEZEL + THAWS - DRAIN - RUNOFF))  ! = mm d-1 Irrigation demand to IRR_TARG

        end if

        IRRIG_DEM = MAX(0., IRRIG_DEM) ! do not allow irrigation demand to become negative

        ! irrigate from scheme if irrigation is allowed
        if (any(doy==doy_irr)) then

            ! if after time step changes the fraction of water holding capcaity is below trigger then apply irrigation
            if (irrigate) then
                irrig_scheme = IRRIGF * IRRIG_DEM  ! = mm d-1 Irrigation
                irrig_scheme = min(irrig_scheme, MAX_IRR, abs_max_irr)
                irrig_scheme = max(irrig_scheme, 0.0)

            else
                irrig_scheme = 0.0
            end if

        else
            irrig_scheme = 0.0 ! if the day of year is not
        end if

        ! now calculate additional irigation from storage


        ! calculate further irrigation demand from storage
        if (calc_ind_store_demand) then
            if (Irr_frm_PAW) then ! calculate irrigation demand and trigger from PAW
                use_storage_today = (PAW + irrig_scheme <= irr_trig_store * MXPAW)

                temp = (INFILTOT - EVAP - TRAN - FREEZEL + THAWS + irrig_scheme - DRAIN - RUNOFF) * DELT
                irrig_dem_store = MXPAW * IRR_TARG_store + WAWP - (WAL + temp)  ! = mm d-1 Irrigation demand to IRR_TARG_store

            else ! calculate irrigation demand and trigger from field capacity
                temp = (INFILTOT - EVAP - TRAN - FREEZEL + THAWS + irrig_scheme - DRAIN - RUNOFF) * DELT
                use_storage_today = ((WAL + temp) / WAFC <= irr_trig_store)

                irrig_dem_store = WAFC * IRR_TARG_store - (WAL + temp) ! = mm d-1 Irrigation demand to IRR_TARG_store

            end if
        else ! the remainaing irrigation demand from scheme irrigation
            use_storage_today = irrigate
            irrig_dem_store = IRRIG_DEM - irrig_scheme
        end if

        irrig_dem_store = max(0.0, irrig_dem_store)

        if (irrig_scheme>=abs_max_irr) then
            irrig_store = 0.
            store_irr_loss = 0.
            use_storage_today = .FALSE.
        end if
        if (h2o_store_vol<=stor_reserve_vol) then
            use_storage_today = .FALSE.
        end if

        ! calculate the irrigation from storage)
        if (any(doy==doy_irr)) then
            ! if after time step changes the fraction of water holding capcaity is below trigger then apply irrigation
            if (use_storage_today) then
                irrig_store = IRRIGF * irrig_dem_store  ! = mm d-1 Irrigation

                irrig_store = min(irrig_store, abs_max_irr - irrig_scheme)
                irrig_store = max(0., irrig_store)
                temp_stor_vol = max(0., h2o_store_vol - stor_reserve_vol)

                if (temp_stor_vol / (1 + stor_irr_ineff) < (irrig_store / 1000) * (irrigated_area * 10000)) then ! not enough water

                    irrig_store = (temp_stor_vol * 1000 / (irrigated_area * 10000)) / (1 + stor_irr_ineff)
                    store_irr_loss = (irrig_store / 1000) * (irrigated_area * 10000) * stor_irr_ineff

                else ! enough water in storage
                    store_irr_loss = (irrig_store / 1000) * (irrigated_area * 10000) * (stor_irr_ineff)
                end if
                h2o_store_vol = h2o_store_vol - (irrig_store / 1000 * (irrigated_area * 10000)) - store_irr_loss

            else
                irrig_store = 0.
                store_irr_loss = 0.
            end if
        else
            irrig_store = 0. ! if the day of year is not
            store_irr_loss = 0.
            use_storage_today = .FALSE.
        end if

        IRRIG = irrig_scheme + irrig_store
    end subroutine irrigate_storage_usage

    ! ##### full storage routine #####
    Subroutine calc_storage_volume_use(doy, PAW, irr_trig, irr_targ, irrig_dem, INFILTOT, WAFC, WAWP, MXPAW, &
            EVAP, TRAN, &
            WAL, irrigate, DRAIN, FREEZEL, RUNOFF, THAWS, nirr, doy_irr, IRRIG, MAX_IRR, irrig_store, &
            irrig_scheme)
        integer :: doy
        integer :: nirr
        integer, dimension(nirr) :: doy_irr
        real :: IRRIG
        real :: MAX_IRR, IRRIG_DEM

        real :: EVAP, TRAN, WAL
        real :: DRAIN, FREEZEL, RUNOFF, THAWS
        real :: IRR_TRIG, IRR_TARG
        real :: irrig_store, irrig_scheme
        real :: INFILTOT, WAFC, WAWP, MXPAW, PAW
        logical :: irrigate



        ! storage in (non irrigation scheme)
        call storage_runoff()

        ! storage out (non irrigation scheme)
        call storage_evap() ! TODO this is a holder, storage evaporation is not implmeneted
        call storage_loss_leakage()

        ! storage and irrigation scheme interaction
        call irrigate_storage_usage(PAW, irr_trig, irr_targ, irrig_dem, INFILTOT, WAFC, WAWP, MXPAW, EVAP, TRAN, &
                WAL, irrigate, DRAIN, FREEZEL, RUNOFF, THAWS, doy, nirr, doy_irr, IRRIG, MAX_IRR, irrig_store, irrig_scheme)

        if(use_storage_today) then
            store_scheme_in = 0
            store_scheme_in_loss = 0
        else
            call storage_refil_from_scheme(MAX_IRR, irrig_scheme)
        end if
        call storage_full_refil(doy)
    End Subroutine calc_storage_volume_use

end module h2o_storage_system