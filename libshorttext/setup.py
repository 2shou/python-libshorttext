import os
from os.path import join

import numpy

from _build_utils import get_blas_info

import warnings
from numpy.distutils.system_info import get_info, BlasNotFoundError


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    libraries = []
    if os.name == 'posix':
        libraries.append('m')

    config = Configuration('libshorttext', parent_package, top_path)
    config.add_subpackage('analyzer')
    config.add_subpackage('classifier')
    config.add_subpackage(join('classifier', 'learner'))
    config.add_subpackage('converter')
    config.add_subpackage(join('converter', 'stemmer'))

    blas_info = get_info('blas_opt', 0)
    if (not blas_info) or (('NO_ATLAS_INFO', 1) in blas_info.get('define_macros', [])):
        config.add_library('cblas',
                           sources=[join('src', 'cblas', '*.c')])
        warnings.warn(BlasNotFoundError.__doc__)

    ### liblinear module
    cblas_libs, blas_info = get_blas_info()
    if os.name == 'posix':
        cblas_libs.append('m')

    liblinear_sources = ['liblinear.c',
                         join('src', 'liblinear', '*.cpp')]

    liblinear_depends = [join('src', 'liblinear', '*.h'),
                         join('src', 'liblinear', 'liblinear_helper.c')]

    config.add_extension('liblinear',
                         sources=liblinear_sources,
                         libraries=cblas_libs,
                         include_dirs=[join('src', 'cblas'),
                                       numpy.get_include(),
                                       blas_info.pop('include_dirs', [])],
                         extra_compile_args=blas_info.pop('extra_compile_args', []),
                         depends=liblinear_depends,
                         # extra_compile_args=['-O0 -fno-inline'],
                         **blas_info)

    ## end liblinear module

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup

    setup(**configuration(top_path='').todict())
