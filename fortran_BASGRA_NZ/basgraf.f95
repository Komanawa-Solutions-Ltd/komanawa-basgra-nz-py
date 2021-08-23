module basgramodule
    use, intrinsic :: iso_c_binding

    implicit none
    private
    public :: BASGRA

contains

subroutine BASGRA(PARAMS,MATRIX_WEATHER,DAYS_HARVEST,NDAYS,NOUT,nirr, doy_irr,y,VERBOSE) bind(C, name = "BASGRA_")
!-------------------------------------------------------------------------------
! This is the BASic GRAss model originally written in MATLAB/Simulink by Marcel
! van Oijen, Mats Hoglind, Stig Morten Thorsen and Ad Schapendonk.
! 2011-07-13: Translation to FORTRAN by David Cameron and Marcel van Oijen.
! 2014-03-17: Extra category of tillers added
! 2014-04-03: Vernalization added
! 2014-04-03: Lower limit of temperature-driven leaf senescence no longer zero
! 2018-08-01: Modified by Simon Woodward for New Zealand ryegrass simulations
! 2019-06-09: Added C wrapper to allow model to be compiled into an R package
! 2020-08-19: Modified by Matt Hanson to allow python use, added documentation, set maximum weather size to 36600
!             and unlimited harvest dates.
! 2021-01-19: Modified by Matt Hanson to include multiple additional features, see github repo for details
!             https://github.com/Komanawa-Solutions-Ltd/BASGRA_NZ_PY
!-------------------------------------------------------------------------------
!INPUTS
  !PARAMS: double, set of model parameters for details and order please see ./input_paramaters_decriptors.csv
  !MATRIX_WEATHER: double, weather matrix with two formats:
  !  1) internal calculation of PET size = (36,600 x 11) NDAYS rows must have valid data, null values set to 0
  !     Columns:
  !                  year  # day of the year (d)
  !                  doy   # day of the year (d)
  !                  rain  # precipitation (mm d-1)
  !                  radn    # irradiation (MJ m-2 d-1)
  !                  tmax  # minimum (or average) temperature (degrees Celsius)
  !                  tmin  # maximum (or average) temperature (degrees Celsius)
  !                  vpa    # vapour pressure (kPa)
  !                  wind    # mean wind speed at 2m (m s-1)
  !                  max_irr  # maximum irrigation available (mm)
  !                  irr_trig  # fraction of PAW/field (see irr_frm_paw) at or below which irrigation is
  !                              triggered e.g. 0.5 means that irrigation will only be applied when soil water
  !                              content is at 1/2 of the appropriate variable (fraction)
  !                  irr_targ  # fraction of PAW/field (see param irr_frm_paw) to irrigate up to (fraction)


  !  2) external calculations/measurment of PET size = (36,600 x 10)NDAYS rows with null values set to 0
  !     Columns:
  !              year,  # e.g. 2002
  !              doy,  # day of year 1 - 356 or 366 for leap years
  !              radn,  # daily solar radiation (MJ/m2)
  !              tmin,  # daily min (degrees C)
  !              tmax,  # daily max (degrees C)
  !              rain,  # sum daily rainfall (mm)
  !              pet,  # Potential evapotransperation (mm)
  !              max_irr  # maximum irrigation available (mm)
  !              irr_trig  # fraction of PAW/field (see irr_frm_paw) at or below which irrigation is
  !                          triggered e.g. 0.5 means that irrigation will only be applied when soil water
  !                          content is at 1/2 of the appropriate variable (fraction)
  !              irr_targ  # fraction of PAW/field (see param irr_frm_paw) to irrigate up to (fraction)

  !  switching between modes requires different compiliations, to set to mode 2, -Dweathergen, must be called while
  !  compiling (e.g.gfortran -x f95-cpp-input -Dweathergen -O3 -c -fdefault-real-8 ....)

  !DAYS_HARVEST: double, The harvest dates, size is (NDHARV,8) the columns are:
  !           'year', # year e.g. 2002
  !           'doy', # day of year 1 - 356 (366 for leap year)
  !           'frac_harv', # fraction (0-1) of material above target to harvest to maintain 'backward capabilities'
  !                        with v2.0.0 (fraction)
  !           'harv_trig', # dm above which to initiate harvest if trigger is less than zero
  !                        no harvest will take place (kgDM/ha)
  !           'harv_targ', # dm to harvest to or to remove depending on 'fixed_removal' (kgDM/ha)
  !           'weed_dm_frac', # fraction of dm of ryegrass to attribute to weeds (fraction)
  !           'reseed_trig',  # when BASAL <= reseed_trig trigger a reseeding. if <0 then do not reseed (fraction)
  !           'reseed_basal', # set BASAL = reseed_basal when reseeding. (fraction)

  !NDAYS: int, the number of days to simulate, this should match the number of days of real data in MATRIX_WEATHER
  !NOUT: int, the number of output variables, at present this should be 72
  !NIIR: int, the length of the DOY_IRR array
  !DOY_IRR: int, array of the days of the year on which to irrigate (0 (no irrigation) to 366 (leap year))
  !y: double, the output array, initialised as zeros
  !VERBOSE: boolean, if True print a number of debugging information

 !-------------------------------------------------------------------------------
