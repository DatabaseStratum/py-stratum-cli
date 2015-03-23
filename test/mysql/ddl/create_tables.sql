-- ---------------------------------------------------------------------------------------------------------------------
/**
 * PyStratum
 *
 * @copyright 2005-2015 Paul Water / Set Based IT Consultancy (https://www.setbased.nl)
 * @license   http://www.opensource.org/licenses/mit-license.php MIT
 * @link
 */
-- ---------------------------------------------------------------------------------------------------------------------
drop table if exists TST_FOO1;

create table TST_FOO1( tst_c00 int
,                      tst_c01 smallint
,                      tst_c02 tinyint
,                      tst_c03 mediumint
,                      tst_c04 bigint
,                      tst_c05 decimal(10,2)     
,                      tst_c06 float
,                      tst_c07 double
,                      tst_c08 bit(8)
,                      tst_c09 date
,                      tst_c10 datetime
,                      tst_c11 timestamp
,                      tst_c12 time
,                      tst_c13 year
,                      tst_c14 char(10)
,                      tst_c15 varchar(10)
,                      tst_c16 binary(10)
,                      tst_c17 varbinary(10)
,                      tst_c18 tinyblob
,                      tst_c19 blob
,                      tst_c20 mediumblob
,                      tst_c21 longblob
,                      tst_c22 tinytext
,                      tst_c23 text
,                      tst_c24 mediumtext
,                      tst_c25 longtext
,                      tst_c26 enum('a','b')
,                      tst_c27 set('a','b') )
engine=myisam
;

-- ---------------------------------------------------------------------------------------------------------------------
drop table if exists TST_FOO2;

create table TST_FOO2( tst_c00 int
,                      tst_c01 varchar(10)
,                      tst_c02 varchar(10)
,                      tst_c03 varchar(10)
,                      tst_c04 varchar(10) )
engine=myisam
;

insert into TST_FOO2( tst_c00
,                     tst_c01
,                     tst_c02
,                     tst_c03
,                     tst_c04 )
values( 1
,       'a'
,       'b'
,       'c1'
,       'd' )
,      ( 2
,       'a'
,       'b'
,       'c2'
,       'd' )
,      ( 3
,       'a'
,       'b'
,       'c3'
,       'd' )
;

-- ---------------------------------------------------------------------------------------------------------------------
drop table if exists TST_TABLE;

create table TST_TABLE( tst_c00 varchar(20)
,                      tst_c01 int(11)
,                      tst_c02 double
,                      tst_c03 decimal (10, 5)
,                      tst_c04 datetime
,                      t       int(11)
,                      s       int(11) )
engine=myisam
;

insert into TST_TABLE( tst_c00
,                      tst_c01
,                      tst_c02
,                      tst_c03
,                      tst_c04
,                      t
,                      s )
values( 'Hello'
,       1
,       '0.543'
,       '1.2345'
,       '2014-03-27 00:00:00'
,       '4444'
,       '1' )
,      ( 'World'
,        3
,        '3E-05'
,        0
,        '2014-03-28 00:00:00'
,        null
,        1 )
;

-- ---------------------------------------------------------------------------------------------------------------------
drop table if exists TST_LABEL;

create table TST_LABEL( tst_id   int unsigned not null auto_increment
,                       tst_test varchar(40)
,                       tst_label varchar(20)
,  primary key(tst_id)
) engine=myisam
;

insert into TST_LABEL( tst_test
,                      tst_label )
values( 'spam'
,       'TST_ID_SPAM')
,     ( 'eggs'
,       'TST_ID_EGGS')
;

-- ---------------------------------------------------------------------------------------------------------------------
