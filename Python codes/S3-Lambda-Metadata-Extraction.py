import boto3
import csv
from io import StringIO
from botocore.exceptions import ClientError

def get_bucket_size(s3_client, bucket_name):
    total_size = 0
    objects = s3_client.list_objects_v2(Bucket=bucket_name)
    for obj in objects.get('Contents', []):
        total_size += obj['Size']
    return total_size

def get_bucket_access(s3_client, bucket_name):
    try:
        response = s3_client.get_public_access_block(Bucket=bucket_name)
        public_access_block = response.get('PublicAccessBlockConfiguration', {})
        return (
            not public_access_block.get('BlockPublicAcls', False) and
            not public_access_block.get('IgnorePublicAcls', False) and
            not public_access_block.get('BlockPublicPolicy', False) and
            not public_access_block.get('RestrictPublicBuckets', False)
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            return True  # If there's no configuration, assume access is allowed
        else:
            raise

def lambda_handler(event, context):
    s3_client = boto3.client('s3', region_name='us-east-1')
    s3_resource = boto3.resource('s3', region_name='us-east-1')
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    
    data = StringIO()
    csv_writer = csv.writer(data)
    csv_writer.writerow(['AccountID', 'BucketName', 'Access', 'Size', 'Region', 'LifecycleRule'])
    
    for bucket in s3_resource.buckets.all():
        bucket_name = bucket.name
        bucket_region = s3_client.get_bucket_location(Bucket=bucket_name)['LocationConstraint'] or 'us-east-1'
        bucket_size = get_bucket_size(s3_client, bucket_name)
        access = get_bucket_access(s3_client, bucket_name)
        
        try:
            lifecycle_rules = s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            has_lifecycle_rule = 'Yes' if lifecycle_rules.get('Rules') else 'No'
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                has_lifecycle_rule = 'No'
            else:
                raise
        
        csv_writer.writerow([account_id, bucket_name, access, bucket_size, bucket_region, has_lifecycle_rule])
    
    data.seek(0)
    
    s3_bucket_name = 'swo-inventory-s3-dev'
    s3_key = f'{account_id}_s3_metadata_us_east_1.csv'
    
    s3_client.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=data.getvalue())
    
    return {
        'statusCode': 200,
        'body': 'S3 metadata written to S3 successfully'
    }
