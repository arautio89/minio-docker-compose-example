import os
import time

#from pyminio import Pyminio
from minio import Minio

MINIO_ENDPOINT = os.environ['MINIO_ENDPOINT']
ACCESS_KEY = os.environ['MINIO_ACCESS_KEY']
SECRET_KEY = os.environ['MINIO_SECRET_KEY']
DATA_PREFIX = os.environ['DATA_PREFIX']
BUCKET_NAME = os.environ['BUCKET_NAME']
FILENAME = os.environ['FILENAME']

def download():
    # create a connection to server
    minio_client = Minio(MINIO_ENDPOINT,
                        access_key=ACCESS_KEY,
                        secret_key=SECRET_KEY,
                        secure=False)

    while True:
        if minio_client.bucket_exists(BUCKET_NAME):
            print(f"{BUCKET_NAME} exists")
            break
        else:
            print(f"{BUCKET_NAME} does not exist")
            print("Wait a sec...")
            time.sleep(1)

    # Key (name) of the file inside Bucket
    FILEKEY = DATA_PREFIX + FILENAME

    while True:
        objects = minio_client.list_objects(BUCKET_NAME, recursive=True)
        object_names = [obj.object_name for obj in objects]

        if FILEKEY in object_names:
            print(f"Found {FILEKEY}!")
            break
        else:
            print(f"Couldn't find {FILEKEY}...")
            print(object_names)
            print("Wait a sec...")
            time.sleep(1)

    # get the object from MinIO
    model_file_object = minio_client.fget_object(BUCKET_NAME, FILEKEY, FILENAME)

    print(model_file_object)

    with open(FILENAME) as f:
        file_content = f.readlines()

    print(file_content)

if __name__ == "__main__":
    try:
        download()
    except Exception as e:
        print("Error occurred.", e)