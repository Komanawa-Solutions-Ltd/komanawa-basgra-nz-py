# BASGRA_NZ

BASGRA_NZ_PY is a python wrapper for the 
[BASGRA_NZ](https://github.com/woodwards/basgra_nz/tree/master/model_package/src) fortran code, contains several 
new features and is the first version of BASGRA to have purpose built tests to ensure that all changes can be made in a
backwards compatible fashion (with some argument changes).

WARNING: this is an experimental library and no guarantee on quality or accuracy is made

The BASGRA NZ project tracks modifications to BASGRA for application to perennial ryegrass in New Zealand conditions.
The test data comes from the Seed Rate Trial 2011-2017. Modifications to BASGRA were necessary to represent this data.

see outstanding_issues.txt
for original info on the model see docs
for information on the changes made by Simon Woodward, see docs/Woodward et al 2020 Tiller Persistence GFS Final.pdf

BASGRA_NZ_PY is modified from Simon Woodward's 
[BASGRA_NZ](https://github.com/woodwards/basgra_nz/tree/master/model_package/src)
which is in turn modified from [BASGRA](https://github.com/davcam/BASGRA)

This repo diverged from Simon Woodward's 
[BASGRA_NZ](https://github.com/woodwards/basgra_nz/tree/master/model_package/src) as of August 2020, 
efforts will be made to incorporate further updates, but no assurances

# Python Implementation
BASGRA_NZ requires python 3.7 or less (3.8 handles DLLs more securely but this causes some faults)
required packages: 
* pandas
* numpy
* matplotlib

to install this general environment via conda: conda create --name basgranz python=3.7 numpy pandas matplotlib
or a fixed anaconda .yml library can be found in the environment.yml file

# package installation
BASGRA_NZ_PY can only be installed locally from a github pull and addition to your PYTHONPATH

todo setup pip/anaconda and see how to ship the dlls

this installs both the python wrapper and the source fortran code.  at present a fortran installation is 
required.

# Fortran Installation 
At present BASGRA_NZ_py requires fortran 64 and assumes the use of gfortran64.  It is beyond the scope of this readme
to detail how to install fortran, but general instructions can be found in this 
[youtube video](https://www.youtube.com/watch?v=wGv2kGl8OV0) 
WARNING the installation in this video is 32Bit

This repo was developed and tested with gfortran 64 4.8.1 which can be 
[downloaded here](https://sourceforge.net/projects/mingwbuilds/files/host-windows/releases/4.8.1/64-bit/threads-posix/seh/x64-4.8.1-release-posix-seh-rev5.7z/download)

# Fortran compilation
At present BASGRA_NZ_py requires fortran and requires the user to compile the fortran code.
The compilation code can be found in the following .bat file: fortran_BASGRA_NZ/compile_BASGRA_gfortran.bat
The python wrapper will attempt to run the compilation bat if the DLL it required does not exist.


# new features implemented from [Simon Woodward's BASGRA_NZ](https://github.com/woodwards/basgra_nz/tree/master/model_package/src)

A number of new features where necessary for futher modeling work. Specially more generalized irrigation 
and harvest management.  This required changes to the fortran code, but tests were put in place to ensure backwards 
compatibility (with some argument changes) to
[Simon Woodward's BASGRA_NZ](https://github.com/woodwards/basgra_nz/tree/master/model_package/src) as of August 2020.

## irrigation triggering and demand modelling v2.0.0

### New Irrigation Process
Irrigation modelling was developed to answer questions about pasture growth rates in the face of possible irrigation
 water restribtions; therefore the irrigation has been implemented as follows:

* if the day of year is within the irrigation season
    * if the fraction of soil water (e.g. WAL/WAFC) including the timestep modification to the soil water content
     (e.g. transpriation, rainfall, etc) are BELOW the trigger for that day
        * irrigation is applied at a rate = max(IRRIGF* amount of water needed to fill to 
        irrigation target * field capacity, max_irr on the day)  
    
This modification includes bug fixes that allowed irrigation to be negative.

### New irrigation input/outputs
a number of inputs have been added to parameters:
* 'IRRIGF',  # fraction # fraction of irrigation to apply to bring water content up to field capacity, 
this was previously set within the fortran code
* 'doy_irr_start', #doy >= doy_irr_start has irrigation applied if needed
* 'doy_irr_end',  #doy <= doy_irr_end has irrigation applied
* 'irr_frm_paw',  # are irrigation trigger/target the fraction of profile available water (1/True or 
                    # the fraction of field capacity (0/False). 

new columns has been added to matrix_weather:
* 'max_irr',  # maximum irrigation available (mm/d)
* 'irr_trig',  # fraction of PAW/field (see irr_frm_paw) capacity at or below which irrigation is triggered (fraction 0-1) e.g. 0.5 
means that irrigation will only be applied when soil water content is at 1/2 field capacity
 (e.g. water holding capacity)
* 'irr_targ',  # fraction of PAW/field (see irr_frm_paw) capacity to irrigate to (fraction 0-1)

New outputs have been added:

* 'IRRIG':  # mm d-1 Irrigation,
* 'WAFC': #mm # Water in non-frozen root zone at field capacity
* 'IRR_TARG',  # irrigation Target (fraction of field capacity) to fill to, also an input variable
* 'IRR_TRIG',  # irrigation trigger (fraction of field capacity at which to start irrigating
* 'IRRIG_DEM',  # irrigation irrigation demand to field capacity * IRR_TARG # mm

### How to run so that the results are backwards compatible with versions before V2.0.0
To run the model in the original (no irrigation fashion) set both max_irr and irr_trig to zero.


## Harvest management and scheduling v3.0.0
As of version v3.0.0 harvest managment has changed significantly to allow many more options for harvest management

### New Harvest processes 
harvesting has been changed to allow:
* automatic harvesting
* time varient harvestable dry matter triggers
* time varient harvestable dry matter target (e.g. dry matter is harvested to the target)
* time varient fixed weight harvesting
* time varient allowing weed species to provide some fraction of the rye grass production

#### Automatic harvesting process
In the automatic harvesting process 
1. a harvest trigger is set for each time step
2. at each time step harvestable Rye grass dry matter is calculated and reported by 
DMH_RYE = ((CLV+CST+CSTUB)/0.45 + CRES/0.40 + (CLVD * HARVFRD / 0.45)) * 10.0
2. at each time step harvestable weed species dry matter is calculated and reported by 
DMH_WEED =  WEED_DM_FRAC*DMH_RYE/BASAL*(1-BASAL)
3. total harvestable dry matter is calculated and reported by DMH_RYE + DMH_WEED
4. if the total harvestable dry matter is >= the dry matter target for that time step then harveting occurs
5. the amount of Dry matter to remove is calculated
    1. if fixed_removal flag then the amount to remove is defined by DM_RM = HARV_TARG * FRAC_HARV
    2. if not fixed_removal then the ammount to remove is defined by  
    DM_RM = ((DMH_RYE + DMH_WEED) - HARV_TARG) * FRAC_HARV
5. An inital fraction of dry mater to remove is calculated, HARVFRIN = DM_RYE_RM/DMH_RYE  Note that this means 
that the weed species dry matter harvested is not removed from the ryegrass model
6. iff 'opt_harvfrin'= True, the harvest fraction to remove is estimated by brent zero optimisation. This step 
is recommended as the harvest fraction is non-linearly related to the harvest as the stem and reserve harvest fracion 
is related to a power function.  In some test runs without estimation, target 500kg removal has 
actually removed c. 1000kg 
7. harvesting then progresses as per V2.0.0

#### Manual harvesting process
As per automatic harvesting, however the dataframe is reshaped within the pyhon code so that the row count 
is equal to n days.  all indexes where manual harvesting will not occur have the 'harv_trig' set to -1 so that no 
harvesting will occur

DMH_WEED or the harvestable dry matter from weed species is calculated at every time step.  as such 'weed_dm_frac' 
must be defined sensibly for every day of the simulation.  Internally the python wrapper to BASGRA_NZ_PY
 uses pd.Series.fillna(method='ffill') or fills the missing values with the last valid values.  if 'weed_dm_frac' 
 is not set for the first day of the series a warning is issued and the first valid value is used to fill the values
  before the first valid value. 

Note that if the dry matter value is below the trigger value for a given manual time step no harvesting will occur. 

### New Harvest inputs
New input parameters
* 'fixed_removal',  # float boolean(1.0=True, 0.0=False) defines if auto_harv_targ is fixed amount or amount to harvest
 to
* 'opt_harvfrin',  # float boolean(1.0=True, 0.0=False) if True, harvest fraction is estimated by brent zero 
  optimisation if false, HARVFRIN = DM_RYE_RM/DMH_RYE.  As the harvest fraction is non-linearly related to the 
  harvest, the amount harvested may be significantly greather than expected depending on CST. We would suggest 
  always setting 'opt_harvfrin' to True unless trying to duplicate a previous run done under v2.0.0- 

New outputs
* 'RYE_YIELD',  # PRG Yield from rye grass species, #  (tDM ha-1)  note that this is the actual amount of material 
that has been removed
* 'WEED_YIELD',  # PRG Yield from weed (other) species, #  (tDM ha-1)  note that this is the actual amount of material 
that has been removed
* 'DM_RYE_RM',  # dry matter of Rye species harvested in this time step (kg DM ha-1) Note that this is the calculated 
removal but if 'opt_harvfrin' = False then it may be significantly different to the actual removal, which is show by 
the appropriate yield variable
* 'DM_WEED_RM',  # dry matter of weed species harvested in this time step (kg DM ha-1) Note that this is the calculated
 removal but if 'opt_harvfrin' = False then it may be significantly different to the actual removal, which is show by
  the appropriate yield variable
* 'DMH_RYE',  # harvestable dry matter of # species, includes harvestable fraction of dead (HARVFRD) (kg DM ha-1)
* 'DMH_WEED',  # harvestable dry matter of # specie, includes harvestable fraction of dead (HARVFRD) (kg DM ha-1)
* 'DMH',  # harvestable dry matter = DMH_RYE + DMH_WEED  (kg DM ha-1)


New format for havest dataframe, 
* Datatype transition from int(v2.0.0-) to float(v3.0.0)
* Two allowable dataframe Lenghts:
    * Manual harvest (n x 6 dataframe, where n=number of harvest events), python auto_harvest=False
    * Automatic harvest (m x 6 dataframe, where m=ndays), python auto_harvest=True
* Note the fixed harvest size requirements of 100 days were fixed in V1.0.0
* Dataframe columns
    * 'year',  # e.g. 2002
    * 'doy',  # day of year 1 - 356 (366 for leap year)
    * 'frac_harv', # fraction (0-1) of material above target to harvest to maintain 'backward capabilities' with v2.0.0
    * 'harv_trig',  # dm above which to initiate harvest, if trigger is less than zero no harvest will take place
    * 'harv_targ',  # dm to harvest to or to remove depending on 'fixed_removal'
    * 'weed_dm_frac',  # fraction of dm of ryegrass to attribute to weeds

### How to run so that the results are backwards compatible with versions before V3.0.0
* 'fixed_removal' = 0
* 'opt_harvfrin' = 0
* manual harvest (python auto_harvest=False)
* set harvest dataframe as follows:
    *  'year', as per v2.0.0-
    * 'doy', as per v2.0.0-
    * 'frac_harv', as per v2.0.0- percent_harvest/100,  note that fraction harvest is now a float value
    * 'harv_trig', as 0 
    * 'harv_targ', as 0
    * 'weed_dm_frac' as 0    