"""
 Author: Matt Hanson
 Created: 14/08/2020 8:53 AM
 """

_param_keys = (  # 99.9% sure that this is in the correct order as defined by set_params.f95
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
    'DAYLB',  # DAYLB,  # d d-1, # Day length below which DAYLGE becomes 0 and phenological stage is reset to zero (must be < DLMXGE)
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
    'PHENCR',  # PHENCR,  # -, # Phenological stage above which elongation and appearance of leaves on elongating tillers decreases
    'PHY',  # PHY,  # Â°C d, # Phyllochron
    'RDRSCO',  # RDRSCO,  # d-1, # Increase in relative death rate of leaves and non-elongating tillers due to shading per unit of LAI above LAICR
    'RDRSMX',  # RDRSMX,  # d-1, # Maximum relative death rate of leaves and non-elongating tillers due to shading
    'RDRTEM',  # RDRTEM,  # d-1 Â°C-1, # Proportionality of leaf senescence with temperature
    'RGENMX',  # RGENMX,  # d-1, # Maximum relative rate of tillers becoming elongating tillers
    'ROOTDM',  # ROOTDM,  # m, # Initial and maximum value rooting depth
    'RRDMAX',  # RRDMAX,  # m d-1, # Maximum root depth growth rate
    'RUBISC',  # RUBISC,  # g m-2 leaf, # Rubisco content of upper leaves
    'LSHAPE',  # SHAPE,  # -, # Area of a leaf relative to a rectangle of same length and width (must be < 1)
    'SIMAX1T',  # SIMAX1T,  # gC tiller-1 d-1, # Sink strength of small elongating tillers
    'SLAMAX',  # SLAMAX,  # m2 leaf gC-1, # Maximum SLA of new leaves (Note unusual units!)
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
    'IRRIGF',  # fraction # fraction of soil capacity to irrigate to!  Relative irrigation rate
    'doy_irr_start', #doy>=doy_irr_start has irrigation applied if needed
    'doy_irr_end',  #doy <= doy_irr_end has irrigation applied


)

_matrix_weather_keys = (  # I am 99% sure of the correct order
    'year',  # e.g. 2002
    'doy',  # day of year 1 - 356 or 366 for leap years
    'radn',  # daily solar radiation (MJ/m2)
    'tmin',  # daily min (degrees C)
    'tmax',  # daily max (degrees C)
    'rain',  # sum daily rainfall (mm)
    'pet',  # Potential evapotransperation (mm), suggest priestly
    'max_irr',  # maximum irrigation available (mm/d)
)

_days_harvest_keys = (
    # -1 for these seems to set as a null value, to account for the 100 max harvests days
    'year',  # e.g. 2002
    'doy',  # day of year 1 - 356 (366 for leap year)
    'percent_harvest',  # percent of harvest as an integer 0-100,

)

_out_cols = (
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

    'DM',  # Ryegrass Mass, #  (kg DM ha-1)
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
    'YIELD',  # PRG Yield, #  (tDM ha-1)
    'BASAL',  # Basal Area, #  (%)
    'GTILV',  # Till. Birth, #  (till m-2 d-1)
    'DTILV',  # Till. Death, #  (till m-2 d-1)
    'FS',  # Site Filling, #  (till leaf-1)
    'IRRIG',  # mm d-1 Irrigation
)

