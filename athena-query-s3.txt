CREATE EXTERNAL TABLE IF NOT EXISTS swo_inventory.swo_s3_inventory (
  `AccountID` string,
  `BucketName` string,
  `Access` string,
  `Size` int,
  `Region` string,
  `LifecycleRule` string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = ',',
  'field.delim' = ','
) LOCATION 's3://swo-inventory-s3-dev/'
TBLPROPERTIES ('has_encrypted_data'='false', 'skip.header.line.count'='1');