! Allows access to all public objects in the other modules
use parameters_site
use parameters_plant
use environment
use resources
use soil
use plant

implicit none

! Define model inputs

logical(kind = c_bool), intent(in)           :: VERBOSE
integer(kind = c_int), intent(in)            :: NDAYS
integer(kind = c_int), intent(in)            :: NOUT
integer(kind = c_int), intent(in)            :: nirr
integer, parameter ::  NHARVCOL = 8 ! here so that I don't have to keep updating in harvest as well
real(kind = c_double), intent(in), dimension(NDAYS,NHARVCOL) :: DAYS_HARVEST

! BASGRA handles two types of weather files with different data columns
#ifdef weathergen
  integer, parameter                                :: NWEATHER =  13
#else
  integer, parameter                                :: NWEATHER =  14
#endif
real(kind = c_double), intent(in), dimension(NPAR)              :: PARAMS ! NPAR set in parameters_site.f90
integer(kind = c_int), intent(in), dimension(nirr)              :: doy_irr
real(kind = c_double), intent(in), dimension(NMAXDAYS,NWEATHER) :: MATRIX_WEATHER
real(kind = c_double), intent(out), dimension(NDAYS,NOUT)       :: y

! Define time variables
integer               :: day, doy, i, year

! Define state variables
real :: CLV, CLVD, YIELD, YIELD_RYE, YIELD_WEED, CRES, CRT, CST, CSTUB, DRYSTOR, Fdepth, LAI, LT50, O2, PHEN, AGE
real :: ROOTD, Sdepth, TILG1, TILG2, TILV, TANAER, WAL, WAPL, WAPS, WAS, WETSTOR, WAFC, WAWP, MXPAW, PAW
!integer :: VERN
real :: VERN                                  ! Simon made VERN a continuous function of VERND
real :: VERND, DVERND, WALS, BASAL

! Define intermediate and rate variables
real :: DeHardRate, DLAI, DLV, DLVD, DPHEN, DRAIN, DRT, DSTUB, dTANAER, DTILV, EVAP, EXPLOR
real :: Frate, FREEZEL, FREEZEPL, GLAI, GLV, GPHEN, GRES, GRT, GST, GSTUB, GTILV, HardRate
real :: HARVFR, HARVFRIN, HARVLA, HARVLV, HARVLVD, HARVPH, HARVRE, HARVST, HARVTILG2, INFIL, IRRIG, IRRIG_DEM, O2IN
real :: WEED_HARV_FR, DM_RYE_RM, DM_WEED_RM, DMH_RYE, DMH_WEED
real :: O2OUT, PackMelt, poolDrain, poolInfil, Psnow, reFreeze, RGRTV, RDRHARV
real :: RGRTVG1, RROOTD, RUNOFF, SnowMelt, THAWPS, THAWS, TILVG1, TILG1G2, TRAN, Wremain, SP
integer :: HARV

real :: irrig_dem_store, irrig_store, irrig_scheme!
! Extra output variables (Simon)
real :: Time, DM, RES, SLA, TILTOT, FRTILG, FRTILG1, FRTILG2, LINT, DEBUG, TSIZE, RESEEDED


  ! set inital values for storage outputs/ state variables

  store_runoff_in = 0
  store_leak_out = 0
  store_irr_loss = 0
  store_evap_out = 0
  store_scheme_in = 0
  store_scheme_in_loss = 0

