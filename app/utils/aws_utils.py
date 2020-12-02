import boto3, pandas

class AWSBucket:
    def __init__(
            self,
            current_app):
        self.aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID']
        self.aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
        self.region=current_app.config['AWS_REGION']
        self.bucket=current_app.config['AWS_BUCKET']

    def get_client(self):
        """
        Method to return an instance of S3 Client
        """
        return boto3.client('s3',
        self.region,
        aws_access_key_id = self.aws_access_key_id,
        aws_secret_access_key = self.aws_secret_access_key)

    def list_bucket_items(self, s3_client):
        result = s3_client.list_objects(Bucket=self.bucket)
        for item in result['Contents']:
            print(item['Key'])
        return result

    def file_upload(self, file, key):
        s3_client = self.get_client()
        return s3_client.upload_fileobj(file, self.bucket, key)

    def put_file(self, body, key):
        s3_client = self.get_client()
        return s3_client.put_object(Body=body, Bucket=self.bucket, Key=key)

    def aws_to_dataframe(self, key, extension):
        """Method for downloading, excel/csv/json files from AWS S3 Bucket and downloading them into a Dataframe.

        Args:
            s3_client ( boto3 client ): [description]
            key (string): String representing the file path
            extension ([type]): Extension of the file. Used to determine the file type to read into dataframe
        """
        s3_client = self.get_client()
        df = None
        with open('filename', 'wb') as s3_file:
            s3_client.download_fileobj(Bucket=self.bucket, Key=key,Fileobj=s3_file)
            if extension == 'csv':
                df = pandas.read_csv(s3_file.name)
            elif extension == 'xlsx':
                df = pandas.read_excel(s3_file.name)
            elif extension  == 'json':
                df = pandas.read_json(s3_file.name)
        return df

    def _get_total_bytes(self, s3_client ,key):
        """Method to return the total bytes for a particular AWS S3 Object

        Args:
            s3_client ([type]): S3 Bucket Client
            key ([type]): File path or key for the particular file

        Returns:
            [int]: Size of the item
        """
        result = s3_client.list_objects(Bucket=self.bucket)
        for item in result['Contents']:
            if item['Key'] == key:
                return item['Size']

    def get_object(self, key):
        """[summary]

        Args:
            key ([type]): [description]

        Returns:
            [type]: [description]
        """
        s3_client = self.get_client()
        total_bytes = self._get_total_bytes(s3_client, key)
        if total_bytes > 1000000:
            return self._get_object_range(s3_client, total_bytes)
        return s3_client.get_object(Bucket=self.bucket, Key=key)['Body'].read()

    def _get_object_range(s3_client, total_bytes):
        offset = 0
        while total_bytes > 0:
            end = offset + 999999 if total_bytes > 1000000 else ""
            total_bytes -= 1000000
            byte_range = 'bytes={offset}-{end}'.format(offset=offset, end=end)
            offset = end + 1 if not isinstance(end, str) else None
            yield s3_client.get_object(Bucket=self.bucket, Key=key, Range=byte_range)['Body'].read()


    def __repr__(self):
        return "AWS Bucket instance containing Configuration details"