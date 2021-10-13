"""
 Author: Matt Hanson
 Created: 14/08/2020 8:53 AM
 """

param_keys = (
    # PARAMETER   # Name,  # units   #  Description
    'LOG10CLVI',  # CLVI,  # gC m-2, # Initial value of leaves
    'LOG10CRESI',  # CRESI,  # gC m-2, # Initial value of reserves
    'LOG10CRTI',  # CRTI,  # gC m-2, # Initial value of roots
    'CSTI',  # CSTI,  # gC m-2, # Initial value of stems
    'LOG10LAII',  # LAII,  # m2 m-2, # Initial value of leaf area index
    'PHENI',  # PHENI,  # -, # Initial value of phenological stage
    'TILTOTI',  # TILTOTI,  # m-2, # Initial value of tiller density
    'FRTILGI',  # FRTILGI,  # -, # Initial value of elongating tiller fraction
    'LT50I',  # LT50I,  # Â°C, # Initial value of LT50
    'CLAIV',  # CLAIV,  # m2 leaf m-2, # Maximum LAI remaining after harvest, when no tillers elongate
    'COCRESMX',  # COCRESMX,  # -, # Maximum concentration of reserves in aboveground biomass
    'CSTAVM',  # CSTAVM,  # gC tiller-1, # Maximum stem mass of elongating tillers
    'DAYLB',
    # DAYLB,  # d d-1, # Day length below which DAYLGE becomes 0 and phenological stage is reset to zero (must be < DLMXGE)
    'DAYLP',  # DAYLP,  # d d-1, # Day length below which phenological development slows down
    'DLMXGE',  # DLMXGE,  # d d-1, # Day length below which DAYLGE becomes less than 1 (should be < maximum DAYL?)
    'FSLAMIN',  # FSLAMIN,  # -, # Minimum SLA of new leaves as a fraction of maximum possible SLA (must be < 1)
    'FSMAX',  # FSMAX,  # -, # Maximum ratio of tiller and leaf appearance based on sward geometry (must be < 1)
    'HAGERE',  # HAGERE,  # -, # Parameter for proportion of stem harvested
    'KLAI',  # K,  # m2 m-2 leaf, # PAR extinction coefficient
    'LAICR',  # LAICR,  # m2 leaf m-2, # LAI above which shading induces leaf senescence
    'LAIEFT',  # LAIEFT,  # m2 m-2 leaf, # Decrease in tillering with leaf area index
    'LAITIL',  # LAITIL,  # -, # Maximum ratio of tiller and leaf apearance at low leaf area index
    'LFWIDG',  # LFWIDG,  # m, # Leaf width on elongating tillers
    'LFWIDV',  # LFWIDV,  # m, # Leaf width on non-elongating tillers
    'NELLVM',  # NELLVM,  # tiller-1, # Number of elongating leaves per non-elongating tiller
    'PHENCR',
    # PHENCR,  # -, # Phenological stage above which elongation and appearance of leaves on elongating tillers decreases
    'PHY',  # PHY,  # Â°C d, # Phyllochron
    'RDRSCO',
    # RDRSCO,  # d-1, # Increase in relative death rate of leaves and non-elongating tillers due to shading per unit of LAI above LAICR
    'RDRSMX',  # RDRSMX,  # d-1, # Maximum relative death rate of leaves and non-elongating tillers due to shading
    'RDRTEM',  # RDRTEM,  # d-1 Â°C-1, # Proportionality of leaf senescence with temperature
    'RGENMX',  # RGENMX,  # d-1, # Maximum relative rate of tillers becoming elongating tillers
    'ROOTDM',  # ROOTDM,  # m, # Initial and maximum value rooting depth
    'RRDMAX',  # RRDMAX,  # m d-1, # Maximum root depth growth rate
    'RUBISC',  # RUBISC,  # g m-2 leaf, # Rubisco content of upper leaves
    'LSHAPE',  # SHAPE,  # -, # Area of a leaf relative to a rectangle of same length and width (must be < 1)
    'SIMAX1T',  # SIMAX1T,  # gC tiller-1 d-1, # Sink strength of small elongating tillers
    'SLAMAX',  # SLAMAX,  # m2 leaf gC-1, # Maximum SLA of new leaves (Note unusual units#)
    'TBASE',  # TBASE,  # Â°C, # Minimum value of effective temperature for leaf elongation
    'TCRES',  # TCRES,  # d, # Time constant of mobilisation of reserves
    'TOPTGE',  # TOPTGE,  # Â°C, # Optimum temperature for vegetative tillers to become generative (must be > TBASE)
    'TRANCO',  # TRANCO,  # mm d-1 g-1 m2, # Transpiration effect of PET
    'YG',  # YG,  # gC gC-1, # Growth yield per unit expended carbohydrate (must be < 1)

    'LAT',  # LAT,  # degN, # Latitude
    'WCI',  # WCI,  # m3 m-3, # Initial value of volumetric water content
    'FWCAD',  # WCAD,  # m3 m-3, # Relative saturation at air dryness
    'FWCWP',  # WCWP,  # m3 m-3, # Relative saturation at wilting point
    'FWCFC',  # WCFC,  # m3 m-3, # Relative saturation at field capacity
    'FWCWET',  # WCWET,  # m3 m-3, # Relative saturation above which transpiration is reduced
    'WCST',  # WCST,  # m3 m-3, # Volumetric water content at saturation
    'WpoolMax',  # WpoolMax,  # mm, # Maximum pool water (liquid plus ice)
    'Dparam',  # Dparam,  # Â°C-1 d-1, # Constant in the calculation of dehardening rate
    'FGAS',  # FGAS,  # -, # Fraction of soil volume that is gaseous
    'FO2MX',  # FO2MX,  # mol O2 mol-1 gas, # Maximum oxygen fraction of soil gas
    'KTSNOW',  # gamma,  # m-1, # Temperature extinction coefficient of snow
    'Hparam',  # Hparam,  # Â°C-1 d-1, # Hardening parameter
    'KRDRANAER',  # KRDRANAER,  # d-1, # Maximum relative death rate due to anearobic conditions
    'KRESPHARD',  # KRESPHARD,  # gC gC-1 Â°C-1, # Carbohydrate requirement of hardening
    'KRSR3H',  # KRSR3H,  # Â°C-1, # Constant in the logistic curve for frost survival
    'KRTOTAER',  # KRTOTAER,  # -, # Ratio of total to aerobic respiration
    'KSNOW',  # KSNOW,  # mm-1, # Light extinction coefficient of snow
    'LAMBDAsoil',  # LAMBDAsoil,  # J m-1 degC-1 d-1, # Thermal conductivity of soil?
    'LDT50A',  # LDT50A,  # d, # Intercept of linear dependence of LD50 on lT50
    'LDT50B',  # LDT50B,  # d Â°C-1, # Slope of linear dependence of LD50 on LT50
    'LT50MN',  # LT50MN,  # Â°C, # Minimum LT50 (Lethal temperature at which 50% die)
    'LT50MX',  # LT50MX,  # Â°C, # Maximum LT50
    'RATEDMX',  # RATEDMX,  # Â°C d-1, # Maximum dehardening rate
    'reHardRedDay',  # reHardRedDay,  # d, # Duration of period over which rehardening capability disappears
    'RHOnewSnow',  # RHOnewSnow,  # kg SWE m-3, # Density of newly fallen snow
    'RHOpack',  # RHOpack,  # d-1, # Relative packing rate of snow
    'SWret',  # SWret,  # mm mm-1 d-1, # Liquid water storage capacity of snow
    'SWrf',  # SWrf,  # mm d-1 Â°C-1, # Maximum refreezing rate per degree below 'TmeltFreeze'
    'THARDMX',  # THARDMX,  # Â°C, # Maximum surface temperature at which hardening is possible
    'TmeltFreeze',  # TmeltFreeze,  # Â°C, # Temperature above which snow melts
    'TrainSnow',  # TrainSnow,  # Â°C, # Temperature below which precipitation is snow
    'TsurfDiff',  # TsurfDiff,  # Â°C, # Constant in the calculation of dehardening rate
    'KLUETILG',  # KLUETILG,  # -, # LUE-increase with increasing fraction elongating tillers
    'FRTILGG1I',  # FRTILGG1I,  # -, # Initial fraction of generative tillers that is still in stage 1
    'DAYLG1G2',  # DAYLG1G2,  # d d-1, # Minimum day length above which generative tillers can start elongating
    'RGRTG1G2',  # RGRTG1G2,  # d-1, # Relative rate of TILG1 becoming TILG2
    'RDRTMIN',  # RDRTMIN,  # d-1, # Minimum relative death rate of foliage
    'TVERN',  # TVERN,  # Â°C, # Temperature below which vernalisation advances
    'TVERND',  # TVERND,  # d, # Days of cold after which vernalisation completed
    'RDRSTUB',  # RDRSTUB,  # -, # Relative death rate of stubble/pseudostem
    'LERGB',  # LERGB,  # mm d-1 Â°C-1, # Leaf elongation slope generative
    'RDRROOT',  # RDRROOT,  # d-1, # Relatuive death rate of root mass CRT
    'DAYLA',  # DAYLA,  # -, # DAYL above which growth is prioritised over storage
    'DAYLRV',  # DAYLRV,  # -, # DAYL at which vernalisation is reset
    'FCOCRESMN',  # FCOCRESMN,  # -, # Minimum concentration of reserves in aboveground biomass as fraction of COCRESMX
    'KCRT',  # KCRT,  # gC m-2, # Root mass at which ROOTD is 67% of ROOTDM
    'VERNDI',  # VERNDI,  # d, # Initial value of cumulative vernalisation days
    'LERVA',  # LERVA,  # Â°C, # Leaf elongation intercept vegetative
    'LERVB',  # LERVB,  # mm d-1 Â°C-1, # Leaf elongation slope vegetative
    'LERGA',  # LERGA,  # Â°C, # Leaf elongation intercept generative
    'RDRTILMIN',  # RDRTILMIN,  # d-1, # Background relative rate of tiller death
    'RDRHARVMAX',  # RDRHARVMAX,  # d-1, # Maximum relative death rate due to harvest
    'FGRESSI',  # FGRESSI,  # -, # CRES sink strength factor
    'BD',  # BD,  # kg l-1, # Bulk density of soil
    'HARVFRD',  # HARVFRD,  # -, # Relative harvest fraction of CLVD
    'EBIOMAX',  # EBIOMAX,  # -, # Earthworm biomass max
    'KBASAL',  # KBASAL,  # ?, # Constant at half basal area
    'RDRWMAX',  # RDRWMAX,  # d-1, # Maximum death rate due to water stress
    'BASALI',  # BASALI,  # -, # Grass basal area
    'ABASAL',  # ABASAL,  # d-1, # Grass basal area response rate
    'TVERNDMN',  # TVERNDMN,  # d, # Minimum vernalisation days
    'DAYLGEMN',  # DAYLGEMN,  # -, # Minimum daylength growth effect
    'TRANRFCR',  # TRANRFCR,  # -, # Critical water stress for tiller death
    'DELE',  # DELE,  # -, # Litter disappearance due to earthworms
    'DELD',  # DELD,  # -, # Litter disappearance due to decomposition

    # site parameters brought out
    'IRRIGF',  # fraction # fraction of the needed irrigation to apply to bring water content up to field capacity
    'DRATE',  # woodward set to 50   # mm d-1 Maximum soil drainage rate #
    'CO2A',  # woodward set to 350   # CO2 concentration in atmosphere (ppm)
    'poolInfilLimit',  # woodward set to  0.2     # m Soil frost depth limit for water infiltration

    # new for irrigation
    'irr_frm_paw',  # # are irrigation trigger/target the fraction of profile available water (1/True or
    # the fraction of field capacity (0/False).

    # new for harvest, certainly parameters
    'fixed_removal',  # sudo boolean defines if auto_harv_targ is fixed amount or amount to harvest to
    'opt_harvfrin',  # # sudo boolean(1=True, 0=False) if True, harvest fraction is estimated by brent zero optimisation
    # if false, HARVFRIN = DM_RYE_RM/DMH_RYE.  As the harvest fraction is non-linearly related to the
    # harvest, the amount harvested may be significantly greather than expected depending on CST
    'reseed_harv_delay',  # number of days to delay harvest after reseed, must be >=1 and must be a whole number
    'reseed_LAI',  # >=0 the leaf area index to set after reseeding, if < 0 then simply use the current LAI
    'reseed_TILG2',
    # Non-elongating generative tiller density after reseed if >=0 otherwise use current state of variable
    'reseed_TILG1',  # Elongating generative tiller density after reseed if >=0 otherwise use current state of variable
    'reseed_TILV',  # Non-elongating tiller density after reseed if >=0 otherwise use current state of variable
    'reseed_CLV',  # Weight of leaves after reseed if >= 0 otherwise use current state of variable
    'reseed_CRES',  # Weight of reserves after reseed if >= 0 otherwise use current state of variable
    'reseed_CST',  # Weight of stems after reseed if >= 0 otherwise use current state of variable
    'reseed_CSTUB',  # Weight of stubble after reseed if >= 0 otherwise use current state of variable

    'pass_soil_moist',  # sudo boolean 1=True, 0=False.  if True then do not calculate soil moisture instead
    # soil moisture is passed to the model through max_irr as a fraction of either soil capacity
    # when 'irr_frm_paw' is False, or as a fraction (0-1) of PAW when 'irr_frm_paw' is True
    # this prevent any irrigation scheduling or and soil moisture calculation in the model.

    'use_storage',  # whether or not to include storage in the model, sudo boolean 1=True, 0=False
    'runoff_from_rain',  # if True then use a fraction of rainfall, otherwise proscribed refill data from an
    # external model, sudo boolean 1=True, 0=False
    'calc_ind_store_demand',  # if true then calculate storage demand after scheme irrigation from triggers, targets,
    # =  if false then calculate storage demand as the remaining demand after scheme irrigation,
    # sudo boolean 1=True, 0=False

    # integer
    'stor_full_refil_doy',  # the day of the year (0-366) when storage will be set to full.,
    # set to -1 to never fully refill storage

    # float
    'abs_max_irr',  # the maximum irrigation that can be applied per day (e.g. equipment limits) mm/day note that if
    # matrix weather prescribed max_irr for a given day is larger then abs_max_irr, that water may still be avalible
    # to refill storage.
    'irrigated_area',  # the area irrigated (ha)
    'I_h2o_store_vol',  # initial h2o storage fraction
    'h2o_store_max_vol',  # h2o storage maximum volume (m3)
    'h2o_store_SA',  # h2o storage surface area (m2)
    'runoff_area',  # the area that can provide runoff to the storage (ha)
    'runoff_frac',  # the fraction of precipitation that becomes runoff to recharge storage (0-1, unit less)
    'stor_refill_min',  # the minimum amount of excess irrigation water that is needed to refill storage (mm/day)
    'stor_refill_losses',  # the losses incurred from re-filling storage from irrigation scheme (0-1)
    'stor_leakage',  # the losses from storage to leakage static (m3/day)
    'stor_irr_ineff',  # the fraction of irrigation water that is lost when storage is used for irrigation
    # (e.g. 0 means a perfectly efficient system,
    # 1 means that 2x the storage volume is needed to irrigate x volume)
    # unit less
    'stor_reserve_vol',  # the volume of storage to reserve (e.g. irrigation is cutoff at this volume) (m3)

)

