from setuptools import setup, find_packages

setup(
  name = 'worldcatidentities',
  packages = find_packages(exclude=["tests"]),
  version = '0.3',
  license='GPL-3',
  description = 'Package that recovers authorities data from OCLCs WorldCat Identities API',
  author = 'Wenceslao Arroyo-Machado',
  author_email = 'wences@ugr.es',
  url = 'https://github.com/Wences91/worldcatidentities',
  download_url = 'https://github.com/Wences91/worldcatidentities',
  keywords = ['API', 'WorldCat Identities'],
  install_requires=[
          'requests',
      ],
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