! Extract calendar and weather data
YEARI  = MATRIX_WEATHER(:,1)
DOYI   = MATRIX_WEATHER(:,2)
GRI    = MATRIX_WEATHER(:,3)
TMMNI  = MATRIX_WEATHER(:,4)
TMMXI  = MATRIX_WEATHER(:,5)
#ifdef weathergen
  RAINI = MATRIX_WEATHER(:,6)
  PETI  = MATRIX_WEATHER(:,7)
  MAX_IRRI = MATRIX_WEATHER(:,8)
  IRR_TRIGI = MATRIX_WEATHER(:,9)
  IRR_TARGI = MATRIX_WEATHER(:,10)
  IRR_TRIG_storeI = MATRIX_WEATHER(:,11)
  IRR_TARG_storeI = MATRIX_WEATHER(:,12)
  external_inflowI = MATRIX_WEATHER(:,13)

#else
  VPI   = MATRIX_WEATHER(:,6)
  RAINI = MATRIX_WEATHER(:,7)
  WNI   = MATRIX_WEATHER(:,8)
  MAX_IRRI = MATRIX_WEATHER(:,9)
  IRR_TRIGI = MATRIX_WEATHER(:,10)
  IRR_TARGI = MATRIX_WEATHER(:,11)
  IRR_TRIG_storeI = MATRIX_WEATHER(:,12)
  IRR_TARG_storeI = MATRIX_WEATHER(:,13)
  external_inflowI = MATRIX_WEATHER(:,14)
#endif

! Extract parameters
call set_params(PARAMS)

! Initial value transformations, Simon moved to here
CLVI  = 10**LOG10CLVI
!CLVDI =
!CRESI = 10**LOG10CRESI
CRTI  = 10**LOG10CRTI
!LAII  = 10**LOG10LAII

! Soil water parameter scaling, Simon moved to here
WCAD  = FWCAD  * WCST
WCWP  = FWCWP  * WCST
WCFC  = FWCFC  * WCST
WCWET = FWCWET * WCST

! Initialise state variables
AGE     = 0.0
CLV     = CLVI
CLVD    = CLVI * 0.2                             ! Simon initially set equal to leaf mass * 0.2
CRES    = (FCOCRESMN*0.5+0.5) * COCRESMX * (CLVI + CSTI)   ! Simon start at av
CRT     = CRTI
CST     = CSTI
CSTUB   = CSTUBI                                 ! Currently constant 0
DAYL    = 0.5                                    ! Simon used to initialise YDAYL
DRYSTOR = DRYSTORI
Fdepth  = FdepthI
LAI     = (FSLAMIN*0.5+0.5) * SLAMAX * CLV       ! Simon start at av, LAI is defined over entire area
LT50    = LT50I
O2      = FGAS * ROOTDM * FO2MX * 1000./22.4
PHEN    = PHENI
Sdepth  = SDEPTHI
TANAER  = TANAERI
TILG1   = TILTOTI *       FRTILGI *    FRTILGG1I
TILG2   = TILTOTI *       FRTILGI * (1-FRTILGG1I)
TILV    = TILTOTI * (1. - FRTILGI)
BASAL   = BASALI
ROOTD   = ROOTDM * CRT/BASAL / (CRT/BASAL + KCRT)! Simon tied ROOTD to CRT like this, CRT is defined over entire area
!VERN    = 0.0
!VERND   = floor(VERNDI)                           ! Simon initialise count of cold days
!  if ((VERN==0).and.(VERND .ge. TVERND)) then ! copied from Vernalisation()
!	VERN = 1.0
! 	VERND = 0.0
!    DVERND = 0.0
!  end if
VERND   = VERNDI
VERN    = max(0.0, min(1.0, (VERND-TVERNDMN)/(TVERND-TVERNDMN))) ! FIXME does not include effect of new summer tillers
YIELD_RYE   = YIELDI ! currently hard coded to zero
YIELD_WEED   = YIELDI ! currently hard coded to zero
YIELD   = YIELD_RYE + YIELD_WEED
if (pass_soil_moist) then
    WAFC = 1000. * WCFC * max(0., (ROOTDM - Fdepth))                      ! (mm) Field capacity, Simon modified to ROOTDM
    WAWP = 1000. * WCWP * max(0., (ROOTDM - Fdepth))                      ! (mm) wilting point Simon modified to ROOTDM
    MXPAW = WAFC-WAWP
  if (Irr_frm_PAW) then
    WAL     = (MAX_IRRI(1) * MXPAW) + WAWP
  else
     WAL  =  MAX_IRRI(1) * WAFC
  end if
  WALS    = 0
  WAPL    = 0
  WAPS    = 0
  WAS     = 0
  WETSTOR = 0

