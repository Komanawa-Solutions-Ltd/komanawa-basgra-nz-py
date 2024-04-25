"""
created matt_dumont 
on: 26/04/24
"""
import fmodpy
import sys
from pathlib import Path


def get_fortran_basgra(supply_pet):
    """
    get the callable fortran BASGRA function
    :param supply_pet:
    :return:
    """
    f_compiler_args = ['-x', 'f95-cpp-input', '-O3', '-fdefault-real-8', '-cpp']
    if supply_pet:
        module_name = 'for_basgra_pet'
        f_compiler_args.append('-Dweathergen')
    else:
        module_name = 'for_basgra_peyman'

    dependencies = [str(Path(__file__).parent.joinpath('fortran_BASGRA_NZ', f)) for f in [
        'parameters_plant.f95',
        'parameters_site.f95',
        'plant.f95',
        'resources.f95',
        'set_params.f95',
        'soil.f95',
        'h2o_storage.f95',
        'environment.f95',
        'brent.f95',
    ]]

    # todo check gfortran is installed.
    outputdir = Path(__file__).parent.joinpath('fortran_BASGRA_NZ', f'compiled_{module_name}')
    sys.path.append(str(outputdir))

    for_basgra = fmodpy.fimport(
        str(Path(__file__).parent.joinpath('fortran_BASGRA_NZ/basgraf.f95')),
        output_dir=str(outputdir),
        dependencies=dependencies,
        f_compiler_args=f_compiler_args,
        verbose=True,
        end_is_named=False
    )

    return for_basgra  # todo check!!!


if __name__ == '__main__':
    get_fortran_basgra(False)
