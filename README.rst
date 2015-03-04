PyStratum
=========
A stored procedure and function loader, wrapper generator for MySQL and SQL Server in Python.

Overview
========
PyStratum is a tool and library with the following mayor functionalities:

* Loading modified and new stored routines and removing obsolete stored routines into/from a MySQL or SQL Server instance. This MySQL or SQL Server instance can be part of your development or a production environment. 
* Enhancing the (limited) syntax of MySQL and SQL Server stored routines with constants and custom types (based on actual table columns).
* Generating automatically a Python wrapper class for calling your stored routines. This wrapper class takes care about error handing and prevents SQL injections.
* Defining Python constants based on auto increment columns and column widths.

Status
=====
Currently this project is under development and for more information we refer to its sister project.

Sister Project 
==============
We are also working on PhpStratum_. PhpStratum_ provides the same functionalities as PyStratum but in a PHP 
environment and supports MySQL only.

.. _PhpStratum: https://github.com/SetBased/php-stratum.
