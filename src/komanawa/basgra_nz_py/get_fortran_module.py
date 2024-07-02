"""
created matt_dumont 
on: 26/04/24
"""
from copy import deepcopy
import warnings
import fmodpy
import sys
from pathlib import Path
import subprocess


def get_fortran_basgra(supply_pet, recomplile=False, verbose=False, binname='gfortran-11'):
    """
    get the callable fortran BASGRA function

    :param supply_pet: bool if True use the PET version, if False use the peyman version
    :param recomplile: bool if True force recompile the fortran code
    :param verbose: bool if True print the fortran compilation output
    :param version: str the version of gfortran to use, only tested on 11.4.0
    :return:
    """
    tested_fortran_versions = ['11.4.0', '12.3.0']
    bad_tested_fortran_versions = ['13.2.0']

    if sys.platform.startswith('linux'):
        which = subprocess.run(f'which {binname}', shell=True, check=False, stdout=subprocess.PIPE)
        if which.returncode != 0:
            raise ChildProcessError(f'which {binname} returned non zero... why?')
        if which.stdout is None:
            warnings.warn(
                'gfortran-11 not found, trying other gfortran instances alternativly please install gfortran: sudo apt install gfortran-11')
            binname = 'gfortran'
        try:
            out = subprocess.run(f'{binname} --version', shell=True, check=True, stdout=subprocess.PIPE)
            full_version = out.stdout.decode().split('\n')[0]
            version = full_version.split(' ')[-1]

            if version not in tested_fortran_versions:
                warnings.warn(
                    f'gfortran version {full_version} has not been tested, only versions {tested_fortran_versions} have been tested. '
                    f'YMMV, You may wish to clone the repo and run the tests yourself to ensure identical behaviour.'
                    f'note the following versions have caused issues {bad_tested_fortran_versions}')
        except subprocess.CalledProcessError:
            raise ChildProcessError('gfortran not found, please install gfortran: sudo apt install gfortran-11')

    else:
        warnings.warn(
            'This function is only tested on linux, you will need to have Gfortran installed on your system, and no guarantees are made for other systems.')
    f_compiler_args = ['-x', 'f95-cpp-input', '-O3', '-fdefault-real-8', '-cpp']
    if supply_pet:
        module_name = 'for_basgra_pet'
        f_compiler_args.append('-Dweathergen')
    else:
        module_name = 'for_basgra_peyman'

    fortran_dir = Path(__file__).parent.joinpath('fortran_BASGRA_NZ', 'uncompiled_fortran')

    dependencies = [str(fortran_dir.joinpath(f)) for f in [
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

    basepath = fortran_dir.joinpath('basgraf.f95')
    outputdir = fortran_dir.parent.joinpath(f'compiled_{module_name}')
    if outputdir.joinpath('basgraf', '__init__.py').exists() and not recomplile:
        pass
    else:
        for_basgra = fmodpy.fimport(
            str(basepath),
            output_dir=str(outputdir),
            dependencies=dependencies,
            f_compiler = binname,
            f_compiler_args=f_compiler_args,
            verbose=verbose,
            end_is_named=False,
            rebuild=True
        )
    if supply_pet:
        from komanawa.basgra_nz_py.fortran_BASGRA_NZ.compiled_for_basgra_pet.basgraf import basgramodule
    else:
        from komanawa.basgra_nz_py.fortran_BASGRA_NZ.compiled_for_basgra_peyman.basgraf import basgramodule

    return deepcopy(basgramodule)


if __name__ == '__main__':
    get_fortran_basgra(False)
    get_fortran_basgra(True)
