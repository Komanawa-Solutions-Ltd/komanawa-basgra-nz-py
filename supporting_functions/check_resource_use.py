"""
 Author: Matt Hanson
 Created: 23/11/2020 9:50 AM
 """
import os
import sys
import timeit
import os

def timeit_test(py_file_path, function_names=('test_function', 'test_function2'), n=10):
    """
    run an automated timeit test, must be outside of the function definition, prints results in scientific notation
    units are seconds

    :param py_file_path: path to the python file that holds the functions,
                        if the functions are in the same script as call then  __file__ is sufficient.
                        in this case the function call should be protected by: if __name__ == '__main__':
    :param function_names: the names of the functions to test (iterable), functions must not have arguments
    :param n: number of times to test
    :return:
    """
    print(py_file_path)
    d = os.path.dirname(py_file_path)
    fname = os.path.basename(py_file_path).replace('.py', '')
    sys.path.append(d)
    out = {}
    for fn in function_names:
        print('testing: {}'.format(fn))
        t = timeit.timeit('{}()'.format(fn),
                          setup='from {} import {}'.format(fname, fn), number=n) / n
        out[fn] = t
        print('{0:e} seconds'.format(t))
    return out


if __name__ == '__main__':
    fns = ['run_example_basgra',
           'support_for_memory_usage']
    lens = [2192, 36600]
    temp = timeit_test(os.path.join(os.path.dirname(__file__), 'support_for_resource_use.py'),
                       fns)

    for f, l in zip(fns, lens):
        print('BASGRA took {:e} seconds to run {} which has {} sim days'.format(temp[f], f, l))
        print('BASGRA took {:e} seconds per realisation day to run {}'.format(temp[f] / l, f))
    import psutil
    process = psutil.Process(os.getpid())