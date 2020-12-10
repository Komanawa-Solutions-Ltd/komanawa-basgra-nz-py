module parameters_site


implicit none

! Simulation period and time step
integer, parameter                                  :: NPAR     = 124
  real, parameter       :: DELT   =   1.0 ! Model time step

! Geography
  real                  :: LAT            ! Latitude in degrees north

! Atmospheric conditions
  real                  :: CO2A

! Soil
  real                  :: DRATE
  real                  :: WCI
  real                  :: FWCAD, FWCWP, FWCFC, FWCWET, WCST, BD
  real                  ::  WCAD,  WCWP,  WCFC,  WCWET

! Soil - WINTER PARAMETERS
  real                  :: FGAS, FO2MX, KTSNOW, KRTOTAER, KSNOW ! Simon renamed gamma as KTSNOW
  real, parameter       :: LAMBDAice      = 1.9354e+005  ! J m-1 K-1 d-1 Thermal conductivity of ice
  real                  :: LAMBDAsoil
  real, parameter       :: LatentHeat     = 335000.      ! J kg-1 Latent heat of water fusion
  real                  :: poolInfilLimit    ! m Soil frost depth limit for water infiltration
  real                  :: RHOnewSnow, RHOpack
  real, parameter       :: RHOwater       =   1000.      ! kg m-3	Density of water
  real                  :: SWret, SWrf, TmeltFreeze, TrainSnow
  real                  :: WpoolMax

! Soil initial values
  real, parameter       :: DRYSTORI = 0.
  real, parameter       :: FdepthI  = 0.
  real, parameter       :: SDEPTHI  = 0.
  real, parameter       :: TANAERI  = 0.
  real, parameter       :: WAPLI    = 0.
  real, parameter       :: WAPSI    = 0.
  real, parameter       :: WASI     = 0.
  real, parameter       :: WETSTORI = 0.

! Management: irrigation
  real       :: IRRIGF                   ! Relative irrigation rate
  real       :: IRR_TRIG ! irrigation trigger, fraction of field capacity to start irrigating at
  real       :: IRR_TARG ! irrigation target, fraction of field capacity to fill to
  logical    ::  Irr_frm_PAW ! are irrigation trigger/target the fraction of profile avalible water or field capcity.

! Management: harvest
  logical    :: FIXED_REMOVAL
  logical    :: opt_harvfrin

! Managment: reseed
  integer    :: reseed_harv_delay ! number of days to delay harvest after reseed, must be >=1
  real       :: reseed_LAI ! >=0 the leaf area index to set after reseeding, if < 0 then simply use the current LAI
  real       :: reseed_TILG2  ! Non-elongating generative tiller density after reseed if >=0 otherwise use current state of variable
  real       :: reseed_TILG1  ! Elongating generative tiller density after reseed if >=0 otherwise use current state of variable
  real       :: reseed_TILV  ! Non-elongating tiller density after reseed if >=0 otherwise use current state of variable
  real       :: reseed_CLV ! Weight of leaves after reseed if >=0 otherwise use current state of variable
  real       :: reseed_CRES  ! Weight of reserves after reseed if >=0 otherwise use current state of variable
  real       :: reseed_CST  ! Weight of stems after reseed if >=0 otherwise use current state of variable
  real       :: reseed_CSTUB  ! Weight of stubble after reseed if >=0 otherwise use current state of variable


! Mathematical constants
  real, parameter       :: pi   = 3.141592653589793
  real, parameter       :: Freq = 2.*pi / 365.
  real, parameter       :: Kmin = 4.           ! mm C-1 d-1 in SnowMeltWmaxStore()
  real, parameter       :: Ampl = 0.625        ! mm C-1 d-1 Intra-annual amplitude snow melt at 1 degree > 'TmeltFreeze' in SnowMeltWmaxStore()
  real, parameter       :: Bias = Kmin + Ampl  ! mm C-1 d-1 Average snow melting rate at 1 degree above 'TmeltFreeze' in SnowMeltWmaxStore()

end module parameters_site

