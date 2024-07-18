import os
import random
import string
from dataclasses import dataclass
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


@dataclass
class S3Instance:
    def __init__(self):
        self.aws_access_key_id = os.getenv("AWS_S3_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
        self.aws_region_name = os.getenv("AWS_S3_REGION_NAME")
        self.aws_s3_bucket_name = os.getenv("AWS_S3_BUCKET_NAME")

    def get_s3_instance(self):
        return boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region_name,
        )

    @staticmethod
    def upload_file(s3_client, file, user_uuid):
        try:
            random_string = "".join(random.choices(string.ascii_letters + string.digits, k=16))
            profile_image_uri = f"profile_images/{user_uuid}/{random_string}.png"
            s3_client.upload_fileobj(
                file,
                os.getenv("AWS_S3_BUCKET_NAME"),
                profile_image_uri,
            )
            profile_image_url = f"https://{os.getenv('AWS_S3_BUCKET_NAME')}.s3.amazonaws.com/{profile_image_uri}"
            return profile_image_url
        except (NoCredentialsError, PartialCredentialsError) as e:
            raise Exception("Could not upload file to S3: " + str(e))