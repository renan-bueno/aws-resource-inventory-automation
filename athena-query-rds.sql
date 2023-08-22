CREATE EXTERNAL TABLE IF NOT EXISTS swo_inventory.swo_rds_inventory (
  `AccountID` STRING,
  `DBIdentifier` STRING,
  `Engine` STRING,
  `EngineVersion` STRING,
  `Size` STRING,
  `Region` STRING,
  `MultiAZ` STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = ',',
  'field.delim' = ','
) LOCATION 's3://swo-inventory-rds-dev/'
TBLPROPERTIES ('has_encrypted_data'='false', 'skip.header.line.count'='1');
