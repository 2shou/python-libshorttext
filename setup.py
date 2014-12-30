import os
import shutil
from distutils.command.clean import clean as Clean
import sys
from os.path import join

from numpy.distutils.core import setup


SETUPTOOLS_COMMANDS = set([
    'develop', 'release', 'bdist_egg', 'bdist_rpm',
    'bdist_wininst', 'install_egg_info', 'build_sphinx',
    'egg_info', 'easy_install', 'upload', 'bdist_wheel',
    '--single-version-externally-managed',
])

if len(SETUPTOOLS_COMMANDS.intersection(sys.argv)) > 0:

    extra_setuptools_args = dict(
        zip_safe=False,  # the package can run out of an .egg file
        include_package_data=True,
    )
else:
    extra_setuptools_args = dict()


class CleanCommand(Clean):
    description = "Remove build artifacts from the source tree"

    def run(self):
        Clean.run(self)
        if os.path.exists('build'):
            shutil.rmtree('build')
        for dirpath, dirnames, filenames in os.walk('libshorttext'):
            for filename in filenames:
                if (filename.endswith('.so') or filename.endswith('.pyd') or filename.endswith(
                        '.dll') or filename.endswith('.pyc')):
                    os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                if dirname == '__pycache__':
                    shutil.rmtree(os.path.join(dirpath, dirname))


def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration

    config = Configuration(None, parent_package, top_path)

    # Avoid non-useful msg:
    # "Ignoring attempt to set 'name' (from ... "
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('libshorttext')

    return config


def setup_configuration():
    metadata = dict(
        name='libshorttext',
        version='1.1',
        url='',
        license='',
        author='',
        author_email='',
        description='',
        classifiers=[
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Operating System :: MacOS',
        ],
        cmdclass={'clean': CleanCommand},
        package_data={'libshorttext': [join('converter', 'stop-words', '*')]},
        **extra_setuptools_args
    )
    metadata['configuration'] = configuration
    setup(**metadata)


if __name__ == '__main__':
    setup_configuration()