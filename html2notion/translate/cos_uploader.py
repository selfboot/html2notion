import asyncio
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos.cos_exception import CosClientError
from functools import partial
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from ..utils import logger, test_prepare_conf, config

class TencentCosUploaderAsync:
    def __init__(self, secret_id, secret_key, region, bucket, timeout=60):
        self.config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Timeout=timeout)
        self.client = CosS3Client(self.config)
        self.bucket = bucket

    @retry(stop=stop_after_attempt(5),
           wait=wait_exponential(multiplier=1, min=3, max=30),
           retry=retry_if_exception_type(CosClientError))
    async def upload_file(self, loop, local_path, key):
        with open(local_path, 'rb') as f:
            content = f.read()

        executor = loop.run_in_executor
        put_object_partial = partial(self.client.put_object, Bucket=self.bucket, Body=content, Key=key)
        response = await executor(None, put_object_partial)
        return response

    @retry(stop=stop_after_attempt(5),
           wait=wait_exponential(multiplier=1, min=3, max=30),
           retry=retry_if_exception_type(CosClientError))
    async def check_file_exist(self, loop, key):
        try:
            executor = loop.run_in_executor
            return await executor(None, self.client.object_exists, self.bucket, key)
        except Exception as e:
            logger.error(e)
            return False

    @retry(stop=stop_after_attempt(5),
           wait=wait_exponential(multiplier=1, min=3, max=30),
           retry=retry_if_exception_type(CosClientError))
    async def delete_file(self, loop, key):
        executor = loop.run_in_executor
        response = await executor(None, self.client.delete_object, self.bucket, key)
        return response


async def main():
    test_prepare_conf()

    try:
        secret_id = config["cos"]["secret_id"]
        secret_key = config["cos"]["secret_key"]
        region = config["cos"]["region"]
        bucket = config["cos"]["bucket"]
    except Exception as e:
        print(f"Please fill cos conf in the config file")
        return

    local_path = './demos/saul.webp'
    key = 'test/saul.webp'

    uploader = TencentCosUploaderAsync(secret_id, secret_key, region, bucket)
    loop = asyncio.get_event_loop()

    upload_response = await uploader.upload_file(loop, local_path, key)
    print(f"Upload response: {upload_response}")

    if await uploader.check_file_exist(loop, key):
        print("Upload successful!")
    else:
        print("Upload failed!")


if __name__ == "__main__":
    asyncio.run(main())
