from distutils.core import setup
from distutils.command.install import install as DistutilsInstall
from distutils.command.clean import clean as Clean
import shutil
import os
from os.path import join


class MakeCommand(DistutilsInstall):
    def run(self):
        os.system('make')
        common_dir = 'libshorttext/converter/stemmer'
        target_dir = '%s/%s' % (self.build_lib, common_dir)
        self.mkpath(target_dir)
        os.system('mv %s/porter.so.1 %s' % (common_dir, target_dir))
        common_dir = 'libshorttext/classifier/learner'
        target_dir = '%s/%s' % (self.build_lib, common_dir)
        self.mkpath(target_dir)
        os.system('mv %s/util.so.1 %s' % (common_dir, target_dir))
        common_dir = 'libshorttext/classifier/learner/liblinear'
        target_dir = '%s/%s' % (self.build_lib, common_dir)
        self.mkpath(target_dir)
        os.system('mv %s/liblinear.so.1 %s' % (common_dir, target_dir))
        DistutilsInstall.run(self)


class CleanCommand(Clean):
    description = "Remove build artifacts from the source tree"

    def run(self):
        Clean.run(self)
        if os.path.exists('build'):
            shutil.rmtree('build')
        for dirpath, dirnames, filenames in os.walk('libshorttext'):
            for filename in filenames:
                if (filename.endswith('.o') or filename.endswith('.a') or filename.endswith(
                        '.so.1') or filename.endswith(
                        '.pyd') or filename.endswith(
                        '.dll') or filename.endswith('.pyc')):
                    os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                if dirname == '__pycache__':
                    shutil.rmtree(os.path.join(dirpath, dirname))


setup(
    name='libshorttext',
    version='1.1',
    packages=['', 'libshorttext', 'libshorttext.analyzer', 'libshorttext.converter', 'libshorttext.converter.stemmer',
              'libshorttext.classifier', 'libshorttext.classifier.learner', 'libshorttext.classifier.learner.liblinear',
              'libshorttext.classifier.learner.liblinear.python'],
    package_data={'libshorttext': [join('converter', 'stop-words', '*')]},
    url='',
    license='',
    author='',
    author_email='',
    description='',
    cmdclass={
        'install': MakeCommand,
        'clean': CleanCommand,
    },
)
