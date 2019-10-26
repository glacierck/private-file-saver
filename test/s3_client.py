import os

import boto3
from moto import mock_s3

from core import configs
from core.s3_client import S3Client

REGION_NAME = 'ap-northeast-1'
BUCKET_NAME = 'testing-bucket-xxxxx'
DUMMY_TEST_FILE_PATH = './test_file.txt'


@mock_s3
def test_s3_client_properly_regards_transfer_config():
    client = S3Client(BUCKET_NAME)
    c_tc = client.transfer_config
    assert c_tc.multipart_chunksize == configs.MULTIPART_CHUNKSIZE, "S3Client does not regard MULTIPART_CHUNKSIZE config"
    assert c_tc.multipart_threshold == configs.MULTIPART_THRESHOLD, "S3Client does not regard MULTIPART_THRESHOLD config"
    assert c_tc.max_concurrency == configs.MAX_CONCURRENCY, "S3Client does not regard MAX_CONCURRENCY config"


@mock_s3
def test_put_and_get_object():
    # Create test bucket
    s3 = boto3.resource('s3', region_name=REGION_NAME)
    s3.create_bucket(Bucket=BUCKET_NAME)

    # Create a dummy test file
    with open(DUMMY_TEST_FILE_PATH, 'w') as f:
        f.write("test file")

    object_key = 'test_object_key_1'
    client = S3Client(BUCKET_NAME)
    client.put_object(object_key=object_key, file_path=DUMMY_TEST_FILE_PATH,
                      metadata={'md5sum': 'xxxxxxxxxx'})
    object_uploaded = client.get_object(object_key=object_key).get()
    assert object_uploaded['Body'].read().decode('utf-8') == 'test file'

    os.remove(DUMMY_TEST_FILE_PATH)