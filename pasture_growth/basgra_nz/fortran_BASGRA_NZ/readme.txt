this model is modified from https://github.com/woodwards/basgra_nz/tree/master/model_package/src
which is in turn modified from https://github.com/davcam/BASGRA

This repo divereged from Woodwards as of August 2020, efforts will be made to incorporate further updates, but no promises

The BASGRA NZ project tracks modifications to BASGRA for application to perennial ryegrass in New Zealand conditions.
The test data comes from the Seed Rate Trial 2011-2017. Modifications to BASGRA were necessary to represent this data.

see project_guide.txt
see outstanding_issues.txt
for original info on the model see docs
for information on the changes made by Simon Woodward, see docs/Woodward et al 2020 Tiller Persistence GFS Final.pdf


general instructions to install fortran instructions here: https://www.youtube.com/watch?v=wGv2kGl8OV0 WARNING THIS IS 32Bit

I suggest using compiling with gfortran 64:
   https://sourceforge.net/projects/mingwbuilds/files/host-windows/releases/4.8.1/64-bit/threads-posix/seh/x64-4.8.1-release-posix-seh-rev5.7z/download
compiliation code: compile_basgra_gfortran.bat, current DLL is 64 bit, this uses weather option 2, where PET is passed to the model.

# todo should I publish this packages, if so I need to make it python 3.8 compatible
# todo put in public git, waiting on pierre
# # todo set up requirements, just numpy and pandas
# # todo set up on pipi/anaconda
not very hard when you've got a template 😉
   https://github.com/Evapotranspiration/ETo
use this repo as a example
   https://packaging.python.org/tutorials/packaging-projects/
for pypi packaging
it's needs to go onto pypi before anaconda
once you get to the anaconda stage, talk to me and I'll work you through it...
well...I can also work you through the pypi bit too 😉