from distutils.core import setup, Extension
from distutils.command.install import install as DistutilsInstall
import os


class MakeCLibraryInstall(DistutilsInstall):
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


setup(
    name='libshorttext',
    version='1.1',
    packages=['', 'libshorttext', 'libshorttext.analyzer', 'libshorttext.converter', 'libshorttext.converter.stemmer',
              'libshorttext.classifier', 'libshorttext.classifier.learner', 'libshorttext.classifier.learner.liblinear',
              'libshorttext.classifier.learner.liblinear.python'],
    url='',
    license='',
    author='',
    author_email='',
    description='',
    cmdclass={'install': MakeCLibraryInstall}
)
