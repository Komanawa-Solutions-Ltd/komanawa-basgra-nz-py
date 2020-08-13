gfortran -x f95-cpp-input -O3 -c -fdefault-real-8 parameters_site.f95 parameters_plant.f95 environment.f95 resources.f95 soil.f95 plant.f95 set_params.f95 basgraf.f95
gfortran -shared -o BASGRA.DLL parameters_site.o parameters_plant.o environment.o resources.o soil.o plant.o set_params.o basgraf.o
del *.o
del *.mod
pause