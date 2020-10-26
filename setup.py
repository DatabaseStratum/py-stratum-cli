from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyStratum-Cli',

    version='1.0.4',

    description='PyStratum-Cli: The frontend of PyStratum.',
    long_description=long_description,

    url='https://github.com/DatabaseStratum/py-stratum-cli',

    author='Set Based IT Consultancy',
    author_email='info@setbased.nl',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Code Generators',
        'Topic :: System :: Installation/Setup',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    keywords='PyStratum',

    packages=find_packages(exclude=['build', 'test']),

    install_requires=['cleo==0.6.8',
                      'PyStratum-Backend<2, >=1.0.2'],

    entry_points={
        'console_scripts': [
            'pystratum = pystratum_cli:main',
        ],
    }
)
