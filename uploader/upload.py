import os

#from pyminio import Pyminio
from minio import Minio

MINIO_ENDPOINT = os.environ['MINIO_ENDPOINT']
ACCESS_KEY = os.environ['MINIO_ACCESS_KEY']
SECRET_KEY = os.environ['MINIO_SECRET_KEY']
DATA_PREFIX = os.environ['DATA_PREFIX']
BUCKET_NAME = os.environ['BUCKET_NAME'] #'my_bucket'
FILENAME = os.environ['FILENAME']

def upload():
    # create a connection to server
    minio_client = Minio(MINIO_ENDPOINT,
                        access_key=ACCESS_KEY,
                        secret_key=SECRET_KEY,
                        secure=False)

    # Make 'asiatrip' bucket if not exist.
    bucket_found = minio_client.bucket_exists(BUCKET_NAME)
    if not bucket_found:
        minio_client.make_bucket(BUCKET_NAME)
    else:
        print(f"Bucket {BUCKET_NAME} already exists")

    # Key (name) of the file inside Bucket
    FILEKEY = DATA_PREFIX + FILENAME
    # Upload the file to the bucket
    minio_client.fput_object(BUCKET_NAME, FILEKEY, FILENAME)

    # List all object paths in bucket
    objects = minio_client.list_objects(BUCKET_NAME, recursive=True)
    for obj in objects:
        print(obj.bucket_name, obj.object_name, obj.last_modified,
            obj.etag, obj.size, obj.content_type)

    # List all object paths in bucket that begin with my-prefixname.
    objects = minio_client.list_objects(BUCKET_NAME, recursive=True, prefix=DATA_PREFIX)
    for obj in objects:
        print(obj.bucket_name, obj.object_name, obj.last_modified,
            obj.etag, obj.size, obj.content_type)

if __name__ == "__main__":
    try:
        upload()
    except Exception as e:
        print("Error occurred.", e)
