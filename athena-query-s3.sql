CREATE EXTERNAL TABLE IF NOT EXISTS inventory.s3_inventory (
  `AccountID` STRING,
  `BucketName` STRING,
  `Access` STRING,
  `Size` int,
  `Region` STRING,
  `LifecycleRule` STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = ',',
  'field.delim' = ','
) LOCATION 's3://your-s3-bucket-name/'
TBLPROPERTIES ('has_encrypted_data'='false', 'skip.header.line.count'='1');