else
  WAL     = 1000. * (ROOTDM - Fdepth) * WCFC        ! Simon set to WCFC
  WALS    = min(WAL, 25.0)                          ! Simon added WALS rapid surface layer (see manual section 4.3)
  WAPL    = WAPLI
  WAPS    = WAPSI
  WAS     = WASI
  WETSTOR = WETSTORI
end if


! Loop through days
do day = 1, NDAYS

  ! Calculate intermediate and rate variables (many variable and parameters are passed implicitly)
  !    SUBROUTINE      INPUTS                          OUTPUTS

  call set_weather_day(day,DRYSTOR, year,doy, NDAYS) ! set weather for the day, including DTR, PAR, which depend on DRYSTOR

  call Reseed(day, NDAYS, NHARVCOL, DAYS_HARVEST, BASAL, LAI, PHEN, TILG1, TILG2, TILV, & ! inputs
                    CLV, CRES, CST, CSTUB, &
                    RESEEDED)
  call Harvest (day, NDAYS, NHARVCOL, BASAL, CLV,CRES,CST,CSTUB,CLVD,DAYS_HARVEST,LAI,PHEN,TILG2,TILG1,TILV, &
                GSTUB,HARVLA,HARVLV,HARVLVD,HARVPH,HARVRE,HARVST, &
                HARVTILG2,HARVFR,HARVFRIN,HARV,RDRHARV, &
                WEED_HARV_FR, DM_RYE_RM, DM_WEED_RM, DMH_RYE, DMH_WEED)


  LAI     = LAI     - HARVLA * (1 + RDRHARV)
  CLV     = CLV     - HARVLV * (1 + RDRHARV)
  CLVD    = CLVD    - HARVLVD     + (HARVLV + HARVRE) * RDRHARV
  CRES    = CRES    - HARVRE * (1 + RDRHARV)
  CST     = CST     - HARVST   - GSTUB
  CSTUB   = CSTUB              + GSTUB
  TILV    = TILV    - TILV * RDRHARV
  TILG1   = TILG1   - TILG1 * RDRHARV
  TILG2   = TILG2   - HARVTILG2
  if (TILG2 < 1.0) then
	TILG2 = 0.0                              ! Simon avoid roundoff error in TILG2
  end if
  TILTOT  = TILG1 + TILG2 + TILV
  PHEN    = PHEN    - HARVPH
  if (doy.eq.152) then                               ! Reset yield on 1 June
      YIELD = 0.0
      YIELD_RYE = 0.0
      YIELD_WEED = 0.0
  end if
  YIELD_RYE     = YIELD_RYE + ((HARVLV + HARVLVD + HARVST) / 0.45 + HARVRE / 0.40) * 10.0 / 1000.0 ! tDM ha-1 Simon cumulative harvest
  YIELD_WEED = YIELD_WEED + (((HARVLV + HARVLVD + HARVST) / 0.45 + HARVRE / 0.40) * 10.0 / 1000.0)* WEED_HARV_FR
  YIELD = YIELD_RYE + YIELD_WEED
  call SoilWaterContent(Fdepth,ROOTD,WAL,WALS)                   ! calculate WCL
  call Physics        (DAVTMP,Fdepth,ROOTD,Sdepth,WAS, Frate)    ! calculate Tsurf, Frate
  call MicroClimate   (doy,DRYSTOR,Fdepth,Frate,LAI,BASAL,Sdepth,Tsurf,WAPL,WAPS,WETSTOR, &
                                                       FREEZEPL,INFIL,PackMelt,poolDrain,poolInfil, &
                                                       pSnow,reFreeze,SnowMelt,THAWPS,wRemain) ! calculate water, snow and ice
  call DDAYL          (doy)                                      ! calculate DAYL, DAYLMX
#ifdef weathergen
  call PEVAPINPUT     (LAI,BASAL)                                      ! calculate PEVAP, PTRAN, depend on LAY, RNINTC
