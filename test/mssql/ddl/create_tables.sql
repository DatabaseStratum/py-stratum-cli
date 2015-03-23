/*================================================================================*/
/* DDL SCRIPT                                                                     */
/*================================================================================*/
/*  Title    :                                                                    */
/*  FileName : py-stratum.ecm                                                     */
/*  Platform : SQL Server 2014                                                    */
/*  Version  : Concept                                                            */
/*  Date     : zondag 22 maart 2015                                               */
/*================================================================================*/
/*================================================================================*/
/* CREATE TABLES                                                                  */
/*================================================================================*/

CREATE TABLE [TST_FOO1] (
  [tst_bigint] BIGINT,
  [tst_int] INT,
  [tst_smallint] SMALLINT,
  [tst_tinyint] TINYINT,
  [tst_bit] BIT,
  [tst_money] MONEY,
  [tst_smallmoney] SMALLMONEY,
  [tst_decimal] DECIMAL(10,4),
  [tst_numeric] NUMERIC(12,4),
  [tst_float] FLOAT,
  [tst_real] REAL,
  [tst_date] DATE,
  [tst_datetime] DATETIME,
  [tst_datetime2] DATETIME2(7),
  [tst_datetimeoffset] DATETIMEOFFSET(7),
  [tst_smalldatetime] SMALLDATETIME,
  [tst_time] TIME(7),
  [tst_char] CHAR(10),
  [tst_varchar] VARCHAR(10),
  [tst_text] TEXT,
  [tst_nchar] NCHAR(10),
  [tst_nvarchar] NVARCHAR(10),
  [tst_ntext] NTEXT,
  [tst_binary] BINARY(100),
  [tst_varbinary] VARBINARY(100),
  [tst_image] IMAGE,
  [tst_xml] XML,
  [tst_geography] GEOGRAPHY,
  [tst_geometry] GEOMETRY
)
GO

EXECUTE sp_addextendedproperty 'MS_Description', 'TODO:
* cursor
* timestamp
* hierarchy
* uniqieidentifier
* sql_variant
* table', 'SCHEMA', '', 'TABLE', 'TST_FOO1', NULL, NULL
GO

CREATE TABLE [TST_FOO2] (
  [tst_c00] INT NOT NULL,
  [tst_c01] VARCHAR(10),
  [tst_c02] VARCHAR(10),
  [tst_c03] VARCHAR(10),
  [tst_c04] VARCHAR(10),
  CONSTRAINT [PK_TST_FOO2] PRIMARY KEY ([tst_c00])
)
GO

CREATE TABLE [TST_LABEL] (
  [tst_id] INT IDENTITY(1,1) NOT NULL,
  [tst_test] VARCHAR(40) NOT NULL,
  [tst_label] VARCHAR(40),
  CONSTRAINT [PK_TST_LABEL] PRIMARY KEY ([tst_id])
)
GO

CREATE TABLE [TST_TABLE] (
  [tst_c00] VARCHAR(20) NOT NULL,
  [tst_c01] INT,
  [tst_c02] REAL,
  [tst_c03] DECIMAL(10,5),
  [tst_c04] DATETIME,
  [tst_c05] INT,
  [tst_c06] INT,
  CONSTRAINT [PK_TST_TABLE] PRIMARY KEY ([tst_c00])
)
GO
