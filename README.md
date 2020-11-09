# BASGRA_NZ

WARNING: this is an experimental library and no guarantee on quality or accuracy is made

this model is modified from https://github.com/woodwards/basgra_nz/tree/master/model_package/src
which is in turn modified from https://github.com/davcam/BASGRA

This repo divereged from Woodwards as of August 2020, efforts will be made to incorporate further updates, but no assurances

The BASGRA NZ project tracks modifications to BASGRA for application to perennial ryegrass in New Zealand conditions.
The test data comes from the Seed Rate Trial 2011-2017. Modifications to BASGRA were necessary to represent this data.

see outstanding_issues.txt
for original info on the model see docs
for information on the changes made by Simon Woodward, see docs/Woodward et al 2020 Tiller Persistence GFS Final.pdf


general instructions to install fortran instructions here: https://www.youtube.com/watch?v=wGv2kGl8OV0 
WARNING the insallation in this video is 32Bit

I suggest compiling with gfortran 64:
   https://sourceforge.net/projects/mingwbuilds/files/host-windows/releases/4.8.1/64-bit/threads-posix/seh/x64-4.8.1-release-posix-seh-rev5.7z/download
compiliation code: compile_basgra_gfortran.bat, this uses weather option 2, where PET is passed to the model.

BASGRA_NZ requires python 3.7 or less (3.8 handles DLLs more securely but this causes some faults)
required packages: 
* pandas
* numpy.

# new features implemented

## irrigation triggering and demand modelling

a number of inputs have been added to parameters:
* 'IRRIGF',  # fraction # fraction of irrigation to apply to bring water content up to field capacity, this was previously set within the fortran code
* 'doy_irr_start', #doy >= doy_irr_start has irrigation applied if needed
* 'doy_irr_end',  #doy <= doy_irr_end has irrigation applied

new columns has been added to matrix_weather:
* 'max_irr',  # maximum irrigation available (mm/d)
* 'irr_trig',  # fraction of field capacity at or below which irrigation is triggered (fraction 0-1) e.g. 0.5 means that irrigation will only be applied when soil water content is at 1/2 field capacity (e.g. water holding capacity)
* 'irr_targ',  # fraction of field capacity to irrigate to (fraction 0-1)

New outputs have been added:

* 'IRRIG':  # mm d-1 Irrigation,
* 'WAFC': #mm # Water in non-frozen root zone at field capacity
* 'IRR_TARG',  # irrigation Target (fraction of field capacity) to fill to, also an input variable
* 'IRR_TRIG',  # irrigation trigger (fraction of field capacity at which to start irrigating
* 'IRRIG_DEM',  # irrigation irrigation demand to field capacity * IRR_TARG # mm

Irrigation modelling was developed to answer questions about pasture growth rates in the face of possible irrigation water restribtions; therefore the irrigation has been implmeented as follows:

* if the day of year is within the irrigation season
    * if the fraction of soil water (e.g. WAL/WAFC) including the timestep modification to the soil water content (e.g. transpriation, rainfall, etc) are BELOW the trigger for that day
        * irrigation is applied at a rate = max(IRRIGF* amount of water needed to fill to irrigation target * field capacity, max_irr on the day)  
    
To run the model in the original (no irrigation fashion) set both max_irr and irr_trig to zero.
This modification includes bug fixes that allowed irrigation to be negative.

#todo write up full description of changes here    