# BASGRA_NZ

BASGRA or The BASic GRAssland model is a simple pasture growth model. This version, BASGRA_NZ has been specifically
modified for use within New Zealand.

BASGRA_NZ_PY is a python wrapper for the
[BASGRA_NZ](https://github.com/woodwards/basgra_nz/tree/master/model_package/src) fortran code, contains several new
features and is the first version of BASGRA to have purpose built tests to ensure that all changes can be made in a
backwards compatible fashion (with some argument changes).

The BASGRA NZ project tracks modifications to BASGRA for application to perennial ryegrass in New Zealand conditions.
The test data comes from the Seed Rate Trial 2011-2017. Modifications to BASGRA were necessary to represent this data.

see outstanding_issues.txt for original info on the model see docs for information on the changes made by Simon
Woodward, in
[Woodward, 2020](https://onlinelibrary.wiley.com/doi/abs/10.1111/gfs.12464)

BASGRA_NZ_PY is modified from Simon Woodward's
[BASGRA_NZ](https://github.com/woodwards/basgra_nz/tree/master/model_package/src)
which is in turn modified from [BASGRA](https://github.com/davcam/BASGRA)

This repo diverged from Simon Woodward's
[BASGRA_NZ](https://github.com/woodwards/basgra_nz/tree/master/model_package/src) as of August 2020, efforts will be
made to incorporate further updates, but no assurances

## Table of Contents

- [Python Implementation](#python-implementation)
- [package installation](#package-installation)
- [Fortran Installation](#fortran-installation)
- [Fortran compilation](#fortran-compilation)
- [new features implemented from Simon Woodward's BASGRA](#new-features-implemented-from-simon-woodward-s-basgra)
    * [model documentation resources](#model-documentation-resources)
    * [Maximum simulation length](#maximum-simulation-length)
    * [Calender](#Calender)
    * [Resource requirements](#resource-requirements)
    * [irrigation triggering and demand modelling (v2.0.0+)](#irrigation-triggering-and-demand-modelling--v200--)
        + [New Irrigation Process](#new-irrigation-process)
        + [New irrigation input/outputs](#new-irrigation-input-outputs)
        + [How to run so that the results are backwards compatible with versions before V2.0.0](#how-to-run-so-that-the-results-are-backwards-compatible-with-versions-before-v200)
    * [Harvest management and scheduling (v3.0.0+)](#harvest-management-and-scheduling--v300--)
        + [New Harvest processes](#new-harvest-processes)
            - [Automatic harvesting process](#automatic-harvesting-process)
            - [Manual harvesting process](#manual-harvesting-process)
        + [New Harvest inputs/outputs](#new-harvest-inputs-outputs)
        + [How to run so that the results are backwards compatible with versions before V3.0.0](#how-to-run-so-that-the-results-are-backwards-compatible-with-versions-before-v300)
    * [Re-seeding module (V4.0.0+)](#re-seeding-module--v400--)
        + [Reseed process](#reseed-process)
        + [New re-seed inputs/outputs](#new-re-seed-inputs-outputs)
        + [How to run so that the results are backwards compatible with versions V3.0.0 -](#how-to-run-so-that-the-results-are-backwards-compatible-with-versions-v300--)
    * [passing external soil moisture to model (V5.0.0+)](#passing-external-soil-moisture-to-model--v500--)
        + [How to run so that the results are backwards compatible with versions V4.0.0 -](#how-to-run-so-that-the-results-are-backwards-compatible-with-versions-V400--)
    * [Irrigation water storage (V6.0.0+)](#Irrigation-water-storage-(V6.0.0+))
        + [Irrigation storage process](#Irrigation-storage-process)
        + [new inputs/outputs](#new-inputs/outputs)
        + [How to run so that the results are backwards compatible with versions V5.0.0 -](#How-to-run-so-that-the-results-are-backwards-compatible-with-versions-V5.0.0-)

- [python developments](#python-developments)
    * [supporting functions](#supporting-functions)
    * [testing regime and examples](#testing-regime-and-examples)
- [Input and output parameter definitions](#input-and-output-parameter-definitions)
    * [Days Harvest Keys description](#days-harvest-keys-description)
    * [Matrix weather keys where pet is passed description](#matrix-weather-keys-where-pet-is-passed-description)
    * [Matrix weather keys where pet is calculated via penman description](#matrix-weather-keys-where-pet-is-calculated-via-penman-description)
    * [Site Parameters description](#site-parameters-description)
    * [Plant Parameters description](#plant-parameters-description)
    * [output description](#output-description)
- [References](#References)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with
markdown-toc</a></i></small>

## Python Implementation

BASGRA_NZ requires python 3.7 or less (3.8 handles DLLs more securely but this causes some faults)
required packages:

* pandas
* numpy
* matplotlib

to install this general environment via conda: conda create --name basgranz python=3.7 numpy pandas matplotlib or a
fixed anaconda .yml library can be found in the environment.yml file

## package installation

BASGRA_NZ_PY can only be installed locally from a github pull and addition to your PYTHONPATH

this installs both the python wrapper and the source fortran code. at present a fortran installation is required.

## Fortran Installation

At present BASGRA_NZ_py requires fortran 64 and assumes the use of gfortran64. It is beyond the scope of this readme to
detail how to install fortran, but general instructions can be found in this
[youtube video](https://www.youtube.com/watch?v=wGv2kGl8OV0)
WARNING the installation in this video is 32Bit

This repo was developed and tested with gfortran 64 4.8.1 which can be
[downloaded here](https://sourceforge.net/projects/mingwbuilds/files/host-windows/releases/4.8.1/64-bit/threads-posix/seh/x64-4.8.1-release-posix-seh-rev5.7z/download)

## Fortran compilation

At present BASGRA_NZ_py requires fortran and requires the user to compile the fortran code. The compilation code can be
found in the following .bat file: fortran_BASGRA_NZ/compile_BASGRA_gfortran.bat The python wrapper will attempt to run
the compilation bat if the DLL it required does not exist.

## new features implemented from Simon Woodward's BASGRA

A number of new features where necessary for futher modeling work. Specially more generalized irrigation and harvest
management. This required changes to the fortran code, but tests were put in place to ensure backwards compatibility (
with some argument changes) to
[Simon Woodward's BASGRA_NZ](https://github.com/woodwards/basgra_nz/tree/master/model_package/src) as of August 2020.

### model documentation resources

This readme is the documentation of all new features to basgra_nz_py, but the documentation of the previous features are
in fortran_BASGRA_NZ/docs

### Maximum simulation length

At present the maximum simulation length is set explicitly within the fortran code in the environment.f95.  
It is set to 100 years (NMAXDAYS = 36600). This was set at this length to allow long term climate change simulations,
without expending too many resources. Note that internally the python code must make the weather matrix length to
nmaxdays.

### Calender

BASGRA_NZ_PY can be run with either the standard gregorian calendar (e.g. with leap years) or on a 365 day calendar In
both cases BASGRA_NZ_PY runs checks to ensure that there are no missing or additional days in the simulation relative to
the expected calender.

### Resource requirements

BASGRA is fast!  The following baseline test are provided in supporting_functions/check_resource_use.py:

* BASGRA took 1.585375e-01 seconds to run run_example_basgra which has 2192 sim days
* BASGRA took 7.232549e-05 seconds per realisation day to run run_example_basgra
* BASGRA took 7.072114e-01 seconds to run support_for_memory_usage which has 36600 sim days
* BASGRA took 1.932272e-05 seconds per realisation day to run support_for_memory_usage

BASGRA is relatively light weight

* run_example_basgra which has 2192 sim days required a max of c. 9 mb of memory
* run support_for_memory_usage which has 36600 sim days required a max of c. 45 mb of memory
* memory tests were run with [memory_profiler 0.58.0](https://pypi.org/project/memory-profiler/)
  to rerun these tests (supporting_functions/test_memory_use.py) requires installation of the memory profiler

### irrigation triggering and demand modelling (v2.0.0+)

#### New Irrigation Process

Irrigation modelling was developed to answer questions about pasture growth rates in the face of possible irrigation
water restribtions; therefore the irrigation has been implemented as follows:

* if the day of year is within the irrigation season (doy in doy_irr)
    * if the fraction of soil water (e.g. WAL/WAFC) including the time step modification to the soil water content
      (e.g. transpiration, rainfall, etc) are BELOW the trigger for that day
        * irrigation is applied at a rate = max(IRRIGF* amount of water needed to fill to irrigation target * field
          capacity, max_irr on the day)

This modification includes bug fixes that allowed irrigation to be negative.

#### New irrigation input/outputs

There is a new input variable: doy_irr, which is the days that irrigation can occur(1d array)

a number of inputs have been added to parameters:

* 'IRRIGF', # fraction # fraction of irrigation to apply to bring water content up to field capacity, this was
  previously set within the fortran code
* 'irr_frm_paw', # are irrigation trigger/target the fraction of profile available water (1/True or # the fraction of
  field capacity (0/False).

new columns has been added to matrix_weather:

* 'max_irr', # maximum irrigation available (mm/d)
* 'irr_trig', # fraction of PAW/field (see irr_frm_paw) capacity at or below which irrigation is triggered (fraction
  0-1) e.g. 0.5 means that irrigation will only be applied when soil water content is at 1/2 field capacity
  (e.g. water holding capacity)
* 'irr_targ', # fraction of PAW/field (see irr_frm_paw) capacity to irrigate to (fraction 0-1)

New outputs have been added:

* 'IRRIG':  # mm d-1 Irrigation,
* 'WAFC': #mm # Water in non-frozen root zone at field capacity
* 'IRR_TARG', # irrigation Target (fraction of field capacity) to fill to, also an input variable
* 'IRR_TRIG', # irrigation trigger (fraction of field capacity at which to start irrigating
* 'IRRIG_DEM', # irrigation irrigation demand to field capacity * IRR_TARG # mm

#### How to run so that the results are backwards compatible with versions before V2.0.0

To run the model in the original (no irrigation fashion) set both max_irr and irr_trig to zero, also set doy_irr = [0]

### Harvest management and scheduling (v3.0.0+)

As of version v3.0.0 harvest management has changed significantly to allow many more options for harvest management

Importantly days_harvest is now a float array instead of an integer array as was the case in v.2.0.0

#### New Harvest processes

harvesting has been changed to allow:

* automatic harvesting
* time varient harvestable dry matter triggers
* time varient harvestable dry matter target (e.g. dry matter is harvested to the target)
* time varient fixed weight harvesting
* time varient allowing weed species to provide some fraction of the rye grass production

##### Automatic harvesting process

In the automatic harvesting process

1. a harvest trigger is set for each time step
2. at each time step harvestable Rye grass dry matter is calculated and reported by DMH_RYE = ((CLV+CST+CSTUB)/0.45 +
   CRES/0.40 + (CLVD * HARVFRD / 0.45)) * 10.0
2. at each time step harvestable weed species dry matter is calculated and reported by DMH_WEED = WEED_DM_FRAC *
   DMH_RYE/BASAL * (1-BASAL)
3. total harvestable dry matter is calculated and reported by DMH_RYE + DMH_WEED
4. if the total harvestable dry matter is >= the dry matter target for that time step then harveting occurs
5. the amount of Dry matter to remove is calculated
    1. if fixed_removal flag then the amount to remove is defined by DM_RM = HARV_TARG * FRAC_HARV
    2. if not fixed_removal then the amount to remove is defined by  
       DM_RM = ((DMH_RYE + DMH_WEED) - HARV_TARG) * FRAC_HARV
5. An initial fraction of dry mater to remove is calculated, HARVFRIN = DM_RYE_RM/DMH_RYE Note that this means that the
   weed species dry matter harvested is not removed from the rye grass model
6. iff 'opt_harvfrin'= True, the harvest fraction to remove is estimated by brent zero optimisation. This step is
   recommended as the harvest fraction is non-linearly related to the harvest as the stem and reserve harvest fraction
   is related to a power function. In some test runs without estimation, target 500kg removal has actually removed c.
   1000kg
7. harvesting then progresses as per V2.0.0

##### Manual harvesting process

As per automatic harvesting, however the data frame is reshaped within the python code so that the row count is equal to
n days. all indexes where manual harvesting will not occur have the 'harv_trig' set to -1 so that no harvesting will
occur

DMH_WEED or the harvestable dry matter from weed species is calculated at every time step. as such 'weed_dm_frac' must
be defined sensibly for every day of the simulation. Internally the python wrapper to BASGRA_NZ_PY uses
pd.Series.fillna(method='ffill') or fills the missing values with the last valid values. if 'weed_dm_frac' is not set
for the first day of the series a warning is issued and the first valid value is used to fill the values before the
first valid value.

Note that if the dry matter value is below the trigger value for a given manual time step no harvesting will occur.

#### New Harvest inputs/outputs

New input parameters

* 'fixed_removal', # float boolean(1.0=True, 0.0=False) defines if auto_harv_targ is fixed amount or amount to harvest
  to
* 'opt_harvfrin', # float boolean(1.0=True, 0.0=False) if True, harvest fraction is estimated by brent zero optimisation
  if false, HARVFRIN = DM_RYE_RM/DMH_RYE. As the harvest fraction is non-linearly related to the harvest, the amount
  harvested may be significantly greater than expected depending on CST. We would suggest always setting 'opt_harvfrin'
  to True unless trying to duplicate a previous run done under v2.0.0-

New outputs

* 'RYE_YIELD', # PRG Yield from rye grass species, #  (tDM ha-1)  note that this is the actual amount of material that
  has been removed
* 'WEED_YIELD', # PRG Yield from weed (other) species, #  (tDM ha-1)  note that this is the actual amount of material
  that has been removed
* 'DM_RYE_RM', # dry matter of Rye species harvested in this time step (kg DM ha-1) Note that this is the calculated
  removal but if 'opt_harvfrin' = False then it may be significantly different to the actual removal, which is show by
  the appropriate yield variable
* 'DM_WEED_RM', # dry matter of weed species harvested in this time step (kg DM ha-1) Note that this is the calculated
  removal but if 'opt_harvfrin' = False then it may be significantly different to the actual removal, which is show by
  the appropriate yield variable
* 'DMH_RYE', # harvestable dry matter of # species, includes harvestable fraction of dead (HARVFRD) (kg DM ha-1)
* 'DMH_WEED', # harvestable dry matter of # specie, includes harvestable fraction of dead (HARVFRD) (kg DM ha-1)
* 'DMH', # harvestable dry matter = DMH_RYE + DMH_WEED  (kg DM ha-1)

New format for harvest data frame,

* Datatype transition from int(v2.0.0-) to float(v3.0.0)
* Two allowable data frame lengths:
    * Manual harvest (n x 6 data frame, where n=number of harvest events), python auto_harvest=False
    * Automatic harvest (m x 6 data frame, where m=ndays), python auto_harvest=True
* Note the fixed harvest size requirements of 100 days were fixed in V1.0.0
* Data frame columns
    * 'year', # e.g. 2002
    * 'doy', # day of year 1 - 356 (366 for leap year)
    * 'frac_harv', # fraction (0-1) of material above target to harvest to maintain 'backward capabilities' with v2.0.0
    * 'harv_trig', # dm above which to initiate harvest, if trigger is less than zero no harvest will take place
    * 'harv_targ', # dm to harvest to or to remove depending on 'fixed_removal'
    * 'weed_dm_frac', # fraction of dm of ryegrass to attribute to weeds

#### How to run so that the results are backwards compatible with versions before V3.0.0

* 'fixed_removal' = 0
* 'opt_harvfrin' = 0
* manual harvest (python auto_harvest=False)
* set harvest data frame as follows:
    * 'year', as per v2.0.0-
    * 'doy', as per v2.0.0-
    * 'frac_harv', as per v2.0.0- percent_harvest/100, note that fraction harvest is now a float value
    * 'harv_trig', as 0
    * 'harv_targ', as 0
    * 'weed_dm_frac' as 0

### Re-seeding module (V4.0.0+)

At times during a long term simulations weather events can push the BASAL coverage of the rye grass to well below the
normal amount for the simulation. The BASGRA model will slowly increase BASAL coverage, however this may not very
realistic. Farmers may choose to re-seed pasture following an infrequent event.

#### Reseed process

The process very simplistic and does not model the physiological processes of seed germination and young plant growth.
it simply allows the following parameters to be re-set and initiates a delay for harvesting:

* BASAL
* LAI
* TILG2
* TILG1
* TILV

1. on each day check the internal BASAL parameter against the appropriate daily value for 'reseed_trig'
   (the reseed trigger), if BASAL is <= 'reseed_trig', then reseed otherwise simply pass. if reseed_trig <0 then
   passes (flag for no reseed)
2. set BASAL to 'reseed_basal'
3. set the Phenological stage (PHEN) to 0
3. set [LAI, TILG2, TILG1, TILV, CLV, CRES, CST, CSTUB] to either the user defined parameter 'reseed_{var}' or keep at
   current state value when the user defined parameter 'reseed_{var}' <0.
4. set a user defined delay in harvesting ('reseed_harv_delay'), by setting the next n days harv_trig to -1

#### New re-seed inputs/outputs

In order to very simply model this behaviour a new re-seed module was added. This module requires 5 new parameters and 2
new inputs in the harvest matrix, and produces 1 new output

the parameters are:

* 'reseed_harv_delay':  number of days to delay harvest after reseed, must be >=1 and an integer
  (value not type, within 1e-5)
* 'reseed_LAI': >=0 the leaf area index to set after reseeding, if < 0 then simply use the current LAI
* 'reseed_TILG2': Non-elongating generative tiller density after reseed if >=0 otherwise use current state of variable
* 'reseed_TILG1': Elongating generative tiller density after reseed if >=0 otherwise use current state of variable
* 'reseed_TILV': Non-elongating tiller density after reseed if >=0 otherwise use current state of variable
* 'reseed_CLV', # Weight of leaves after reseed if >= 0 otherwise use current state of variable
* 'reseed_CRES', # Weight of reserves after reseed if >= 0 otherwise use current state of variable
* 'reseed_CST', # Weight of stems after reseed if >= 0 otherwise use current state of variable
* 'reseed_CSTUB', # Weight of stubble after reseed if >= 0 otherwise use current state of variable

The new columns in the harvest matrix are:

* 'reseed_trig': (-1 or 0 to 1) when BASAL <= reseed_trig, trigger a reseeding. if <0 then do not reseed
* 'reseed_basal': (0 to 1) set BASAL = reseed_basal when reseeding.

The new output is:

* 'RESEEDED': reseeded flag, if ==1 then the simulation was reseeded on this day, if 0 then not reseeded

#### How to run so that the results are backwards compatible with versions V3.0.0 -

* set all 'reseed_trig' in the harvest matrix to -1.
* set all 'reseed_basal' to 0 (can be set to anything between 0-1 as it will not be used)
* set 'reseed_harv_delay' to 1 (to avoid python assertion error)
* all other reseed parameters (reseed_{var}) must be set, but they can all be safely set to -1

### passing external soil moisture to model (V5.0.0+)

As of V5.0.0 it is possible to pass time series external soil moisture data into BASGRA to use rather than the internal
soil moisture model. Soil moisture can be passed as a fraction (0-1) of either profile available water (PAW) or field
capacity

Note V5.0.0 + has a slight change to fix an off by one error that occurs with PAW. Now PAW will match WAL

To do this:

* set 'pass_soil_moist' to 1
* set matrix_weather.max_irr to the soil moisture fraction
* set 'irr_frm_paw' to 1 if soil moisture is fraction of PAW or 0 is soil moisture is a fraction of field capacity

#### How to run so that the results are backwards compatible with versions V4.0.0 -

Note PAW will not be identical with previous versions as Note V5.0.0 + has a slight change to fix an off by one error
that occurs with PAW. Now PAW will match WAL Otherwise:

* set 'pass_soil_moist' to 0
* set max_irr as normal

### Irrigation water storage (V6.0.0+)

As of V6.0.0 it is possible to model local storage of water for irrigation in addition to a larger scheme irrigation
system. We define a scheme irrigation as something which is not volume limited, but may be limited based on other 
factors (e.g. restrictions in a river). Storage irrigation in contrast is irrigation that is only limited by volume. 
Storage is turned on by setting parameter *'use_storage'* to 1. 

#### Irrigation storage process

The storage water balance and irrigation process occurs in the following order

1. Calculate non-scheme inflows to storage
   
        Non-scheme inflows are defined as runoff and a full refill at a (one) certain day of the year.  The latter is 
        provided for convenience if the modeller wishes to assume that the storage is always full at a certain time of
        the year. The runoff component can either be calculated internally (when 'runoff_from_rain' == 1) or can be 
        specified by the modeller (when 'runoff_from_rain' == 0, e.g. from an external rainfall runoff model).  If 
        The runoff is specified by the modeller then the daily values are passed via the matrix_weather parameter
        'external_inflow'. 

        The internal calculation of rainfall runoff is very simplistic the user specified a catchment area 
        (parameter 'runoff_area') of which a user specified fraction of the rainfall (parameter 'runoff_frac') 
        runs off to storage.

2. Calculate non-irrigation outflows from storage 

        The non-irrigation outflows include a user defined leakage rate, fixed removal of storage water for other
        purposes and finally evaporation from the storage body (NOT IMPLMENTED). 
   
        Leakage from the storage body is defined as a fixed user specified rate ('stor_leakage') which will be 
        removed daily.  There is no head leakage relationship defined in the model
   
        A set amount of water can be removed from the storage on any given day (e.g. for stock water use). 
        This is achieved by setting the matrix_weather parameter 'external_inflow' to a negative value.  This feature
        is not avalible if runoff is calculated internally (when *'runoff_from_rain' == 0)

        Finally, evaporation is planned to be implmented; however it is currently set to 0 as a place holder for
        further development.

3. Calculate irrigation and irrigate from scheme

        Irrigation from the scheme is handled as per version V2.0.0+  (if soil water is below trigger, calculate 
        irrigation demand, check water avalibility and then irrigate up to the target) with one minor modification. 
        The maximum irrigation that can be applied on any given day is controlled by the new parameter 'abs_max_irr' 
        this is envisioned as a limitation of equipment rather than water that of water availability. The amount 
        of water that is to irrigate from a scheme on any given day is defined by the matrix_weather 
        parameter 'max_irr'.  Note that if 'max_irr' is set higher than 'abs_max_irr' then the water is 
        not available for irrigation, but depending on the parameterisation of the model may be available to 
        re-fill storage. If there is no scheme available (e.g. isolated storage from runoff), scheme based 
        irrigation can be effectively turned off by setting the matrix_weather parameter 'max_irr' to zero and 
        passing dummy values to matrix_weather parameters 'irr_trig', 'irr_targ'

4. Calculate irrigation and irrigate from storage

        If storage is implemented ('use_storage' = 1), storage can either be used in one of two modes:
          1. to make up the difference between the weather_matrix parameter 'max_irr' and the irrigation demand 
             to the target (calculated in step 3) to the extent possible depending on storage water avalibility.
          2. calculating a novel storage demand AFTER SHEME IRRIGATION IS APPLIED. This demand is calculated as
             per the scheme demand, but from the matrix_weather parameters 'irr_trig_store' and 'irr_targ_store'
             it is important to recall that this demand is calculated after scheme based irrigation has been applied
             which means that the soil moisture may be below the storage trigger value before scheme irrigation, but
             no storage irrigation is applied because the scheme irrigation increased the soil water content above
             the trigger.
        To implment mode 1 the parameter 'calc_ind_store_demand' is set to 0, mode 2 is implemented 
        when 'calc_ind_store_demand' = 1

        if storage irrigation occurs, then as much storage as is avalible is applied to reach the soil moisture target
        or the maximum irrigation rate ('abs_max_irr'), whichever is less. Note that a volume of storage can be 
        held in reserve (e.g. for stock water).  This volume is set in parameter 'stor_reserve_vol'.

        Finally storage irrigation scheme ineffciency can be implmented with parameter 'stor_irr_ineff', which 
        defines the fraction of the applied irrigation volume that is needed to compensate for losses in the 
        process of irrigation.  a value of 0 means a perfecly effcient system, while a value of 1 means that for 
        every m3 of water applied in irrigation from storage, 2 m3 is removed from the storage resevouir.

5. refill storage from scheme (if allowed)

        The storage resevouir can implmented to be refilled by the excess water from the scheme.  This process is 
        implmented in a simple way:
            1. calculate the amount of excess water
            2. if the amount of water is greater than the minimum refill parameter ('stor_refill_min')
            3. then refill the storage with the remaining water.
            4. ineffciencies in the refilling process can be implmented with parameter 'stor_refill_losses' where
               the volume that enters the storage resevouir is equal to 'stor_refill_losses' * the excess water.

all components of the storage water budget is saved to the output. 

#### new inputs/outputs

*parameter additions*

**Key**|**Unit**|**Description**
| --- | --- | ---|
'use_storage' |sudo boolean 1=True, 0=False   | whether or not to include storage in the model
'runoff_from_rain' |sudo boolean 1=True, 0=False   | if True then use a fraction of rainfall, otherwise proscribed refill data from an external model
'calc_ind_store_demand' |sudo boolean 1=True, 0=False   | if true then calculate storage demand after scheme irrigation from triggers, targets, if false then calculate storage demand as the remaining demand after scheme irrigation,
'stor_full_refil_doy' |day of year (1-366)   | the day of the year (0-366) when storage will be set to full. set to -1 to never fully refill storage
'abs_max_irr' | mm | the maximum irrigation that can be applied per day (e.g. equipment limits) mm/day note that if matrix weather prescribed max_irr for a given day is larger then abs_max_irr, that water may still be avalible to refill storage.
'irrigated_area' |ha | the area irrigated (ha)
'I_h2o_store_vol' |fraction | initial h2o storage fraction
'h2o_store_max_vol' | m<sup>3</sup>| h2o storage maximum volume (m3)
'h2o_store_SA' | m<sup>2</sup> | h2o storage surface area (m2)
'runoff_area' |m<sup>2</sup> | the area that can provide runoff to the storage (ha)
'runoff_frac' | fraction | the fraction of precipitation that becomes runoff to recharge storage (0-1, unit less)
'stor_refill_min' | mm | the minimum amount of excess irrigation water that is needed to refill storage (mm/day)
'stor_refill_losses' |fraction | the losses incurred from re-filling storage from irrigation scheme (0-1)
'stor_leakage' |m<sup>3</sup> | the losses from storage to leakage static (m3/day)
'stor_irr_ineff' |fraction | the fraction of irrigation water that is lost when storage is used for irrigation (e.g. 0 means a perfectly efficient system, 1 means that 2x the storage volume is needed to irrigate x volume) unit less
'stor_reserve_vol'|m<sup>3</sup>| the volume of storage to reserve (e.g. irrigation is cutoff at this volume)

*matrix_weather additions*

**Key**|**Unit**|**Description**
| --- | --- | ---|
'irr\_trig\_store'|fraction|the irrigation trigger value (if calc_ind_store_demand) for the storage based irrigation either fraction of PAW or field capacity
'irr\_targ\_store'|fraction| the irrigation target value (if calc_ind_store_demand) for the storage based irrigation either fraction of PAW or field capacity
'external\_inflow'|m<sup>3</sup>| only used if not runoff_from_rain, the volume (m3) of water to add to storage (allows external rainfall runoff model for storage management) can be negative


*output additions*

**Key**|**Unit**|**Description**
| --- | --- | ---|
'irrig_dem_store'| mm | irrigation demand from storage (mm)
'irrig_store'| mm | irrigation applied from storage (mm)
'irrig_scheme'| mm | irrigation applied from the scheme (mm)
'h2o_store_vol'| m<sup>3</sup>| volume of water in storage (m3)
'h2o_store_per_area'| mm | h2o storage per irrigated area (mm)
'IRR_TRIG_store'|fraction | irrigation trigger for storage (fraction paw/FC), input, only relevant if calc_ind_store_demand
'IRR_TARG_store'|fraction | irrigation target for storage (fraction paw/FC), input, only relevant if calc_ind_store_demand
'store_runoff_in'| m<sup>3</sup>| storage budget in from runoff or external model (m3)
'store_leak_out'| m<sup>3</sup> | storage budget out from leakage (m3)
'store_irr_loss'| m<sup>3</sup> | storage budget out from losses incurred with irrigation (m3)
'store_evap_out'| m<sup>3</sup> | storage budget out from evaporation (NOTIMPLEMENTED) (m3)
'store_scheme_in'| m<sup>3</sup> | storage budget in from the irrigation scheme (m3)
'store_scheme_in_loss'| m<sup>3</sup> | storage budget out losses from the scheme to the storage basin (m3)
'external_inflow',| m<sup>3</sup> | input value external inflow (m3) kept for full water budget of storage
'store_overflow', | m<sup>3</sup> |water that could have been added to storage (including losses), but was not as storage was full (m3)


#### How to run so that the results are backwards compatible with versions V5.0.0 -

 * set parameter 'use_storage' to 0, which turns off storage
 * set parameter 'abs_max_irr' to the max(matrix_weather\['max_irr']) or greater
   
You will also need to pass dummy values to:

**Parameter location**|**Parameter name**|**Suggested dummy value**
| --- | --- | ---|
 parameter| 'runoff_from_rain'| 1
 parameter| 'calc_ind_store_demand'| 0
 parameter| 'stor_full_refil_doy'| -1
 parameter| 'irrigated_area'| 0
 parameter| 'I_h2o_store_vol'| 0
 parameter| 'h2o_store_max_vol'| 0
 parameter| 'h2o_store_SA'| 0
 parameter| 'runoff_area'| 0
 parameter| 'runoff_frac'| 0
 parameter| 'stor_refill_min'| 0
 parameter| 'stor_refill_losses'| 0
 parameter| 'stor_leakage'| 0
 parameter| 'stor_irr_ineff'| 0
 matrix_weather|'irr_trig_store'|0
 matrix_weather|'irr_targ_store'|1
 matrix_weather|'external_inflow'|0

## python developments

### supporting functions

there are several supporting functions developed within basgra_nz_py. These are not all documented in this readme;
however there are decent docstrings. these include:

* conversion from RH to vapour pressure and wind speed to wind speed at 2m (conversions.py)
* plotting multiple results either on monthly time steps or for the duration of the run (plotting.py)
* access to the mean parameters that resulted from Woodward 2020's inverse calibration (woodward_2020_params.py)
    * Parameters are available for the Scott Farm in the Waikato, Jordan Valley Farm in Northland, and the Lincoln Test
      Farm in Canterbury.
    * Scott Farm and Jordan Valley Farm are dryland systems, while Lincoln Test Farm is irrigated.
    * Plant parameters were calibrated for all three farms, while site parameters were calibrated for each specific
      site.
    * [see woodward, 2020](https://onlinelibrary.wiley.com/doi/abs/10.1111/gfs.12464) for more details.
    * Note that the parameters provided here provide the correct parameters to run the model in a way that is consistent with version V1.0.0 

### testing regime and examples

In order to ensure that future changes can be made backwards compatible with previous runs there are a suite of test in
check_basgra_python/test_basgra_python.py. These tests are not yet implemented in a framework; however simply running
the test_basgra_python.py will run all of the testing functions. These functions can also be used as examples.

## Input and output parameter definitions

### Days Harvest Keys description

|**Key**|**Unit**|**Description**|
| --- | --- | ---|
|'year'| |year e.g. 2002|
|'doy'| |day of year 1 - 356 (366 for leap year)|
|'frac\_harv'|fraction|fraction (0-1) of material above target to harvest to maintain 'backward capabilities' with v2.0.0|
|'harv\_trig'|kgDM/ha|dm above which to initiate harvest if trigger is less than zero no harvest will take place|
|'harv\_targ'|kgDM/ha|dm to harvest to or to remove depending on 'fixed\_removal'|
|'weed\_dm\_frac'|fraction|fraction of dm of ryegrass to attribute to weeds|
|'reseed\_trig'|fraction|when BASAL <= reseed\_trig trigger a reseeding. if <0 then do not reseed|
|'reseed\_basal'|fraction|set BASAL = reseed\_basal when reseeding.|

### Matrix weather keys where pet is passed description

**Key**|**Unit**|**Description**
| --- | --- | ---|
'year'| year |e.g. 2002
'doy'| day|day of year 1 - 356 or 366 for leap years
'radn'|MJ/m2|daily solar radiation
'tmin'|degrees C|daily min
'tmax'|degrees C|daily max
'rain'|mm|sum daily rainfall
'pet'|mm|priestly/penman evapotransperation
'max\_irr'|mm/d|maximum irrigation available when 'pass_soil_moist' is False or the fraction (0-1) PAW/Field capacity to be passed to the model when 'pass_soil_moist' is True, see 'pass_soil_moist' for more details
'irr\_trig'|fraction|fraction of PAW/field (see irr\_frm\_paw) at or below which irrigation is triggered e.g. 0.5 means that irrigation will only be applied when soil water content is at 1/2 of the appropriate variable
'irr\_targ'|fraction|fraction of PAW/field (see irr\_frm\_paw) to irrigate up to.
'irr\_trig\_store'|fraction|the irrigation trigger value (if calc_ind_store_demand) for the storage based irrigation either fraction of PAW or field capacity
'irr\_targ\_store'|fraction| the irrigation target value (if calc_ind_store_demand) for the storage based irrigation either fraction of PAW or field capacity
'external\_inflow'|m<sup>3</sup>| only used if not runoff_from_rain, the volume (m3) of water to add to storage (allows external rainfall runoff model for storage management) can be negative

### Matrix weather keys where pet is calculated via penman description

**Key**|**Unit**|**Description**
| --- | --- | ---|
'year'| |e.g. 2002
'doy'| |day of year 1 - 356 or 366 for leap years
'radn'|MJ/m2|daily solar radiation
'tmin'|degrees C|daily min
'tmax'|degrees C|daily max
'rain'|mm|sum daily rainfall
'vpa'|kPa|vapour pressure
'wind'|m/s|mean wind speed at 2m
'max\_irr'|mm/d|maximum irrigation available (from scheme) when 'pass_soil_moist' is False or the fraction (0-1) PAW/Field capacity to be passed to the model when 'pass_soil_moist' is True, see 'pass_soil_moist' for more details
'irr\_trig'|fraction|fraction of PAW/field (see irr\_frm\_paw) at or below which irrigation (from scheme) is triggered e.g. 0.5 means that irrigation will only be applied when soil water content is at 1/2 of the appropriate variable
'irr\_targ'|fraction|fraction of PAW/field (see irr\_frm\_paw) to irrigate (from scheme) up to.
'irr\_trig\_store'|fraction|the irrigation trigger value (if calc_ind_store_demand) for the storage based irrigation either fraction of PAW or field capacity
'irr\_targ\_store'|fraction| the irrigation target value (if calc_ind_store_demand) for the storage based irrigation either fraction of PAW or field capacity
'external\_inflow'|m<sup>3</sup>| only used if not runoff_from_rain, the volume (m3) of water to add to storage (allows external rainfall runoff model for storage management) can be negative

### Site Parameters description

**Key**|**Unit**|**Description**
| --- | --- | ---|
'abs_max_irr' | mm | the maximum irrigation that can be applied per day (e.g. equipment limits) mm/day note that if matrix weather prescribed max_irr for a given day is larger then abs_max_irr, that water may still be avalible to refill storage.
'BD'|   kg l-1|  Bulk density of soil
'calc_ind_store_demand' |sudo boolean 1=True, 0=False   | if true then calculate storage demand after scheme irrigation from triggers, targets, if false then calculate storage demand as the remaining demand after scheme irrigation,
'CO2A'|  ppm|   CO2 concentration in atmosphere woodward 2020 set to 350
'DRATE'|    mm d-1| Maximum soil drainage rate   woodward 2020 set to 50
'FGAS'|  -|  Fraction of soil volume that is gaseous
'fixed\_removal'|   | sudo boolean(1=True 0=False) defines if auto\_harv\_targ is fixed amount or amount to harvest to
'FO2MX'|   mol O2 mol-1 gas|  Maximum oxygen fraction of soil gas
'FWCAD'|    m3 m-3|  Relative saturation at air dryness
'FWCFC'|    m3 m-3|  Relative saturation at field capacity
'FWCWET'|   m3 m-3|  Relative saturation above which transpiration is reduced
'FWCWP'|    m3 m-3|  Relative saturation at wilting point
'h2o_store_max_vol' | m<sup>3</sup>| h2o storage maximum volume (m3)
'h2o_store_SA' | m<sup>2</sup> | h2o storage surface area (m2)
'I_h2o_store_vol' |fraction | initial h2o storage fraction
'irr\_frm\_paw'|   |  are irrigation trigger/target the fraction of profile available water (1/True or the fraction of field capacity (0/False) also determines whether passed soil moisture data is from PAW or FC, see 'pass_soil_moist'.
'irrigated_area' |ha | the area irrigated (ha)
'IRRIGF'|   fraction|   fraction of the needed irrigation to apply to bring water content up to field capacity
'KRTOTAER'|     -|  Ratio of total to aerobic respiration
'KSNOW'|      mm-1|  Light extinction coefficient of snow
'KTSNOW'|   m-1|  Temperature extinction coefficient of snow
'LAMBDAsoil'|    J m-1 degC-1 d-1|  Thermal conductivity of soil?
'LAT'|   degN|  Latitude
'opt\_harvfrin'|    | sudo boolean(1=True  0=False) if True  harvest fraction is estimated by brent zero optimisation if false  harvest fraction is estimated by brent zero optimisation if false  HARVFRIN = DM\_RYE\_RM/DMH\_RYE. As the harvest fraction is non-linearly related to the harvest  the amount harvested may be significantly greather than expected depending on CST
'pass_soil_moist'|sudo boolean 1=True, 0=False   | if True then do not calculate soil moisture instead soil moisture is passed to the model through max_irr as a fraction of either soil capacity when 'irr_frm_paw' is False, or as a fraction (0-1) of PAW when 'irr_frm_paw' is True this prevent any irrigation scheduling or and soil moisture calculation in the model.
'poolInfilLimit'| m|   woodward set to  0.2  Soil frost depth limit for water infiltration
'reseed\_CLV'|   (gC m-2)| Weight of leaves after reseed if >= 0 otherwise use current state of variable
'reseed\_CRES'|   (gC m-2)| Weight of reserves after reseed if >= 0 otherwise use current state of variable
'reseed\_CST'|   (gC m-2)| Weight of stems after reseed if >= 0 otherwise use current state of variable
'reseed\_CSTUB'|   (gC m-2)| Weight of stubble after reseed if >= 0 otherwise use current state of variable
'reseed\_harv\_delay'|  days| number of days to delay harvest after reseed  must be >=1
'reseed\_LAI'|   (m2 m-2)|  > =0 the leaf area index to set after reseeding  if < 0 then simply use the current LAI
'reseed\_TILG1'|   (m-2)| Elongating generative tiller density after reseed if >=0 otherwise use current state of variable
'reseed\_TILG2'|   (m-2)| Non-elongating generative tiller density after reseed if >=0 otherwise use current state of variable
'reseed\_TILV'|   (m-2)| Non-elongating tiller density after reseed if >=0 otherwise use current state of variable
'RHOnewSnow'|    kg SWE m-3|  Density of newly fallen snow
'RHOpack'|      d-1|  Relative packing rate of snow
'runoff_area' |m<sup>2</sup> | the area that can provide runoff to the storage (ha)
'runoff_frac' | fraction | the fraction of precipitation that becomes runoff to recharge storage (0-1, unit less)
'runoff_from_rain' |sudo boolean 1=True, 0=False   | if True then use a fraction of rainfall, otherwise proscribed refill data from an external model
'stor_full_refil_doy' |day of year (1-366)   | the day of the year (0-366) when storage will be set to full. set to -1 to never fully refill storage
'stor_irr_ineff' |fraction | the fraction of irrigation water that is lost when storage is used for irrigation (e.g. 0 means a perfectly efficient system, 1 means that 2x the storage volume is needed to irrigate x volume) unit less
'stor_leakage' |m<sup>3</sup> | the losses from storage to leakage static (m3/day)
'stor_refill_losses' |fraction | the losses incurred from re-filling storage from irrigation scheme (0-1)
'stor_refill_min' | mm | the minimum amount of excess irrigation water that is needed to refill storage (mm/day)
'stor_reserve_vol'|m<sup>3</sup>| the volume of storage to reserve (e.g. irrigation is cutoff at this volume)
'SWret'|    mm mm-1 d-1|  Liquid water storage capacity of snow
'SWrf'|   mm d-1 °C-1|  Maximum refreezing rate per degree below 'TmeltFreeze'
'TmeltFreeze'|     Â°C|  Temperature above which snow melts
'TrainSnow'|   Â°C|  Temperature below which precipitation is snow
'use_storage' |sudo boolean 1=True, 0=False   | whether or not to include storage in the model
'WCI'|   m3 m-3|  Initial value of volumetric water content
'WCST'|    m3 m-3|  Volumetric water content at saturation
'WpoolMax'|  mm|  Maximum pool water (liquid plus ice)

### Plant Parameters description

**PARAMETER**|**units**|**Description**
| --- | --- | ---|
'ABASAL'|   d-1|  Grass basal area response rate
'BASALI'|   -|  Grass basal area
'CLAIV'|   m2 leaf m-2|  Maximum LAI remaining after harvest when no tillers elongate
'COCRESMX'|   -|  Maximum concentration of reserves in aboveground biomass
'CSTAVM'|   gC tiller-1|  Maximum stem mass of elongating tillers
'CSTI'|   gC m-2|  Initial value of stems
'DAYLA'|   -|  DAYL above which growth is prioritised over storage
'DAYLB'|   d d-1|  Day length below which DAYLGE becomes 0 and phenological stage is reset to zero (must be < DLMXGE)
'DAYLG1G2'|   d d-1|  Minimum day length above which generative tillers can start elongating
'DAYLGEMN'|   -|  Minimum daylength growth effect
'DAYLP'|   d d-1|  Day length below which phenological development slows down
'DAYLRV'|   -|  DAYL at which vernalisation is reset
'DELD'|   -|  Litter disappearance due to decomposition
'DELE'|   -|  Litter disappearance due to earthworms
'DLMXGE'|   d d-1|  Day length below which DAYLGE becomes less than 1 (should be < maximum DAYL?)
'Dparam'|   °C-1 d-1|  Constant in the calculation of dehardening rate
'EBIOMAX'|   -|  Earthworm biomass max
'FCOCRESMN'|   -|  Minimum concentration of reserves in above ground biomass as fraction of COCRESMX
'FGRESSI'|   -|  CRES sink strength factor
'FRTILGG1I'|   -|  Initial fraction of generative tillers that is still in stage 1
'FRTILGI'|   -|  Initial value of elongating tiller fraction
'FSLAMIN'|   -|  Minimum SLA of new leaves as a fraction of maximum possible SLA (must be < 1)
'FSMAX'|   -|  Maximum ratio of tiller and leaf appearance based on sward geometry (must be < 1)
'HAGERE'|   -|  Parameter for proportion of stem harvested
'HARVFRD'|   -|  Relative harvest fraction of CLVD
'Hparam'|   °C-1 d-1|  Hardening parameter
'KBASAL'|   ?|  Constant at half basal area
'KCRT'|   gC m-2|  Root mass at which ROOTD is 67% of ROOTDM
'KLAI'|   m2 m-2 leaf|  PAR extinction coefficient
'KLUETILG'|   -|  LUE-increase with increasing fraction elongating tillers
'KRDRANAER'|   d-1|  Maximum relative death rate due to anearobic conditions
'KRESPHARD'|   gC gC-1 °C-1|  Carbohydrate requirement of hardening
'KRSR3H'|   °C-1|  Constant in the logistic curve for frost survival
'LAICR'|   m2 leaf m-2|  LAI above which shading induces leaf senescence
'LAIEFT'|   m2 m-2 leaf|  Decrease in tillering with leaf area index
'LAITIL'|   -|  Maximum ratio of tiller and leaf apearance at low leaf area index
'LDT50A'|   d|  Intercept of linear dependence of LD50 on lT50
'LDT50B'|   d °C-1|  Slope of linear dependence of LD50 on LT50
'LERGA'|   °C|  Leaf elongation intercept generative
'LERGB'|   mm d-1 °C-1|  Leaf elongation slope generative
'LERVA'|   °C|  Leaf elongation intercept vegetative
'LERVB'|   mm d-1 °C-1|  Leaf elongation slope vegetative
'LFWIDG'|   m|  Leaf width on elongating tillers
'LFWIDV'|   m|  Leaf width on non-elongating tillers
'LOG10CLVI'|   gC m-2|   log10 of Initial value of leaves
'LOG10CRESI'|   gC m-2|  log10 of Initial value of reserves
'LOG10CRTI'|   gC m-2|   log10 of Initial value of roots
'LOG10LAII'|   m2 m-2|  Initial value of leaf area index
'LSHAPE'|   -|  Area of a leaf relative to a rectangle of same length and width (must be < 1)
'LT50I'|   °C|  Initial value of LT50
'LT50MN'|   °C|  Minimum LT50 (Lethal temperature at which 50% die)
'LT50MX'|   °C|  Maximum LT50
'NELLVM'|   tiller-1|  Number of elongating leaves per non-elongating tiller
'PHENCR'|   -|  Phenological stage above which elongation and appearance of leaves on elongating tillers decreases
'PHENI'|   -|  Initial value of phenological stage
'PHY'|   °C d|  Phyllochron
'RATEDMX'|   °C d-1|  Maximum dehardening rate
'RDRHARVMAX'|   d-1|  Maximum relative death rate due to harvest
'RDRROOT'|   d-1|  Relatuive death rate of root mass CRT
'RDRSCO'|   d-1|  Increase in relative death rate of leaves and non-elongating tillers due to shading per unit of LAI above LAICR
'RDRSMX'|   d-1|  Maximum relative death rate of leaves and non-elongating tillers due to shading
'RDRSTUB'|   -|  Relative death rate of stubble/pseudostem
'RDRTEM'|   d-1 °C-1|  Proportionality of leaf senescence with temperature
'RDRTILMIN'|   d-1|  Background relative rate of tiller death
'RDRTMIN'|   d-1|  Minimum relative death rate of foliage
'RDRWMAX'|   d-1|  Maximum death rate due to water stress
'reHardRedDay'|   d|  Duration of period over which rehardening capability disappears
'RGENMX'|   d-1|  Maximum relative rate of tillers becoming elongating tillers
'RGRTG1G2'|   d-1|  Relative rate of TILG1 becoming TILG2
'ROOTDM'|   m|  Initial and maximum value rooting depth
'RRDMAX'|   m d-1|  Maximum root depth growth rate
'RUBISC'|   g m-2 leaf|  Rubisco content of upper leaves
'SIMAX1T'|   gC tiller-1 d-1|  Sink strength of small elongating tillers
'SLAMAX'|   m2 leaf gC-1|  Maximum SLA of new leaves (Note unusual units)
'TBASE'|   °C|  Minimum value of effective temperature for leaf elongation
'TCRES'|   d|  Time constant of mobilisation of reserves
'THARDMX'|   °C|  Maximum surface temperature at which hardening is possible
'TILTOTI'|   m-2|  Initial value of tiller density
'TOPTGE'|   °C|  Optimum temperature for vegetative tillers to become generative (must be > TBASE)
'TRANCO'|   mm d-1 g-1 m2|  Transpiration effect of PET
'TRANRFCR'|   -|  Critical water stress for tiller death
'TsurfDiff'|   °C|  Constant in the calculation of dehardening rate
'TVERN'|   °C|  Temperature below which vernalisation advances
'TVERND'|   d|  Days of cold after which vernalisation completed
'TVERNDMN'|   d|  Minimum vernalisation days
'VERNDI'|   d|  Initial value of cumulative vernalisation days
'YG'|   gC gC-1|  Growth yield per unit expended carbohydrate (must be < 1)

### output description

**varname**|**units**|**description**
| --- | --- | ---|
'BASAL'|(%)|Basal Area
'CLV'|(gC m-2)|Leaf C
'CLVD'|(gC m-2)|Dead Leaf C
'CRES'|(gC m-2)|Reserve C
'CRT'|(gC m-2)|Root C
'CST'|(gC m-2)|Stem C
'CSTUB'|(gC m-2)|Stubble C
'DAVTMP'|(degC)|Av. Temp.
'DAYL'|(-)|Daylength
'DAYLGE'|(-)|Daylength Fact.
'DEBUG'|(?)|Debug
'DM\_RYE\_RM'|(kg DM ha-1)|dry matter of Rye species harvested in this time step Note that this is the calculated removal but if 'opt\_harvfrin' = False then it may be significantly different to the actual removal which is show by the appropriate yield variable
'DM\_WEED\_RM'|(kg DM ha-1)|dry matter of weed species harvested in this time step; Note that this is the calculated removal but if 'opt\_harvfrin' = False then it may be significantly different to the actual removal which is show by the appropriate yield variable
'DM'|(kg DM ha-1)|Ryegrass Mass Note that this is after any harvest (e.g. at end of time stamp)
'DMH\_RYE'|(kg DM ha-1)|harvestable dry matter of rye species includes harvestable fraction of dead (HARVFRD) note that this is before any removal by harvesting
'DMH\_WEED'|(kg DM ha-1)|harvestable dry matter of weed specie includes harvestable fraction of dead (HARVFRD) note that this is before any removal by harvesting
'DMH'|(kg DM ha-1)|harvestable dry matter = DMH\_RYE + DMH\_WEED note that this is before any removal by harvesting
'doy'|(d)|Day of Year
'DRAIN'|(mm d-1)|Drainage
'DTILV'|(till m-2 d-1)|Till. Death
'EVAP'|(mm d-1)|Evap.
'external_inflow',| m<sup>3</sup> | input value external inflow (m3) kept for full water budget of storage
'FS'|(till leaf-1)|Site Filling
'GRT'|(gC m-2 d-1)|Root Growth
'GTILV'|(till m-2 d-1)|Till. Birth
'h2o_store_per_area'| mm | h2o storage per irrigated area (mm)
'h2o_store_vol'| m<sup>3</sup>| volume of water in storage (m3)
'HARVFR'|(-)|Harvest Frac.
'HARVFRIN'|(-)|Harvest Data
'IRR\_TARG'|fraction|irrigation Target (fraction of field capacity) to fill to also an input variable
'IRR\_TRIG'|fraction|irrigation trigger (fraction of field capacity at which to start irrigating
'IRR_TARG_store'|fraction | irrigation target for storage (fraction paw/FC), input, only relevant if calc_ind_store_demand
'IRR_TRIG_store'|fraction | irrigation trigger for storage (fraction paw/FC), input, only relevant if calc_ind_store_demand
'IRRIG\_DEM'|mm|irrigation irrigation demand to field capacity * IRR\_TARG
'irrig_dem_store'| mm | irrigation demand from storage (mm)
'irrig_scheme'| mm | irrigation applied from the scheme (mm)
'irrig_store'| mm | irrigation applied from storage (mm)
'IRRIG'|mm d-1|Irrigation applied
'LAI'|(m2 m-2)|LAI
'LERG'|(m d-1)|Gen. Elong. Rate
'LERV'|(m d-1)|Veg. Elong. Rate
'LINT'|(-)|Light Intercep.
'LT50'|(degC)|Hardening
'MXPAW'|mm|maximum Profile available water
'PAW'|mm|Profile available water at the time step
'PHEN'|(-)|Phen. Stage
'PHENRF'|(-)|Phen. Effect
'PHOT'|(gC m-2 d-1)|Photosyn.
'RAIN'|(mm d-1)|Rain
'RDLVD'|(d-1)|Decomp. Rate
'RDRL'|(d-1)|Leaf Death Rate
'RDRTIL'|(d-1)|Till. Death Rate
'RES'|(g g-1)|Reserve C
'RESEEDED'| |reseeded flag if ==1 then the simulation was reseeded on this day
'RESMOB'|(gC m-2 d-1)|Res. Mobil.
'RGRTV'|(d-1)|Till. App. Rate
'RLEAF'|(d-1)|Leaf App. Rate
'ROOTD'|(m)|Root Depth
'RUNOFF'|(mm d-1)|Runoff
'RYE\_YIELD'|(tDM ha-1)|PRG Yield from rye grass species note that this is the actual amount of material that has been removed
'SLA'|(m2 gC-1)|Spec. Leaf Area
'SLANEW'|(m2 gC-1)|New SLA
'store_evap_out'| m<sup>3</sup> | storage budget out from evaporation (NOTIMPLEMENTED) (m3)
'store_irr_loss'| m<sup>3</sup> | storage budget out from losses incurred with irrigation (m3)
'store_leak_out'| m<sup>3</sup> | storage budget out from leakage (m3)
'store_overflow', | m<sup>3</sup> |water that could have been added to storage (including losses), but was not as storage was full (m3)
'store_runoff_in'| m<sup>3</sup>| storage budget in from runoff or external model (m3)
'store_scheme_in_loss'| m<sup>3</sup> | storage budget out losses from the scheme to the storage basin (m3)
'store_scheme_in'| m<sup>3</sup> | storage budget in from the irrigation scheme (m3)
'TILG1'|(m-2)|Gen. Tillers
'TILG2'|(m-2)|Elong. Tillers
'TILTOT'|(m-2)|Total Tillers
'TILV'|(m-2)|Veg. Tillers
'Time'|(y)|Time
'TRAN'|(mm d-1)|Trans.
'TRANRF'|(%)|Transpiration
'TSIZE'|(gC tiller-1)|Tiller Size
'VERN'|(%)|Vernalisation
'VERND'|(d)|Vern. Days
'WAFC'|mm|Water in non-frozen root zone at field capacity
'WAL'|(mm)|Soil Water
'WAWP'|mm|Water in non-frozen root zone at wilting point
'WCL'|(%)|Eff. Soil Moisture
'WCLM'|(%)|Soil Moisture
'WEED\_YIELD'|(tDM ha-1)|PRG Yield from weed (other) species note that this is the actual amount of material that has been removed
'year'|(y)|Year
'YIELD'|(tDM ha-1)|PRG Yield sum of YIELD\_RYE and YIELD\_WEED




## References

* [BASGRA_2014](https://github.com/davcam/BASGRA): original model repository
* [BASGRA_NZ](https://github.com/woodwards/basgra_nz): update of the model to NZ conditions repository
* [Identifying causes of low persistence of perennial ryegrass (Lolium perenne) dairy pasture using the Basic Grassland model (BASGRA)](https://onlinelibrary.wiley.com/doi/abs/10.1111/gfs.12464):
  update from BASGRA to BASGRA NZ
* [BASGRA 2014 User guide](https://github.com/Komanawa-Solutions-Ltd/BASGRA_NZ_PY/blob/master/fortran_BASGRA_NZ/docs/BASGRA2014_USER_GUIDE.pdf)
  or .fortran_BASGRA_NZ/docs/BASGRA2014_USER_GUIDE.pdf
* [Conceptual Basis, Formalisations and Parameterization of the Stics Crop Model](https://books.google.co.nz/books?id=YwfZFcWgAAMC&pg=PA34&lpg=PA34&dq=vernalisation+model&source=bl&ots=7euCE4tPBe&sig=za2fBGqFVpoR1jKqkVB2NtBK0nc&hl=en&sa=X&ved=2ahUKEwi4stOBi_rcAhXZzmEKHcK6DE0Q6AEwBXoECAQQAQ#v=onepage&q=vernalisation%20model&f=false)
* [Irrigation Management for Cropping - A Grower’s Guide](https://www.far.org.nz/assets/files/uploads/Iss_04_Irrigation.pdf)
  or .fortran_BASGRA_NZ/docs/FAR-Irrigation Management.pdf
* [Estimation of field capacity and wilting point of some New Zealand soils from their saturation percentages](https://www.tandfonline.com/doi/abs/10.1080/01140671.1990.10428101)
* [High perennial ryegrass seeding rates do not negatively impact pasture sward persistence](https://onlinelibrary.wiley.com/doi/abs/10.1111/gfs.12335)
* [Seasonal patterns of root, tiller and leaf production in a Grasslands Ruanui ryegrass sward](https://www.researchgate.net/profile/C-Matthew/publication/266180775_Seasonal_patterns_of_root_tiller_and_leaf_production_in_a_Grasslands_Ruanui_ryegrass_sward/links/56b2ecd408ae56d7b06cdb89/Seasonal-patterns-of-root-tiller-and-leaf-production-in-a-Grasslands-Ruanui-ryegrass-sward.pdf)
* [Fertiliser Nitrogen and Factors Affecting Pasture Responses](https://benthamopen.com/ABSTRACT/TOASJ-2-35)
* [Differential responses of tillers to floral induction in perennial ryegrass (Lolium perenne L.) : implications for perenniality](https://mro.massey.ac.nz/handle/10179/842)
* [A practical model for predicting soil water deficit in New Zealand pastures](tandfonline.com/doi/abs/10.1080/00288233.2001.9513464)
* A mathematical model of perennial grass-clover dairy pasture for control of post-reproductive pasture quality using
  water and grazing management by Simon Woodward (unpublished)
