module soil

    use parameters_site
    use parameters_plant
    use h2o_storage_system

    implicit none

    ! Soil variables
    real :: FO2     ! = mol O2 mol-1 gas Soil oxygen as a fraction of total gas
    real :: fPerm   ! = not used
    real :: Tsurf   ! = soil surface temperature, and fPerm = not used
    real :: WCL     ! = Effective soil water content
    real :: WCLM    ! = Liquid soil water content between frost depth and root depth max

contains

    ! Calculate WCLM = Liquid soil water content between frost depth and root depth
    ! Calculate WCL  = Effective water content exerienced by plant
    Subroutine SoilWaterContent(Fdepth, ROOTD, WAL, WALS)
        real :: Fdepth, ROOTD, WAL, WALS
        if (Fdepth < ROOTD) then
            !    WCL = WAL * 0.001 / (ROOTD-Fdepth) ! Average volumetric moisture content in non-frozen root zone
            WCLM = WAL * 0.001 / (ROOTDM - Fdepth) ! Average volumetric moisture content in ROOTDM-Fdepth zone
            WCLM = max(WCLM, WCAD + (WCFC - WCAD) * WALS / 25.0)                  ! Simon WALS effect
            WCL = WCAD + (WCLM - WCAD) * ((ROOTD - Fdepth) / (ROOTDM - Fdepth))      ! Simon ROOTD effect
        else
            WCLM = 0
            WCL = 0
        end if
    end Subroutine SoilWaterContent

    ! Calculate Tsurf = soil surface temperature, and fPerm = not used
    ! See equations in Thorsen et al 2010
    Subroutine Physics(DAVTMP, Fdepth, ROOTD, Sdepth, WAS, Frate)
        real :: DAVTMP, Fdepth, ROOTD, Sdepth, WAS
        real :: Frate
        if (Fdepth > 0.) then
            Tsurf = DAVTMP / (1. + 10. * (Sdepth / Fdepth)) ! Temperature extinction under snow when soil is frozen (Eqn 15)
            fPerm = 0. ! Not used
        else
            Tsurf = DAVTMP * exp(-KTSNOW * Sdepth)             ! Temperature extinction under snow (Eqn 16, KTSNOW = gamma ~ 65 m-1)
            fPerm = 1. ! Not used
        end if
        call Frozensoil(Fdepth, ROOTD, WAS, Frate)
    end Subroutine Physics

    ! Calculate Frate = m d-1 Rate of increase of frost layer depth
    ! See equations in Thorsen et al Polar Research 29 2010 110�126
    Subroutine FrozenSoil(Fdepth, ROOTD, WAS, Frate)
        real :: Fdepth, ROOTD, WAS
        real :: Frate
        real :: alpha, PFrate, WCeff
        ! Determining the amount of water that contributes in transportation of heat to surface 'WCeff' (Xw)
        if (Fdepth > ROOTDM) then           ! Soil all frozen, Simon modified to ROOTDM, this line becomes redundant
            WCeff = WCFC
        else if (Fdepth > 0.) then          ! Soil partiatlly frozen
            WCeff = (0.001 * WAS) / Fdepth
        else                                ! Soil not frozen
            WCeff = WCLM
        end if
        ! Calculating potential frost rate 'PFrate'
        if (((Fdepth == 0.).and.(Tsurf>0.)).or.(WCeff == 0.)) then ! No soil frost present AND no frost starting
            PFrate = 0.
        else
            alpha = LAMBDAsoil / (RHOwater * WCeff * LatentHeat)      ! (see Eqn 11)
            PFrate = sqrt(max(0., Fdepth**2 - 2. * alpha * Tsurf)) - Fdepth ! (see Eqn 12)
        end if
        if ((PFrate >= 0.).and.(Fdepth > 0.).and.(Fdepth < ROOTDM)) then ! Simon modified to ROOTDM
            !       Frate = PFrate * (0.001*WAS/Fdepth) / WCFC ! Soil frost increasing
            Frate = PFrate * (0.001 * WAS / Fdepth) / WCLM   ! Soil frost increasing, Simon modified (looks strange)
        else if ((PFrate + Fdepth / DELT) < 0.) then
            Frate = -Fdepth / DELT                      ! Remaining soil frost thaws away
        else
            Frate = PFrate
        end if
    end Subroutine FrozenSoil

    subroutine irrigate_no_storage(PAW, irr_trig, irr_targ, irrig_dem, INFILTOT, WAFC, WAWP, MXPAW, EVAP, TRAN, &
            WAL, irrigate, DRAIN, FREEZEL, RUNOFF, THAWS, doy, nirr, doy_irr, IRRIG, MAX_IRR)
        integer :: doy, nirr
        integer, dimension(nirr)              :: doy_irr
        real :: IRRIG
        real :: MAX_IRR, IRRIG_DEM

        real :: EVAP, TRAN, WAL
        real :: DRAIN, FREEZEL, RUNOFF, THAWS
        real :: IRR_TRIG, IRR_TARG
        real :: INFILTOT, WAFC, WAWP, MXPAW, PAW
        logical :: irrigate

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

        ! irrigate if irrigation is allowed
        if (any(doy==doy_irr)) then

            ! if after time step changes the fraction of water holding capcaity is below trigger then apply irrigation
            if (irrigate) then
                IRRIG = IRRIGF * IRRIG_DEM  ! = mm d-1 Irrigation
                IRRIG = min(IRRIG, MAX_IRR, abs_max_irr)
                IRRIG = max(0.0, IRRIG)
            else
                IRRIG = 0.0
            end if

        else
            IRRIG = 0.0 ! if the day of year is not
        end if

        ! set storage values to 0
        store_runoff_in = 0.0
        store_leak_out = 0.0
        store_irr_loss = 0.0
        store_evap_out = 0.0
        store_scheme_in = 0.0
        store_scheme_in_loss = 0.0
    end subroutine irrigate_no_storage


    ! Calculate DRAIN,FREEZEL,IRRIG,RUNOFF,THAWS
    ! FIXME Why would ROOTD affect soil freezing? Uncouple Fdepth from ROOTD.
    Subroutine FRDRUNIR(EVAP, Fdepth, Frate, INFIL, poolDRAIN, ROOTD, TRAN, WAL, WAS, &
            DRAIN, FREEZEL, IRRIG, IRRIG_DEM, RUNOFF, THAWS, &
            MAX_IRR, doy, doy_irr, nirr, IRR_TRIG, IRR_TARG, WAFC, WAWP, MXPAW, PAW, &
            irrig_store, irrig_scheme)

        real :: irrig_store, irrig_scheme
        real :: EVAP, Fdepth, Frate, INFIL, poolDRAIN, ROOTD, TRAN, WAL, WAS
        real :: DRAIN, FREEZEL, IRRIG, RUNOFF, THAWS
        real :: MAX_IRR, IRR_TRIG, IRR_TARG, IRRIG_DEM
        integer :: doy, nirr
        integer, dimension(nirr)              :: doy_irr
        real :: INFILTOT, WAFC, WAST, WAWP, MXPAW, PAW
        logical :: irrigate

        WAFC = 1000. * WCFC * max(0., (ROOTDM - Fdepth))                      ! (mm) Field capacity, Simon modified to ROOTDM
        WAST = 1000. * WCST * max(0., (ROOTDM - Fdepth))                      ! (mm) Saturation, Simon modified to ROOTDM
        WAWP = 1000. * WCWP * max(0., (ROOTDM - Fdepth))                      ! (mm) Saturation, Simon modified to ROOTDM
        MXPAW = WAFC-WAWP

        INFILTOT = INFIL + poolDrain
        if (Fdepth < ROOTDM) then                                            ! Simon modified to ROOTDM
            FREEZEL = max(0., min(WAL / DELT + (INFILTOT - EVAP - TRAN), &
                    (Frate / (ROOTDM - Fdepth)) * WAL))                  ! = mm d-1 Freezing of soil water
        else
            FREEZEL = 0.
        end if
        if ((Fdepth > 0.) .and. (Fdepth <= ROOTDM)) then                     ! Simon modified to ROOTDM
            THAWS = max(0., min(WAS / DELT, -Frate * WAS / Fdepth))               ! = mm d-1 Thawing of soil frost
        else
            THAWS = 0.
        end if
        DRAIN = max(0., min(DRATE, (WAL - WAFC) / DELT + &
                (INFILTOT - EVAP - TRAN - FREEZEL + THAWS)))                 ! = mm d-1 Drainage, drains to WAFC (max 50 mm d-1)
        RUNOFF = max(0., (WAL - WAST) / DELT + &
                (INFILTOT - EVAP - TRAN - FREEZEL + THAWS - DRAIN))          ! = mm d-1 Runoff, runs off to WAST !todo why is this always zero

        if (pass_soil_moist) then ! no soil moisture calculated here instead use user passed soil moisture
            PAW = WAL - WAWP
        else
            PAW = max(0., ((WAL + (INFILTOT - EVAP - TRAN - FREEZEL + THAWS - DRAIN - RUNOFF) * DELT) - WAWP))
        end if

        if (use_storage) then
            call calc_storage_volume_use (doy, PAW, irr_trig, irr_targ, irrig_dem, INFILTOT, WAFC, WAWP, MXPAW, EVAP, TRAN, &
            WAL, irrigate, DRAIN, FREEZEL, RUNOFF, THAWS, nirr, doy_irr, IRRIG, MAX_IRR, irrig_store, irrig_scheme)
        else
            call irrigate_no_storage(PAW, irr_trig, irr_targ, irrig_dem, INFILTOT, WAFC, WAWP, MXPAW, EVAP, TRAN, &
            WAL, irrigate, DRAIN, FREEZEL, RUNOFF, THAWS, doy, nirr, doy_irr, IRRIG, MAX_IRR)
            irrig_store = 0
            irrig_dem_store = 0
            irrig_scheme = IRRIG
        end if

    end Subroutine FRDRUNIR

    ! Calculate FO2 = mol O2 mol-1 gas	Soil oxygen as a fraction of total gas
    Subroutine O2status(O2, ROOTD)
        real :: O2, ROOTD
        FO2 = O2 / (ROOTDM * FGAS * 1000. / 22.4) ! FGAS is a parameter, Simon modified to ROOTDM
    end Subroutine O2status

    Subroutine O2fluxes(O2, PERMgas, ROOTD, RplantAer, O2IN, O2OUT)
        real :: O2, PERMgas, ROOTD, RplantAer
        real :: O2IN, O2OUT
        real :: O2MX
        O2OUT = RplantAer * KRTOTAER * 1. / 12. * 1.
        O2MX = FO2MX * ROOTDM * FGAS * 1000. / 22.4                           ! Simon modified to ROOTDM
        O2IN = PERMgas * ((O2MX - O2) + O2OUT * DELT)
    end Subroutine O2fluxes

end module soil
