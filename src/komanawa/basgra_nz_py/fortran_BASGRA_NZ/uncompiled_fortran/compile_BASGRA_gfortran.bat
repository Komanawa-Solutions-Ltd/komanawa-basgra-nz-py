:: this program creates the DLLS for both versions of BASGRA, but requires gfortran64
:: get gfortan: https://sourceforge.net/projects/mingwbuilds/files/host-windows/releases/4.8.1/64-bit/threads-posix/seh/x64-4.8.1-release-posix-seh-rev5.7z/download

:: this section creates the BASGRA DLL which expects PET to be supplied
gfortran -x f95-cpp-input -Dweathergen -O3 -c -fdefault-real-8 brent.f95 parameters_site.f95 parameters_plant.f95 environment.f95 h2o_storage.f95 resources.f95 soil.f95 plant.f95 set_params.f95 basgraf.f95
gfortran -shared -o BASGRA_pet.DLL brent.o parameters_site.o parameters_plant.o environment.o h2o_storage.o resources.o soil.o plant.o set_params.o basgraf.o
del *.o
del *.mod

:: this section creates the BASGRA DLL which expects PET to be calculated by the peyman equation
gfortran -x f95-cpp-input -O3 -c -fdefault-real-8 brent.f95 parameters_site.f95 parameters_plant.f95 environment.f95 h2o_storage.f95 resources.f95 soil.f95 plant.f95 set_params.f95 basgraf.f95
gfortran -shared -o BASGRA_peyman.DLL brent.o parameters_site.o parameters_plant.o environment.o h2o_storage.o resources.o soil.o plant.o set_params.o basgraf.o
del *.o
del *.mod
