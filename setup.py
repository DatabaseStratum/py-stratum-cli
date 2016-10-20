from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyStratum',

    version='0.10.10',

    description='A stored procedure and function loader and wrapper generator for MySQL, SQL Server, and PostgresSQL',
    long_description=long_description,

    url='https://github.com/SetBased/py-stratum',

    author='Set Based IT Consultancy',
    author_email='info@setbased.nl',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Code Generators',
        'Topic :: System :: Installation/Setup',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='stored routines, stored procedure, stored procedures, wrapper, loader, MySQL, SQL Server, PostgreSQL',

    packages=find_packages(exclude=['build', 'test']),

    install_requires=['cleo==0.5.0'],

    entry_points={
        'console_scripts': [
            'pystratum = pystratum:main',
        ],
    }
)