days_harvest_keys = (
    'year',  # e.g. 2002
    'doy',  # day of year 1 - 356 (366 for leap year)
    'frac_harv',
    # fraction (0-1) of material above target to harvest to maintain 'backward capabilities' with v2.0.0
    'harv_trig',  # dm above which to initiate harvest, if trigger is less than zero no harvest will take place
    'harv_targ',  # dm to harvest to or to remove depending on 'fixed_removal'
    'weed_dm_frac',  # fraction of dm of ryegrass to attribute to weeds
    'reseed_trig',  # when BASAL <= reseed_trig, trigger a reseeding. if <0 then do not reseed
    'reseed_basal',  # set BASAL = reseed_basal when reseeding.

)

matrix_weather_keys_pet = (
    'year',  # e.g. 2002
    'doy',  # day of year 1 - 356 or 366 for leap years
    'radn',  # daily solar radiation (MJ/m2)
    'tmin',  # daily min (degrees C)
    'tmax',  # daily max (degrees C)
    'rain',  # sum daily rainfall (mm)
    'pet',  # priestly evapotransperation (mm)
    'max_irr',  # maximum irrigation available (mm/d) when 'pass_soil_moist' is False or the fraction (0-1)
    # PAW/Field capacity to be passed to the model when 'pass_soil_moist' is True,
    # see 'pass_soil_moist' for more details
    'irr_trig',  # fraction of PAW/field (see irr_frm_paw) at or below which irrigation is triggered (fraction 0-1)
    # e.g. 0.5 means that irrigation will only be applied when soil water content is at 1/2
    # field capacity (e.g. water holding capacity)
    'irr_targ',  # fraction of PAW/field (see irr_frm_paw) to irrigate to (fraction 0-1)
    'irr_trig_store',  # the irrigation trigger value (if calc_ind_store_demand)
    # for the storage based irrigation either fraction of PAW or field capacity
    'irr_targ_store',  # the irrigation target value (if calc_ind_store_demand)
    # for the storage based irrigation either fraction of PAW or field capacity
    'external_inflow',  # only used if not runoff_from_rain, the volume (m3) of water to add
    # to storage (allows external rainfall runoff model for storage management)
)

