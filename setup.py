from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyStratum',

    version='0.1.3',

    description='A stored procedure and function loader, wrapper generator for MySQL and MS-SQL',
    long_description=long_description,

    url='https://github.com/SetBased/py-stratum',

    author='Paul Water, Valery Zuban',
    author_email='info@setbased.nl',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='stored routines,stored procedure,stored procedures,wrapper, loader,MySQL,SQL Server',

    packages=find_packages(exclude=['build', 'test']),

    entry_points={
        'console_scripts': [
            'pystratum = pystratum:main',
        ],
    }
)