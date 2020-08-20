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

upcoming plans:
* include irrigation modelling?