#else
  call PENMAN         (LAI,BASAL)                                      ! calculate PEVAP, PTRAN, depend on LAY, RNINTC
#endif

  call Light          (DAYL,DTR,LAI,BASAL,PAR)                   ! calculate light interception DTRINT,PARINT,PARAV
  call EVAPTRTRF      (Fdepth,PEVAP,PTRAN,CRT,ROOTD,WAL,WCLM,WCL,EVAP,TRAN)! calculate EVAP,TRAN,TRANRF


  call FRDRUNIR       (EVAP,Fdepth,Frate,INFIL,poolDRAIN,ROOTD,TRAN,WAL,WAS, &
                                                         DRAIN,FREEZEL,IRRIG, IRRIG_DEM, RUNOFF,THAWS, &
                         MAX_IRR, doy, doy_irr, nirr, IRR_TRIG, IRR_TARG, &
                         WAFC, WAWP, MXPAW, PAW, &
                         IRR_TRIG_store, IRR_TARG_store, irrig_dem_store, irrig_store, irrig_scheme &
                      ) ! calculate water movement etc DRAIN,FREEZEL,IRRIG,RUNOFF,THAWS

  call O2status       (O2,ROOTD)                                 ! calculate FO2

  call Vernalisation  (DAYL,PHEN,YDAYL,TMMN,TMMX,DAVTMP,Tsurf,VERN,VERND,DVERND) ! Simon calculate VERN,VERND,DVERND
  call Phenology      (DAYL,TILG2,PHEN,         DPHEN,GPHEN,HARVPH) ! calculate GPHEN, DPHEN, PHENRF, DAYLGE
  call Biomass        (AGE,CLV,CRES,CST,CSTUB)                   ! calculate RESNOR
  call CalcSLA                                                   ! calculate LERV,LERG,SLANEW
  call LUECO2TM       (PARAV,BASAL)                              ! calculate LUEMXQ
  call HardeningSink  (CLV,DAYL,doy,LT50,Tsurf)                  ! calculate RESPHARDSI
  call Growth         (CLV,CRES,CST,PARINT,TILG2,TILG1,TILV,TRANRF,AGE,LAI, GLV,GRES,GRT,GST) ! calculate assimilate partitioning
  call PlantRespiration(FO2,RESPHARD)                            ! calculate RplantAer
  call Senescence     (CLV,CRT,CSTUB,doy,LAI,PARBASE,BASAL,LT50,PERMgas,TRANRF,TANAER,TILV,Tsurf,AGE, &
                                                       DeHardRate,DLAI,DLV,DRT,DSTUB,dTANAER,DTILV,HardRate,RDRS,RDRW)
  call Decomposition  (CLVD,DAVTMP,WCLM,                DLVD,RDLVD)    ! Simon decomposition function
  call Tillering      (DAYL,GLV,LAI,BASAL,TILV,TILG1,TRANRF,Tsurf,VERN,AGE, &
                                                       GLAI,RGRTV,GTILV,TILVG1,TILG1G2)

  call ROOTDG         (Fdepth,ROOTD,WAL,WCL,CRT,GRT,DRT, EXPLOR,RROOTD)! calculate root depth increase rate RROOTD,EXPLOR
  call O2fluxes       (O2,PERMgas,ROOTD,RplantAer,     O2IN,O2OUT)


  !================
  ! Outputs
  !================