matrix_weather_keys_penman = (
    'year',  # e.g. 2002
    'doy',  # day of year 1 - 356 or 366 for leap years
    'radn',  # daily solar radiation (MJ/m2)
    'tmin',  # daily min (degrees C)
    'tmax',  # daily max (degrees C)
    'vpa',  # vapour pressure (kPa)
    'rain',  # sum daily rainfall (mm/day)
    'wind',  # mean wind speed m/s at 2m
    'max_irr',  # maximum irrigation available (mm/d)  when 'pass_soil_moist' is False or the fraction (0-1)
    # PAW/Field capacity to be passed to the model when 'pass_soil_moist' is True,
    # see 'pass_soil_moist' for more details
    'irr_trig',  # fraction of field capacity at or below which irrigation is triggered (fraction 0-1)
    # e.g. 0.5 means that irrigation will only be applied when soil water content is at 1/2
    # field capacity (e.g. water holding capacity)
    'irr_targ',  # fraction of field capacity to irrigate to (fraction 0-1)
    'irr_trig_store',  # the irrigation trigger value (if calc_ind_store_demand)
    # for the storage based irrigation either fraction of PAW or field capacity
    'irr_targ_store',  # the irrigation target value (if calc_ind_store_demand)
    # for the storage based irrigation either fraction of PAW or field capacity
    'external_inflow',  # only used if not runoff_from_rain, the volume (m3) of water to add
    # to storage (allows external rainfall runoff model for storage management)
)

