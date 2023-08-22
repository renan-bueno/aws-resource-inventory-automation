CREATE EXTERNAL TABLE IF NOT EXISTS inventory.rds_inventory (
  `AccountID` STRING,
  `InstanceName` STRING,
  `InstanceID` STRING,
  `InstanceType` STRING,
  `Region` STRING,
  `Platform` STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = ',',
  'field.delim' = ','
) LOCATION 's3://your-ec2-bucket-name/'
TBLPROPERTIES ('has_encrypted_data'='false', 'skip.header.line.count' = '1');
