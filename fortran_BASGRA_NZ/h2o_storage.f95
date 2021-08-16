module h2o_storage_system

    use parameters_site

contains

    ! ##### input sub routines #####

    Subroutine storage_runoff(RAIN)
        real  :: RAIN

        h2o_storage_vol = h2o_storage_vol + (RAIN / 1000) * (runoff_area * 10000) * runoff_frac

        if (h2o_storage_vol > h2o_store_max_vol) then
            h2o_storage_vol = h2o_store_max_vol
        end if
    End Subroutine storage_runoff


    subroutine storage_refil_from_scheme(MAX_IRR, irrig_scheme)
        real    :: MAX_IRR, irrig_scheme

        if ((MAX_IRR - irrig_scheme) >= stor_refill_min) then
            h2o_store_vol = h2o_store_vol + (MAX_IRR - irrig_scheme) / 1000 * stor_refill_losses * (irrigated_area * 10000)
        endif

    end subroutine storage_refil_from_scheme

    subroutine storage_full_refil(doy)
        integer  :: doy
        if (doy == stor_full_refil_doy) then
            h2o_store_vol = h2o_store_max_vol
        end if
    end subroutine storage_full_refil




    ! #####  out storage sub routines #####

    subroutine storage_evap()
        ! evaporation from the storage system
        ! TODO This is a holder, storage evap is not implemented
    end subroutine storage_evap

    subroutine storage_loss_leakage()
        ! losses from storage time and condition invarient
        h2o_storage_vol = h2o_storage_vol - stor_leakage
    end subroutine storage_loss_leakage

    subroutine irrigate_storage_usage(PAW, irr_trig, irr_targ, irrig_dem, INFILTOT, WAFC, WAWP, MXPAW, PAW, EVAP, TRAN, &
            WAL, irrigate, DRAIN, FREEZEL, RUNOFF, THAWS, doy, nirr, doy_irr, IRRIG, MAX_IRR, IRRIG_DEM, irrig_store, irrig_scheme)
        ! calculate the usage from storage ! todo
        integer :: doy, nirr
        integer, dimension(nirr)              :: doy_irr
        real :: IRRIG
        real :: irrig_scheme, irrig_store
        real :: MAX_IRR, IRRIG_DEM

        real :: EVAP, TRAN, WAL
        real :: DRAIN, FREEZEL, RUNOFF, THAWS
        real :: IRR_TRIG, IRR_TARG, IRRIG_DEM
        real :: INFILTOT, WAFC, WAWP, MXPAW, PAW
        logical :: irrigate
        real :: IRR_TRIG_store, IRR_TARG_store, irrig_dem_store

        if (Irr_frm_PAW) then ! calculate irrigation demand and trigger from PAW
            irrigate = (PAW <= irr_trig * MXPAW)

            IRRIG_DEM = ((MXPAW * IRR_TARG + WAWP - WAL) / DELT - &
                (INFILTOT - EVAP - TRAN - FREEZEL + THAWS - DRAIN - RUNOFF))  ! = mm d-1 Irrigation demand to IRR_TARG

        else ! calculate irrigation demand and trigger from field capacity
            irrigate = (((WAL + (INFILTOT - EVAP - TRAN - FREEZEL + THAWS - DRAIN - RUNOFF) * DELT) / WAFC) <= irr_trig)

            IRRIG_DEM = ((WAFC * IRR_TARG - WAL) / DELT - &
                (INFILTOT - EVAP - TRAN - FREEZEL + THAWS - DRAIN - RUNOFF))  ! = mm d-1 Irrigation demand to IRR_TARG

        end if

        IRRIG_DEM = MAX(0.,IRRIG_DEM) ! do not allow irrigation demand to become negative

        ! irrigate from scheme if irrigation is allowed
        if (any(doy==doy_irr)) then

            ! if after time step changes the fraction of water holding capcaity is below trigger then apply irrigation
            if (irrigate) then
                irrig_scheme = IRRIGF * IRRIG_DEM  ! = mm d-1 Irrigation
                irrig_scheme = min(irrig_scheme, MAX_IRR, abs_max_irr)
                irrig_scheme = max(irrig_scheme, 0)

            else
                irrig_scheme = 0
            end if

        else
            irrig_scheme = 0 ! if the day of year is not
        end if

        ! now calculate additional irigation from storage
        if (irrig_scheme<abs_max_irr) then

            ! calculate further irrigation demand from storage
            if (Irr_frm_PAW) then ! calculate irrigation demand and trigger from PAW
                use_storage_today = (PAW + irrig_scheme <= irr_trig_store * MXPAW)

                irrig_dem_store = ((MXPAW * IRR_TARG_store + WAWP - WAL) / DELT - &
                    (INFILTOT - EVAP - TRAN - FREEZEL + THAWS - DRAIN - RUNOFF + irrig_scheme))  ! = mm d-1 Irrigation demand to IRR_TARG

            else ! calculate irrigation demand and trigger from field capacity
                use_storage_today = (((WAL + (INFILTOT - EVAP - TRAN - FREEZEL + THAWS + irrig_scheme - DRAIN - RUNOFF) * DELT) / WAFC) <= irr_trig_store)

                irrig_dem_store = ((WAFC * IRR_TARG - WAL) / DELT - &
                    (INFILTOT - EVAP - TRAN - FREEZEL + THAWS - DRAIN - RUNOFF+ irrig_scheme))  ! = mm d-1 Irrigation demand to IRR_TARG


            end if
            if (h2o_store_vol<=0) then
                use_storage_today = .FALSE.
            end if

            irrig_dem_store = max(0, irrig_dem_store)

            ! calculate the irrigation from storage)
            if (any(doy==doy_irr)) then

            ! if after time step changes the fraction of water holding capcaity is below trigger then apply irrigation
                if (use_storage_today) then
                    irrig_store = IRRIGF * irrig_dem_store  ! = mm d-1 Irrigation

                    irrig_store = min(irrig_store, abs_max_irr-irrig_scheme)
                    irrig_store = max(0, irrig_store)

                    if (h2o_store_vol/(1+stor_irr_ineff) < (irrig_store/1000) * (irrigated_area * 10000)) then ! not enough water
                        irrig_store = (h2o_store_vol * 1000 / (irrigated_area * 10000))/(1+stor_irr_ineff)
                        h2o_store_vol = 0

                    else ! enough water in storage
                        h2o_store_vol = h2o_store_vol - (irrig_store/1000) * (irrigated_area * 10000) * (1 + stor_irr_ineff)
                    end if


                else
                    irrig_store = 0
                end if
            else
                irrig_store = 0 ! if the day of year is not
                use_storage_today = .FALSE.
            end if
        else
            use_storage_today = .FALSE.
        end if

        IRRIG = irrig_scheme + irrig_store
    end subroutine irrigate_storage_usage

    ! ##### full storage routine #####
    Subroutine calc_storage_volume_use(RAIN, doy, PAW, irr_trig, irr_targ, irrig_dem, INFILTOT, WAFC, WAWP, MXPAW, PAW, EVAP, TRAN, &
            WAL, irrigate, DRAIN, FREEZEL, RUNOFF, THAWS, doy, nirr, doy_irr, IRRIG, MAX_IRR, IRRIG_DEM, irrig_store, irrig_scheme)
        real  :: RAIN
        integer  :: doy
        integer :: nirr
        integer, dimension(nirr)              :: doy_irr
        real :: IRRIG
        real :: MAX_IRR, IRRIG_DEM

        real :: EVAP, TRAN, WAL
        real :: DRAIN, FREEZEL, RUNOFF, THAWS
        real :: IRR_TRIG, IRR_TARG, IRRIG_DEM
        real :: IRR_TRIG_store, IRR_TARG_store, irrig_dem_store, irrig_store, irrig_scheme! todo these are new varibles
        real :: INFILTOT, WAFC, WAWP, MXPAW, PAW
        logical :: irrigate



        ! storage in (non irrigation scheme)
        call storage_full_refil(doy)
        call storage_runoff(RAIN)

        ! storage out (non irrigation scheme)
        ! call storage_evap() ! TODO this is a holder, storage evaporation is not implmeneted
        call storage_loss_leakage()

        ! storage and irrigation scheme interaction
        call irrigate_storage_usage(PAW, irr_trig, irr_targ, irrig_dem, INFILTOT, WAFC, WAWP, MXPAW, PAW, EVAP, TRAN, &
            WAL, irrigate, DRAIN, FREEZEL, RUNOFF, THAWS, doy, nirr, doy_irr, IRRIG, MAX_IRR, IRRIG_DEM, irrig_store, irrig_scheme)

        if(.not. use_storage_today) then
            call storage_refil_from_scheme(MAX_IRR, irrig_scheme)
        end if
    End Subroutine calc_storage_volume_use

end module h2o_storage_system


! todo which variables to send to outputs