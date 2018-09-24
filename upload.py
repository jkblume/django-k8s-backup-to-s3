# call dumpdata of pod you want to backup
import shlex
from subprocess import Popen, PIPE
import boto3
import os
import time
import shutil

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
PROJECT_NAME = os.getenv("PROJECT_NAME")
MEDIA_DIRECTORY = os.getenv("MEDIA_DIRECTORY")
POD_ID = os.getenv("POD_ID")
DUMPDATA_EXCLUDE = os.getenv("DUMPDATA_EXCLUDE")

BACKUP_BASE_FILE_NAME = f'{PROJECT_NAME}/{time.strftime("%d-%m-%Y")}'

# backup db with dumpdata and upload to s3
cmd = f"kubectl exec -it {POD_ID} python manage.py dumpdata {DUMPDATA_EXCLUDE}"
process = Popen(shlex.split(cmd), stdout=PIPE)
(output, err) = process.communicate()
print(output)
exit_code = process.wait()

s3 = boto3.resource('s3')
object = s3.Object(S3_BUCKET_NAME, f"{BACKUP_BASE_FILE_NAME}.json")
object.put(Body=output)

# backup media files while zip then and afterwards upload to s3
shutil.make_archive('media-data', 'zip', "/media-data")
data = open('media-data.zip', 'rb')
object = s3.Object(S3_BUCKET_NAME, f"{BACKUP_BASE_FILE_NAME}.zip")
object.put(Body=data)