! structural carbohydrate is 45% carbon C6H12O5
! soluble carbohydrate is 40% carbon C6H12O6

  Time      = year + (doy-0.5)/366 ! "Time" = Decimal year (approximation)
  DM        = ((CLV+CST+CSTUB)/0.45 + CRES/0.40 + CLVD/0.45) * 10.0 ! "DM"  = Aboveground dry matter in kgDM ha-1 (Simon included CLVD, changed units)
  RES       = (CRES/0.40) / ((CLV+CST+CSTUB)/0.45 + CRES/0.40)      ! "RES" = Reserves in gDM gDM-1 aboveground green matter
  SLA       = LAI / CLV                          ! SLA     = m2 leaf area gC-1 dry matter vegetative tillers (Note units and RES not included)
  TSIZE     = (CLV+CST) / (TILG1+TILG2+TILV)     ! gC tillers-1 Average tiller size
  FRTILG    = (TILG1+TILG2) / (TILG1+TILG2+TILV) ! "FRTILG"  = Fraction of tillers that is generative
  FRTILG1   =  TILG1        / (TILG1+TILG2+TILV) ! "FRTILG1" = Fraction of tillers that is in TILG1
  FRTILG2   =        TILG2  / (TILG1+TILG2+TILV) ! "FRTILG2" = Fraction of tillers that is in TILG2
  LINT      = PARINT / PAR                       ! = Percentage light interception
  DEBUG     = LAI/BASAL                          ! Output any variable as "DEBUG" for debugging purposes

  ! a script checks that these variable names match what is expected in output_names.tsv (Simon)
  if ((VERBOSE).and.(mod(day,365).eq.0)) then
    print*, 'saving for day', day
  endif

  y(day, 1) = Time
  y(day, 2) = year
  y(day, 3) = doy
  y(day, 4) = DAVTMP

  y(day, 5) = CLV
  y(day, 6) = CLVD
  y(day, 7) = TRANRF * 100.0
  y(day, 8) = CRES
  y(day, 9) = CRT
  y(day,10) = CST
  y(day,11) = CSTUB
  y(day,12) = VERND        ! (Simon changed)
  y(day,13) = PHOT         ! (Simon changed)
  y(day,14) = LAI
  y(day,15) = RESMOB       ! (Simon changed)
  y(day,16) = RAIN         ! mm Daily rainfall (Simon)
  y(day,17) = PHEN
  y(day,18) = LT50
  y(day,19) = DAYL         ! (Simon changed)
  y(day,20) = TILG2        ! (Simon changed)
  y(day,21) = TILG1        ! (Simon changed)
  y(day,22) = TILV
  y(day,23) = WAL          ! mm Soil water amount liquid
  y(day,24) = WCLM * 100.0 ! Soil moisture to ROOTDM (Simon changed)
  y(day,25) = DAYLGE       ! (Simon changed)
  y(day,26) = RDLVD        ! (Simon changed)
  y(day,27) = HARVFR * HARV! (Simon changed)

  ! Extra derived variables for calibration
  y(day,28) = DM
  y(day,29) = RES
  y(day,30) = LERG                               ! = m d-1 Leaf elongation rate per leaf for generative tillers
  y(day,31) = PHENRF                             ! Phenology effect
  y(day,32) = RLEAF                              ! = leaves tiller-1 d-1 Leaf appearance rate per tiller
  y(day,33) = SLA
  y(day,34) = TILTOT
  y(day,35) = RGRTV
  y(day,36) = RDRTIL
  y(day,37) = GRT
  y(day,38) = RDRL                               ! = d-1 Relative leaf death rate
  y(day,39) = VERN * 100.0                       ! = Vernalisation degree

  ! Simon added additional output variables
  y(day,40) = DRAIN
  y(day,41) = RUNOFF
  y(day,42) = EVAP
  y(day,43) = TRAN
  y(day,44) = LINT
  y(day,45) = DEBUG
  y(day,46) = ROOTD
  y(day,47) = TSIZE
  y(day,48) = LERV
  y(day,49) = WCL * 100.0
  y(day,50) = HARVFRIN * HARV
  y(day,51) = SLANEW
  y(day,52) = YIELD
  y(day,53) = BASAL * 100.0
  y(day,54) = GTILV
  y(day,55) = DTILV
  y(day,56) = FS
  y(day,57) = IRRIG
  y(day,58) = WAFC
  y(day,59) = IRR_TARG
  y(day,60) = IRR_TRIG
  y(day,61) = IRRIG_DEM
  y(day,62) = WAWP
  y(day,63) = MXPAW
  y(day,64) = WAL - WAWP ! paw but fix off by one error with WAL


  y(day,65) = YIELD_RYE
  y(day,66) = YIELD_WEED
  y(day,67) = DM_RYE_RM
  y(day,68) = DM_WEED_RM

  y(day,69) = DMH_RYE
  y(day,70) = DMH_WEED
  y(day,71) = DMH_RYE + DMH_WEED
  y(day, 72) = RESEEDED

  ! storage based outputs
  y(day,73) = irrig_dem_store
  y(day,74) = irrig_store
  y(day,75) = irrig_scheme
  y(day,76) = h2o_store_vol ! m3
  y(day,77) = (h2o_store_vol / (irrigated_area * 10000)) * 1000 ! mm
  y(day,78) = IRR_TRIG_store
  y(day,79) = IRR_TARG_store
   y(day,80) = store_runoff_in
   y(day,81) = store_leak_out
   y(day,82) = store_irr_loss
   y(day,83) = store_evap_out
   y(day,84) = store_scheme_in
   y(day,85) = store_scheme_in_loss



  ! Update state variables
  AGE     = AGE     + 1.0
  CLV     = CLV     + GLV   - DLV
  CLVD    = CLVD            + DLV             - DLVD       ! Simon included decomposition of dead material
  CRES    = CRES    + GRES  - RESMOB                       ! Simon modified harvest logic
  CRT     = CRT     + GRT   - DRT
  CST     = CST     + GST
  CSTUB   = CSTUB   - DSTUB
  DRYSTOR = DRYSTOR + reFreeze + Psnow - SnowMelt
  Fdepth  = Fdepth  + Frate
  LAI     = LAI     + GLAI - DLAI
  LT50    = LT50    + DeHardRate - HardRate
  O2      = O2      + O2IN - O2OUT
  PHEN    = PHEN    + GPHEN - DPHEN
  Sdepth  = Sdepth  + Psnow/RHOnewSnow - PackMelt
  TANAER  = TANAER  + dTANAER
  TILV    = TILV    + GTILV - TILVG1           - DTILV
  TILG1   = TILG1           + TILVG1 - TILG1G2
  TILG2   = TILG2                    + TILG1G2
  TILTOT  = TILG1 + TILG2 + TILV                           ! "TILTOT"  = Total tiller number in # m-2