out_cols = (
    # varname, # shortname, # units
    'Time',  # Time, #  (y)
    'year',  # Year, #  (y)
    'doy',  # Day of Year, #  (d)
    'DAVTMP',  # Av. Temp., #  (degC)
    'CLV',  # Leaf C, #  (gC m-2)
    'CLVD',  # Dead Leaf C, #  (gC m-2)
    'TRANRF',  # Transpiration, #  (%)
    'CRES',  # Reserve C, #  (gC m-2)
    'CRT',  # Root C, #  (gC m-2)
    'CST',  # Stem C, #  (gC m-2)
    'CSTUB',  # Stubble C, #  (gC m-2)
    'VERND',  # Vern. Days, #  (d)
    'PHOT',  # Photosyn., #  (gC m-2 d-1)
    'LAI',  # LAI, #  (m2 m-2)
    'RESMOB',  # Res. Mobil., #  (gC m-2 d-1)
    'RAIN',  # Rain, #  (mm d-1)
    'PHEN',  # Phen. Stage, #  (-)
    'LT50',  # Hardening, #  (degC)
    'DAYL',  # Daylength, #  (-)
    'TILG2',  # Elong. Tillers, #  (m-2)
    'TILG1',  # Gen. Tillers, #  (m-2)
    'TILV',  # Veg. Tillers, #  (m-2)
    'WAL',  # Soil Water, #  (mm)
    'WCLM',  # Soil Moisture, #  (%)
    'DAYLGE',  # Daylength Fact., #  (-)
    'RDLVD',  # Decomp. Rate, #  (d-1)
    'HARVFR',  # Harvest Frac., #  (-)

    'DM',  # Ryegrass Mass, #  (kg DM ha-1) Note that this is after any harvest (e.g. at end of time stamp)
    'RES',  # Reserve C, #  (g g-1)
    'LERG',  # Gen. Elong. Rate, #  (m d-1)
    'PHENRF',  # Phen. Effect, #  (-)
    'RLEAF',  # Leaf App. Rate, #  (d-1)
    'SLA',  # Spec. Leaf Area, #  (m2 gC-1)
    'TILTOT',  # Total Tillers, #  (m-2)
    'RGRTV',  # Till. App. Rate, #  (d-1)
    'RDRTIL',  # Till. Death Rate , #  (d-1)
    'GRT',  # Root Growth, #  (gC m-2 d-1)
    'RDRL',  # Leaf Death Rate, #  (d-1)
    'VERN',  # Vernalisation, #  (%)

    'DRAIN',  # Drainage, #  (mm d-1)
    'RUNOFF',  # Runoff, #  (mm d-1)
    'EVAP',  # Evap., #  (mm d-1)
    'TRAN',  # Trans., #  (mm d-1)
    'LINT',  # Light Intercep., #  (-)
    'DEBUG',  # Debug, #  (?)
    'ROOTD',  # Root Depth, #  (m)
    'TSIZE',  # Tiller Size, #  (gC tiller-1)
    'LERV',  # Veg. Elong. Rate, #  (m d-1)
    'WCL',  # Eff. Soil Moisture, #  (%)
    'HARVFRIN',  # Harvest Data, #  (-)
    'SLANEW',  # New SLA, #  (m2 gC-1)
    'YIELD',  # PRG Yield, #  (tDM ha-1) sum of YIELD_RYE and YIELD_WEED
    'BASAL',  # Basal Area, #  (%)
    'GTILV',  # Till. Birth, #  (till m-2 d-1)
    'DTILV',  # Till. Death, #  (till m-2 d-1)
    'FS',  # Site Filling, #  (till leaf-1)
    'IRRIG',  # mm d-1 Irrigation,
    'WAFC',  # mm # Water in non-frozen root zone at field capacity
    'IRR_TARG',  # irrigation Target (fraction of field capacity) to fill to, also an input variable
    'IRR_TRIG',  # irrigation trigger (fraction of field capacity at which to start irrigating
    'IRRIG_DEM',  # irrigation irrigation demand to field capacity * IRR_TARG # mm
    'WAWP',  # # mm # Water in non-frozen root zone at wilting point
    'MXPAW',  # mm # maximum Profile available water
    'PAW',  # mm Profile available water at the time step

    'RYE_YIELD',  # PRG Yield from rye grass species, #  (tDM ha-1)  note that this is the actual amount of
    # material that has been removed
    'WEED_YIELD',  # PRG Yield from weed (other) species, #  (tDM ha-1)  note that this is the actual amount
    # of material that has been removed
    'DM_RYE_RM',  # dry matter of Rye species harvested in this time step (kg DM ha-1) Note that this is the
    # calculated removal but if 'opt_harvfrin' = False then it may be significantly different to the
    # actual removal, which is show by the appropriate yeild variable
    'DM_WEED_RM',  # dry matter of weed species harvested in this time step (kg DM ha-1)
    # Note that this is the calculated removal but if 'opt_harvfrin' = False then it may be
    # significantly different to the actual removal, which is show by the appropriate yeild variable
    'DMH_RYE',  # harvestable dry matter of rye species, includes harvestable fraction of dead (HARVFRD) (kg DM ha-1)
    # note that this is before any removal by harvesting
    'DMH_WEED',  # harvestable dry matter of weed specie, includes harvestable fraction of dead (HARVFRD) (kg DM ha-1)
    # note that this is before any removal by harvesting
    'DMH',  # harvestable dry matter = DMH_RYE + DMH_WEED  (kg DM ha-1)
    # note that this is before any removal by harvesting

    'RESEEDED',  # reseeded flag, if ==1 then the simulation was reseeded on this day

    'irrig_dem_store',  # irrigation demand from storage (mm)
    'irrig_store',  # irrigation applied from storage (mm)
    'irrig_scheme',  # irrigation applied from the scheme (mm)
    'h2o_store_vol',  # volume of water in storage (m3)
    'h2o_store_per_area',  # h2o storage per irrigated area (mm)
    'IRR_TRIG_store',  # irrigation trigger for storage (fraction paw/FC), input, only relevant if calc_ind_store_demand
    'IRR_TARG_store',  # irrigation target for storage (fraction paw/FC), input, only relevant if calc_ind_store_demand
    'store_runoff_in',  # storage budget in from runoff or external model (m3)
    'store_leak_out',  # storage budget out from leakage (m3)
    'store_irr_loss',  # storage budget out from losses incurred with irrigation (m3)
    'store_evap_out',  # storage budget out from evaporation (NOTIMPLEMENTED) (m3)
    'store_scheme_in',  # storage budget in from the irrigation scheme (m3)
    'store_scheme_in_loss',  # storage budget out losses from the scheme to the storage basin (m3)

    # remember to add new ones to output describtion.csv

)

