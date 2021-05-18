from datetime import datetime
import pytz as pytz
import boto3

boto3.setup_default_session(profile_name='s3-viewer')
s3 = boto3.client('s3')
response = s3.list_buckets()
bucket_names = [bucket['Name'] for bucket in response['Buckets']]

print('Select the bucket:')
for name in bucket_names:
    print(name)
selected_bucket = input('Enter bucket name: ')

response = s3.list_objects(Bucket=selected_bucket)
object_names = [obj['Key'] for obj in response['Contents']]

print('\nSelect the object:')
for name in object_names:
    print(name)
selected_object = input('\nEnter object key: ')

response = s3.list_object_versions(Bucket=selected_bucket, Prefix=selected_object)
versions = response['Versions']
versions.sort(key=lambda version: version['LastModified'])

print('\nObject have the next versions:')
for version in versions:
    print(version['LastModified'])
input_date = input("\nEnter the date to get the object in the next format: 'YYYY-MM-dd HH:mm:ss': ")
date = datetime.strptime(input_date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)

selected_version = None
for version in versions:
    if date > version['LastModified']:
        selected_version = version

if selected_version:
    response = s3.get_object(Bucket=selected_bucket, Key=selected_object, VersionId=selected_version['VersionId'])
    print(response['Body'].read().decode('utf-8'))
else:
    print('Such version is not exist')