!  BASAL   = BASAL * (1 - ABASAL) + TILTOT / (TILTOT + KBASAL) * ABASAL   ! Simon model grass basal area
!  BASAL   = BASAL * (1 - ABASAL) + min(1.0, TILTOT / KBASAL) * ABASAL   ! Simon model grass basal area
  BASAL   = BASAL * (1 - ABASAL) + min(1.0, LAI / KBASAL) * ABASAL   ! Simon model grass basal area
!  BASAL   = BASAL * (1 - ABASAL) + min(1.0, (1-exp(-KLAI*LAI)) / (1-exp(-KLAI*KBASAL)) ) * ABASAL   ! Simon model grass basal area
!  ROOTD   = ROOTD   + RROOTD                              ! Simon tied ROOTD to CRT
  ROOTD   = ROOTDM * CRT/BASAL / (CRT/BASAL + KCRT)                    ! Simon tied ROOTD to CRT like this
  VERND   = VERND   + DVERND
!  VERN    = VERN
  ! Simon treat VERN as a dynamic variable to capture effect of new summer tillers
  if (TILV>0) then
	VERN    = min(1.0, VERN + max(0.0, (VERND       -TVERNDMN)/(TVERND-TVERNDMN)) &
							- max(0.0, (VERND-DVERND-TVERNDMN)/(TVERND-TVERNDMN)) &
	                        - VERN * GTILV / TILV)
  else
	VERN    = 0.
  end if

  if (pass_soil_moist) then
    ! pass soil moisture in from external model via max_irr
    if (Irr_frm_PAW) then
      WAL     = (MAX_IRR * MXPAW) + WAWP
    else
      WAL  =  MAX_IRR * WAFC
    end if
    WALS    = 0
    WAPL    = 0
    WAPS    = 0
    WAS     = 0
    WETSTOR = 0
  else
    ! calculate soil mositure internally
    WAL     = WAL  + THAWS  - FREEZEL  + poolDrain + INFIL + EXPLOR + IRRIG - DRAIN - RUNOFF - EVAP - TRAN
    WALS    = max(0.0, min(25.0, WALS + THAWS - FREEZEL  + poolDrain + INFIL + IRRIG - DRAIN - RUNOFF - EVAP - TRAN)) ! Simon added WALS rapid surface pool
    WAPL    = WAPL + THAWPS - FREEZEPL + poolInfil - poolDrain
    WAPS    = WAPS - THAWPS + FREEZEPL
    WAS     = WAS  - THAWS  + FREEZEL
    WETSTOR = WETSTOR + Wremain - WETSTOR
  end if

enddo

end

end module basgramodule