site_param_keys = (
    'LAT',  # LAT,  # degN, # Latitude
    'WCI',  # WCI,  # m3 m-3, # Initial value of volumetric water content
    'FWCAD',  # WCAD,  # m3 m-3, # Relative saturation at air dryness
    'FWCWP',  # WCWP,  # m3 m-3, # Relative saturation at wilting point
    'FWCFC',  # WCFC,  # m3 m-3, # Relative saturation at field capacity
    'FWCWET',  # WCWET,  # m3 m-3, # Relative saturation above which transpiration is reduced
    'WCST',  # WCST,  # m3 m-3, # Volumetric water content at saturation
    'WpoolMax',  # WpoolMax,  # mm, # Maximum pool water (liquid plus ice)
    'FGAS',  # FGAS,  # -, # Fraction of soil volume that is gaseous
    'FO2MX',  # FO2MX,  # mol O2 mol-1 gas, # Maximum oxygen fraction of soil gas
    'KTSNOW',  # gamma,  # m-1, # Temperature extinction coefficient of snow
    'KRTOTAER',  # KRTOTAER,  # -, # Ratio of total to aerobic respiration
    'KSNOW',  # KSNOW,  # mm-1, # Light extinction coefficient of snow
    'LAMBDAsoil',  # LAMBDAsoil,  # J m-1 degC-1 d-1, # Thermal conductivity of soil?
    'RHOnewSnow',  # RHOnewSnow,  # kg SWE m-3, # Density of newly fallen snow
    'RHOpack',  # RHOpack,  # d-1, # Relative packing rate of snow
    'SWret',  # SWret,  # mm mm-1 d-1, # Liquid water storage capacity of snow
    'SWrf',  # SWrf,  # mm d-1 Â°C-1, # Maximum refreezing rate per degree below 'TmeltFreeze'
    'TmeltFreeze',  # TmeltFreeze,  # Â°C, # Temperature above which snow melts
    'TrainSnow',  # TrainSnow,  # Â°C, # Temperature below which precipitation is snow
    'BD',  # BD,  # kg l-1, # Bulk density of soil

    'IRRIGF',  # fraction # fraction of the needed irrigation to apply to bring water content up to field capacity
    'irr_frm_paw',  # # are irrigation trigger/target the fraction of profile available water (1/True or
    # the fraction of field capacity (0/False).
    'DRATE',  # woodward set to 50   # mm d-1 Maximum soil drainage rate #
    'CO2A',  # woodward set to 350   # CO2 concentration in atmosphere (ppm)
    'poolInfilLimit',  # woodward set to  0.2     # m Soil frost depth limit for water infiltration
    'fixed_removal',  # sudo boolean(1=True, 0=False) defines if auto_harv_targ is fixed amount or amount to harvest to,
    'opt_harvfrin',  # # sudo boolean(1=True, 0=False) if True, harvest fraction is estimated by brent zero optimisation
    # if false, HARVFRIN = DM_RYE_RM/DMH_RYE.  As the harvest fraction is non-linearly related to the
    # harvest, the amount harvested may be significantly greather than expected depending on CST
    'reseed_harv_delay',  # number of days to delay harvest after reseed, must be >=1
    'reseed_LAI',  # >=0 the leaf area index to set after reseeding, if < 0 then simply use the current LAI
    'reseed_TILG2',
    # Non-elongating generative tiller density after reseed if >=0 otherwise use current state of variable
    'reseed_TILG1',  # Elongating generative tiller density after reseed if >=0 otherwise use current state of variable
    'reseed_TILV',  # Non-elongating tiller density after reseed if >=0 otherwise use current state of variable
    'reseed_CLV',  # Weight of leaves after reseed if >= 0 otherwise use current state of variable
    'reseed_CRES',  # Weight of reserves after reseed if >= 0 otherwise use current state of variable
    'reseed_CST',  # Weight of stems after reseed if >= 0 otherwise use current state of variable
    'reseed_CSTUB',  # Weight of stubble after reseed if >= 0 otherwise use current state of variable
    'pass_soil_moist',  # sudo boolean 1=True, 0=False.  if True then do not calculate soil moisture instead
    # soil moisture is passed to the model through max_irr as a fraction of either soil capacity
    # when 'irr_frm_paw' is False, or as a fraction (0-1) of PAW when 'irr_frm_paw' is True
    'use_storage',  # whether or not to include storage in the model, sudo boolean 1=True, 0=False
    'runoff_from_rain',  # if True then use a fraction of rainfall, otherwise proscribed refill data from an
    # external model, sudo boolean 1=True, 0=False
    'calc_ind_store_demand',  # if true then calculate storage demand after scheme irrigation from triggers, targets,
    # =  if false then calculate storage demand as the remaining demand after scheme irrigation,
    # sudo boolean 1=True, 0=False

    # integer
    'stor_full_refil_doy',  # the day of the year when storage will be set to full., set to -1 to never fully refill
    # storage

    # float
    'abs_max_irr',  # the maximum irrigation that can be applied per day (e.g. equipment limits) mm/day note that if
    # matrix weather prescribed max_irr for a given day is larger then abs_max_irr, that water may still be avalible
    # to refill storage.
    'irrigated_area',  # the area irrigated (ha)
    'I_h2o_store_vol',  # initial h2o storage volume (m3)
    'h2o_store_max_vol',  # h2o storage maximum volume (m3)
    'h2o_store_SA',  # h2o storage surface area (m2)
    'runoff_area',  # the area that can provide runoff to the storage (ha)
    'runoff_frac',  # the fraction of precipitation that becomes runoff to recharge storage (0-1, unit less)
    'stor_refill_min',  # the minimum amount of excess irrigation water that is needed to refill storage (mm/day)
    'stor_refill_losses',  # the losses incurred from re-filling storage from irrigation scheme (0-1)
    'stor_leakage',  # the losses from storage to leakage static (m3/day)
    'stor_irr_ineff',  # the fraction of irrigation water that is lost when storage is used for irrigation
    # (e.g. 0 means a perfectly efficient system,
    # 1 means that 2x the storage volume is needed to irrigate x volume)
    # unit less
    'stor_reserve_vol',  # the volume of storage to reserve (e.g. irrigation is cutoff at this volume) (m3)

)
plant_param_keys = (
    # PARAMETER   # Name,  # units   #  Description
    'LOG10CLVI',  # CLVI,  # gC m-2, # Initial value of leaves
    'LOG10CRESI',  # CRESI,  # gC m-2, # Initial value of reserves
    'LOG10CRTI',  # CRTI,  # gC m-2, # Initial value of roots
    'CSTI',  # CSTI,  # gC m-2, # Initial value of stems
    'LOG10LAII',  # LAII,  # m2 m-2, # Initial value of leaf area index
    'PHENI',  # PHENI,  # -, # Initial value of phenological stage
    'TILTOTI',  # TILTOTI,  # m-2, # Initial value of tiller density
    'FRTILGI',  # FRTILGI,  # -, # Initial value of elongating tiller fraction
    'LT50I',  # LT50I,  # Â°C, # Initial value of LT50
    'CLAIV',  # CLAIV,  # m2 leaf m-2, # Maximum LAI remaining after harvest, when no tillers elongate
    'COCRESMX',  # COCRESMX,  # -, # Maximum concentration of reserves in aboveground biomass
    'CSTAVM',  # CSTAVM,  # gC tiller-1, # Maximum stem mass of elongating tillers
    'DAYLB',
    # DAYLB,  # d d-1, # Day length below which DAYLGE becomes 0 and phenological stage is reset to zero (must be < DLMXGE)
    'DAYLP',  # DAYLP,  # d d-1, # Day length below which phenological development slows down
    'DLMXGE',  # DLMXGE,  # d d-1, # Day length below which DAYLGE becomes less than 1 (should be < maximum DAYL?)
    'FSLAMIN',  # FSLAMIN,  # -, # Minimum SLA of new leaves as a fraction of maximum possible SLA (must be < 1)
    'FSMAX',  # FSMAX,  # -, # Maximum ratio of tiller and leaf appearance based on sward geometry (must be < 1)
    'HAGERE',  # HAGERE,  # -, # Parameter for proportion of stem harvested
    'KLAI',  # K,  # m2 m-2 leaf, # PAR extinction coefficient
    'LAICR',  # LAICR,  # m2 leaf m-2, # LAI above which shading induces leaf senescence
    'LAIEFT',  # LAIEFT,  # m2 m-2 leaf, # Decrease in tillering with leaf area index
    'LAITIL',  # LAITIL,  # -, # Maximum ratio of tiller and leaf apearance at low leaf area index
    'LFWIDG',  # LFWIDG,  # m, # Leaf width on elongating tillers
    'LFWIDV',  # LFWIDV,  # m, # Leaf width on non-elongating tillers
    'NELLVM',  # NELLVM,  # tiller-1, # Number of elongating leaves per non-elongating tiller
    'PHENCR',
    # PHENCR,  # -, # Phenological stage above which elongation and appearance of leaves on elongating tillers decreases
    'PHY',  # PHY,  # Â°C d, # Phyllochron
    'RDRSCO',
    # RDRSCO,  # d-1, # Increase in relative death rate of leaves and non-elongating tillers due to shading per unit of LAI above LAICR
    'RDRSMX',  # RDRSMX,  # d-1, # Maximum relative death rate of leaves and non-elongating tillers due to shading
    'RDRTEM',  # RDRTEM,  # d-1 Â°C-1, # Proportionality of leaf senescence with temperature
    'RGENMX',  # RGENMX,  # d-1, # Maximum relative rate of tillers becoming elongating tillers
    'ROOTDM',  # ROOTDM,  # m, # Initial and maximum value rooting depth
    'RRDMAX',  # RRDMAX,  # m d-1, # Maximum root depth growth rate
    'RUBISC',  # RUBISC,  # g m-2 leaf, # Rubisco content of upper leaves
    'LSHAPE',  # SHAPE,  # -, # Area of a leaf relative to a rectangle of same length and width (must be < 1)
    'SIMAX1T',  # SIMAX1T,  # gC tiller-1 d-1, # Sink strength of small elongating tillers
    'SLAMAX',  # SLAMAX,  # m2 leaf gC-1, # Maximum SLA of new leaves (Note unusual units#)
    'TBASE',  # TBASE,  # Â°C, # Minimum value of effective temperature for leaf elongation
    'TCRES',  # TCRES,  # d, # Time constant of mobilisation of reserves
    'TOPTGE',  # TOPTGE,  # Â°C, # Optimum temperature for vegetative tillers to become generative (must be > TBASE)
    'TRANCO',  # TRANCO,  # mm d-1 g-1 m2, # Transpiration effect of PET
    'YG',  # YG,  # gC gC-1, # Growth yield per unit expended carbohydrate (must be < 1)
    'Dparam',  # Dparam,  # Â°C-1 d-1, # Constant in the calculation of dehardening rate
    'Hparam',  # Hparam,  # Â°C-1 d-1, # Hardening parameter
    'KRDRANAER',  # KRDRANAER,  # d-1, # Maximum relative death rate due to anearobic conditions
    'KRESPHARD',  # KRESPHARD,  # gC gC-1 Â°C-1, # Carbohydrate requirement of hardening
    'KRSR3H',  # KRSR3H,  # Â°C-1, # Constant in the logistic curve for frost survival
    'LDT50A',  # LDT50A,  # d, # Intercept of linear dependence of LD50 on lT50
    'LDT50B',  # LDT50B,  # d Â°C-1, # Slope of linear dependence of LD50 on LT50
    'LT50MN',  # LT50MN,  # Â°C, # Minimum LT50 (Lethal temperature at which 50% die)
    'LT50MX',  # LT50MX,  # Â°C, # Maximum LT50
    'RATEDMX',  # RATEDMX,  # Â°C d-1, # Maximum dehardening rate
    'reHardRedDay',  # reHardRedDay,  # d, # Duration of period over which rehardening capability disappears
    'THARDMX',  # THARDMX,  # Â°C, # Maximum surface temperature at which hardening is possible
    'TsurfDiff',  # TsurfDiff,  # Â°C, # Constant in the calculation of dehardening rate
    'KLUETILG',  # KLUETILG,  # -, # LUE-increase with increasing fraction elongating tillers
    'FRTILGG1I',  # FRTILGG1I,  # -, # Initial fraction of generative tillers that is still in stage 1
    'DAYLG1G2',  # DAYLG1G2,  # d d-1, # Minimum day length above which generative tillers can start elongating
    'RGRTG1G2',  # RGRTG1G2,  # d-1, # Relative rate of TILG1 becoming TILG2
    'RDRTMIN',  # RDRTMIN,  # d-1, # Minimum relative death rate of foliage
    'TVERN',  # TVERN,  # Â°C, # Temperature below which vernalisation advances
    'TVERND',  # TVERND,  # d, # Days of cold after which vernalisation completed
    'RDRSTUB',  # RDRSTUB,  # -, # Relative death rate of stubble/pseudostem
    'LERGB',  # LERGB,  # mm d-1 Â°C-1, # Leaf elongation slope generative
    'RDRROOT',  # RDRROOT,  # d-1, # Relatuive death rate of root mass CRT
    'DAYLA',  # DAYLA,  # -, # DAYL above which growth is prioritised over storage
    'DAYLRV',  # DAYLRV,  # -, # DAYL at which vernalisation is reset
    'FCOCRESMN',  # FCOCRESMN,  # -, # Minimum concentration of reserves in aboveground biomass as fraction of COCRESMX
    'KCRT',  # KCRT,  # gC m-2, # Root mass at which ROOTD is 67% of ROOTDM
    'VERNDI',  # VERNDI,  # d, # Initial value of cumulative vernalisation days
    'LERVA',  # LERVA,  # Â°C, # Leaf elongation intercept vegetative
    'LERVB',  # LERVB,  # mm d-1 Â°C-1, # Leaf elongation slope vegetative
    'LERGA',  # LERGA,  # Â°C, # Leaf elongation intercept generative
    'RDRTILMIN',  # RDRTILMIN,  # d-1, # Background relative rate of tiller death
    'RDRHARVMAX',  # RDRHARVMAX,  # d-1, # Maximum relative death rate due to harvest
    'FGRESSI',  # FGRESSI,  # -, # CRES sink strength factor
    'HARVFRD',  # HARVFRD,  # -, # Relative harvest fraction of CLVD
    'EBIOMAX',  # EBIOMAX,  # -, # Earthworm biomass max
    'KBASAL',  # KBASAL,  # ?, # Constant at half basal area
    'RDRWMAX',  # RDRWMAX,  # d-1, # Maximum death rate due to water stress
    'BASALI',  # BASALI,  # -, # Grass basal area
    'ABASAL',  # ABASAL,  # d-1, # Grass basal area response rate
    'TVERNDMN',  # TVERNDMN,  # d, # Minimum vernalisation days
    'DAYLGEMN',  # DAYLGEMN,  # -, # Minimum daylength growth effect
    'TRANRFCR',  # TRANRFCR,  # -, # Critical water stress for tiller death
    'DELE',  # DELE,  # -, # Litter disappearance due to earthworms
    'DELD',  # DELD,  # -, # Litter disappearance due to decomposition

)

t = set(site_param_keys)
t.update(plant_param_keys)
assert t == set(param_keys), 'missing params {} must be present in site or plant list'.format(set(param_keys) - t)
