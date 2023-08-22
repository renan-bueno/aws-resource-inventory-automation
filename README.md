# Inventory Automation

## Overview

The Inventory Automation project is designed to streamline the process of gathering and managing inventory data across various AWS services, including EC2, RDS, and S3. Through the use of AWS Lambda functions, Amazon IAM Roles, Amazon S3, Amazon Simple Queue Service (SQS), Amazon Event Bridge Rule, and Amazon Athena, the system automates the extraction of metadata, organizes it into CSV files, and provides queryable tables for comprehensive insights. 

## Key Components:

- IAM Roles: Necessary IAM roles must be created to provide the Lambda functions with the appropriate permissions to access the required AWS resources, including S3 buckets, EC2 instances, RDS databases, and related services.
- Lambda Functions: Three separate functions tailored for EC2, RDS, and S3. They handle metadata extraction and push the data into specific S3 buckets.
- S3 Buckets: Three distinct S3 buckets are used to store the metadata extracted from EC2, RDS, and S3 respectively. It's crucial that the bucket names used in the Python code are consistent with those defined in the CloudFormation template.
- SQS Queue: Acts as an event-driven trigger for the Lambda functions, enabling a seamless and scalable execution process.
- EventBridge Schedule: Regularly scheduled events to initiate the extraction process at a defined interval (e.g., every minute).
- Athena Queries: Leverage Amazon Athena's power to create external tables for the CSV files. These tables enable the direct querying of inventory data, making analysis and reporting more efficient.

## Installation Guide

Provide step-by-step instructions on how to set up your project, including how to deploy the CloudFormation template and any other prerequisites.

1. Pre-Requisites: Ensure that you have the following set up:
   * AWS account with necessary permissions.
   * AWS CLI configured with appropriate credentials.
   * Git installed on your machine.
   * Visual Studio Code or another code editor.
2. Create four S3 Bucket.
   * Create three S3 bucket to store all the CSV files generated across different accounts for EC2, RDS and S3. This bucket's name should be consistent in the Python code and CloudFormation templates.
   * Create a fourth bucket to upload the python zip files. Make sure to matched the buckets name on the cloudformation template. It will be parametirezed once the cloudformation template is submited.
     
     Example: ```aws s3api create-bucket --bucket centralized-bucket-name --region your-region```.

     **Note**:
     - If it is multiple accounts, apply the Cross-Account Bucket Policy. The bucket policy in json format is in S3BucketsPermission.txt
     - Default region is us-east-1.
2. Clone the Repository:
   * Open your terminal and run the following command to clone the repository:
  
      ```git clone <repository_url>```
      
3. Deploy CloudFormation Template:
   * Navigate to the directory containing the CloudFormation template.
   * Run the following command to deploy the template and create the necessary AWS resources:
  
      ```aws cloudformation create-stack --stack-name InventoryAutomation --template-body file://<path_to_template.json>```
     
4. Configure Athena:
   * Log in to the AWS Management Console and navigate to Amazon Athena.
   * Execute the provided SQL scripts for EC2, RDS, and S3 to create the external tables.
5. Verify Deployment:
   * Check that the Lambda functions are deployed correctly and that the EventBridge is triggering them as expected.
   * Verify that the SQS queue is set up and that messages are being processed.
6. (Optional) Customize Lambda Functions:
   * If you need to make changes to the Lambda functions, you can modify the Python code and re-deploy using the CloudFormation template.
7. Monitor and Analyze Data:
   * As the system starts collecting data, you can use Amazon Athena to query the CSV files directly from S3 and analyze your inventory as needed.
  
### Note

* Ensure that your IAM roles and permissions are appropriately configured to allow the necessary actions on EC2, RDS, S3, and other involved services.
* Adjust the schedule expression in the EventBridge if you need the inventory to be collected at different intervals.
* Make sure to replace placeholders like bucket-name, your-region, and others with your specific details.

## Usage

The project aims to provide a real-time, scalable, and fully automated inventory management solution. It caters to organizations that use multiple AWS resources and need an effective way to track, report, and analyze their usage. The solution's design focuses on ease of deployment and customization, allowing it to be adapted to various use cases.

Whether it's monitoring resource utilization, compliance tracking, or strategic decision-making, the Inventory Automation project serves as a robust tool that harnesses the power of AWS cloud technologies to simplify and enhance inventory management.

## Contact

Renan Bueno – [renan.bueno@softwareone.com](mailto:renan.bueno@softwareone.com)

[https://github.com/renan-bueno/aws-resource-inventory-automation.git](https://github.com/renan-bueno/aws-resource-inventory-automation.git)
