import boto3
import csv
from io import StringIO

def get_instance_platform(ec2_client, instance):
    if 'Platform' in instance:
        return instance['Platform']
    else:
        image_id = instance['ImageId']
        image_info = ec2_client.describe_images(ImageIds=[image_id])
        if 'Images' in image_info and len(image_info['Images']) > 0:
            platform_details = image_info['Images'][0].get('PlatformDetails', '')
            if 'Windows' in platform_details:
                return 'Windows'
    return 'Linux/UNIX'

def lambda_handler(event, context):
    ec2_client = boto3.client(service_name='ec2', region_name='us-east-1')
    ec2_resource = boto3.resource(service_name='ec2', region_name='us-east-1')
    s3_client = boto3.client('s3')

    account_id = boto3.client('sts').get_caller_identity().get('Account')
    
    data = StringIO()
    csv_writer = csv.writer(data)
    csv_writer.writerow(['AccountID', 'InstanceName', 'InstanceID', 'InstanceType', 'Region', 'Platform'])

    cnt = 1
    for each_ins_in_reg in ec2_resource.instances.all():
        instance_id = each_ins_in_reg.instance_id
        instance_type = each_ins_in_reg.instance_type
        instance_name = ''
        for tag in each_ins_in_reg.tags:
            if tag['Key'] == 'Name':
                instance_name = tag['Value']
                break
        region = 'us-east-1'
        platform = get_instance_platform(ec2_client, each_ins_in_reg.meta.data)
        
        csv_writer.writerow([account_id, instance_name, instance_id, instance_type, region, platform])
        cnt += 1
    
    data.seek(0)
    
    s3_bucket_name = 'your-ec2-bucket-name'
    s3_key = f'{account_id}_ec2_metadata_us_east_1.csv'
    
    s3_client.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=data.getvalue())
    
    return {
        'statusCode': 200,
        'body': 'Data written to S3 successfully'
    }