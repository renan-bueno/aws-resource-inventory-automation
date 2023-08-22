CREATE EXTERNAL TABLE swo_ec2_inventory (
  AccountID STRING,
  InstanceName STRING,
  InstanceID STRING,
  InstanceType STRING,
  Region STRING,
  Platform STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = ',',
  'field.delim' = ','
) LOCATION 's3://swo-inventory-ec2-dev/'
TBLPROPERTIES ('has_encrypted_data'='false', 'skip.header.line.count' = '1');
