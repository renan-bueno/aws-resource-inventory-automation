import boto3
import csv
from io import StringIO

def lambda_handler(event, context):
    rds_client = boto3.client(service_name='rds', region_name='us-east-1')
    s3_client = boto3.client('s3')

    account_id = boto3.client('sts').get_caller_identity().get('Account')
    
    data = StringIO()
    csv_writer = csv.writer(data)
    csv_writer.writerow(['AccountID', 'DBIdentifier', 'Engine', 'EngineVersion', 'Size', 'Region', 'MultiAZ'])

    rds_instances = rds_client.describe_db_instances()
    for instance in rds_instances['DBInstances']:
        db_identifier = instance['DBInstanceIdentifier']
        engine = instance['Engine']
        engine_version = instance['EngineVersion']
        size = instance['DBInstanceClass']
        region = 'us-east-1'
        multi_az = 'Yes' if instance['MultiAZ'] else 'No'
        
        csv_writer.writerow([account_id, db_identifier, engine, engine_version, size, region, multi_az])
    
    data.seek(0)
    
    s3_bucket_name = 'your-rds-bucket-name'
    s3_key = f'{account_id}_rds_metadata_us_east_1.csv'
    
    s3_client.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=data.getvalue())
    
    return {
        'statusCode': 200,
        'body': 'RDS metadata written to S3 successfully'
    }
