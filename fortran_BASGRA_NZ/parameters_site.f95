module parameters_site


implicit none

! Simulation period and time step
integer, parameter                                  :: NPAR     = 141
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
  real       :: abs_max_irr ! the maximum irrigation that can be applied per day (e.g. equiptment limits) mm/day
  real       :: IRRIGF                   ! Relative irrigation rate
  real       :: IRR_TRIG ! irrigation trigger, fraction of field capacity to start irrigating at
  real       :: IRR_TARG ! irrigation target, fraction of field capacity to fill to
  logical    ::  Irr_frm_PAW ! are irrigation trigger/target the fraction of profile avalible water or field capcity.
  logical    :: pass_soil_moist ! bool if TRUE then assumes that soil moisture is passed in max_irr

! managment: h2o storage
  logical   :: use_storage ! whether or not to include storage in the model
  logical   :: runoff_from_rain ! if True then use a fraction of rainfall, otherwise proscrived refill data from an external model
  logical   :: use_storage_today ! whether or not storage will be used in a given day
  logical   :: calc_ind_store_demand ! if true then calculate storage demand after scheme irrigation from triggers, targets,
                                     ! if false then calcuate storage demeand as the remaining demand after scheme irrigation
  integer   :: stor_full_refil_doy ! the day of the year when storage will be set to full.
  real      :: stor_reserve_vol ! the minimum volume to reserve for storage
  real      :: irrigated_area ! the area irrigated (ha)
  real      :: irr_trig_store ! the irrigation trigger value (if calc_ind_store_demand) for the storage based irrigation either fraction of PAW or field capacity
  real      :: irr_targ_store ! the irrigation target value (if calc_ind_store_demand) for the storage based irrigation either fraction of PAW or field capacity
  real      :: external_inflow ! only used if not runoff_from_rain, the volume (m3) of water to add to storage (allows external rainfall runoff model for storage managment)
  real      :: store_overflow ! water that could be used to fill storage, but ends up not being used as storage is full
  real      :: h2o_store_vol ! h2o storage volume (m3)
  real      :: I_h2o_store_vol ! inital h2o storage volume (m3)
  real      :: h2o_store_max_vol ! h2o storage maximum volume (m3)
  real      :: h2o_store_SA  ! h2o storage surface area (m2)
  real      :: runoff_area   ! the area that can provide runoff to the storage (ha)
  real      :: runoff_frac   ! the fraction of precipitation that becomes runoff to recharge storage (0-1, unitless)
  real      :: stor_refill_min ! the minimum amount of excess irrigation water that is needed to refill storage (mm/day)
  real      :: stor_refill_losses ! the losses incured from re-filling storage from irrigation scheme (0-1)
  real      :: stor_leakage ! the losses from storage to leakage static (m3/day)
  real      :: stor_irr_ineff ! the fraction of irrigation water that is lost when storage is used for irrigation
                              ! (e.g. 0 means a perfectly effcient system,
                              ! 1 means that 2x the storage volume is needed to irrigate x volume)
                              ! unitless
  real     :: irrig_dem_store

! output storage components

  real   ::  store_runoff_in
  real   ::  store_leak_out
  real   ::  store_irr_loss
  real   ::  store_evap_out
  real   ::  store_scheme_in
  real   ::  store_scheme_in_loss


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

