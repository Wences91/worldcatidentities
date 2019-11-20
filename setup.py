import os
from setuptools import setup, find_packages, Command

class CleanCommand(Command):
  user_options = []
  def initialize_options(self):
    self.cwd = None
  def finalize_options(self):
    self.cwd = os.getcwd()
  def run(self):
    assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
    #os.system ('rm -rf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')
    os.system ('rm -rf ./*.egg-info')

setup(
  name = 'worldcatidentities',
  packages = find_packages(exclude=["tests"]),
  version = '0.5',
  license='GPL-3',
  description = 'Package that recovers authorities data from OCLCs WorldCat Identities API',
  author = 'Wenceslao Arroyo-Machado',
  author_email = 'wences@ugr.es',
  url = 'https://github.com/Wences91/worldcatidentities',
  download_url = 'https://github.com/Wences91/worldcatidentities',
  keywords = ['API', 'WorldCat Identities'],
  install_requires = [
    'requests',
    'lxml',
  ],
  cmdclass={
    'clean': CleanCommand,
  },
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)