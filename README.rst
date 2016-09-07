PyStratum
=========
A stored procedure and function loader, wrapper generator for MySQL, SQL Server and PostgreSQL in Python.

+-----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+
| Social                                                                                                                      | Release                                                                                            | Tests                                                                                          | Code                                                                                                |
+=============================================================================================================================+====================================================================================================+================================================================================================+=====================================================================================================+
| .. image:: https://badges.gitter.im/SetBased/py-stratum.svg                                                                 | .. image:: https://badge.fury.io/py/pystratum-mysql.svg                                            | .. image:: https://travis-ci.org/SetBased/py-stratum-mysql.svg?branch=master                   | .. image:: https://scrutinizer-ci.com/g/SetBased/py-stratum-mysql/badges/quality-score.png?b=master |
|   :target: https://gitter.im/SetBased/py-stratum?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge  |   :target: https://badge.fury.io/py/pystratum-mysql                                                |   :target: https://travis-ci.org/SetBased/py-stratum-mysql                                     |   :target: https://scrutinizer-ci.com/g/SetBased/py-stratum-mysql/?branch=master                    |
|                                                                                                                             | .. image:: https://www.versioneye.com/user/projects/5795ef48dfecc800390b0931/badge.svg?style=flat  | .. image:: https://scrutinizer-ci.com/g/SetBased/py-stratum-mysql/badges/coverage.png?b=master |                                                                                                     |
|                                                                                                                             |   :target: https://www.versioneye.com/user/projects/5795ef48dfecc800390b0931                       |   :target: https://scrutinizer-ci.com/g/SetBased/py-stratum-mysql/?branch=master               |                                                                                                     |
+-----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+

Overview
========
PyStratum is a tool and library with the following mayor functionalities:

* Loading modified and new stored routines and removing obsolete stored routines into/from a MySQL, SQL Server, or PostgreSQL instance. This MySQL, SQL Server, or PostgreSQL instance can be part of your development or a production environment.
* Enhancing the (limited) syntax of MySQL, SQL Server, and PostgreSQL stored routines with constants and custom types (based on actual table columns).
* Generating automatically a Python wrapper class for calling your stored routines. This wrapper class takes care about error handing and prevents SQL injections.
* Defining Python constants based on auto increment columns and column widths.

Status
======
Currently this project is under development and for more information we refer to its sister project.

Sister Project 
==============
We are also working on PhpStratum_. PhpStratum_ provides the same functionalities as PyStratum but in a PHP 
environment and supports MySQL only.

.. _PhpStratum: https://github.com/SetBased/php-stratum
