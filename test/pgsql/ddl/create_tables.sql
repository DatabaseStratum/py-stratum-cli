-- ---------------------------------------------------------------------------------------------------------------------
/**
 * PyStratum
 *
 * @copyright 2005-2015 Paul Water / Set Based IT Consultancy (https://www.setbased.nl)
 * @license   http://www.opensource.org/licenses/mit-license.php MIT
 * @link
 */
-- ---------------------------------------------------------------------------------------------------------------------
drop table if exists "tst_foo1";

CREATE TABLE "tst_foo1" (
  "tst_bigint" BIGINT,
  "tst_int" INTEGER,
  "tst_smallint" SMALLINT,
  "tst_bit" BIT,
  "tst_money" MONEY,
  "tst_numeric" NUMERIC(12,4),
  "tst_float" NUMERIC,
  "tst_real" REAL,
  "tst_date" DATE,
  "tst_timestamp" TIMESTAMP,
  "tst_time6" TIME(6),
  "tst_char" CHAR(10),
  "tst_varchar" VARCHAR(10),
  "tst_text" TEXT,
  "tst_bytea" BYTEA,
  "tst_xml" XML
);

-- ---------------------------------------------------------------------------------------------------------------------
drop table if exists "tst_foo2";

CREATE TABLE "tst_foo2" (
  "tst_c00" INTEGER NOT NULL,
  "tst_c01" VARCHAR(10),
  "tst_c02" VARCHAR(10),
  "tst_c03" VARCHAR(10),
  "tst_c04" VARCHAR(10),
  CONSTRAINT "PK_tst_foo2" PRIMARY KEY ("tst_c00")
);

insert into "tst_foo2"( tst_c00
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
drop table if exists "tst_table";

CREATE TABLE "tst_table" (
  "tst_c00" VARCHAR(20) NOT NULL,
  "tst_c01" INTEGER,
  "tst_c02" REAL,
  "tst_c03" NUMERIC(10,5),
  "tst_c04" DATE,
  "tst_c05" INTEGER,
  "tst_c06" INTEGER,
  CONSTRAINT "PK_tst_table" PRIMARY KEY ("tst_c00")
);

insert into "tst_table"( tst_c00
,                      tst_c01
,                      tst_c02
,                      tst_c03
,                      tst_c04
,                      tst_c05
,                      tst_c06 )
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
drop table if exists "tst_label";

CREATE TABLE "tst_label" (
  "tst_id" BIGSERIAL,
  "tst_test" VARCHAR(40) NOT NULL,
  "tst_label" VARCHAR(40),
  CONSTRAINT "PK_tst_label" PRIMARY KEY ("tst_id")
);

insert into "tst_label"( tst_test
,                      tst_label )
values( 'spam'
,       'TST_ID_SPAM')
,     ( 'eggs'
,       'TST_ID_EGGS')
;

-- ---------------------------------------------------------------------------------------------------------------------
