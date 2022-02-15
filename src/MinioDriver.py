import mimetypes
import os
from shutil import copyfile, move
import uuid
from masonite.filesystem import FileStream


class MinioDriver:
    def __init__(self, application):
        self.application = application
        self.options = {}
        self.connection = None

    def set_options(self, options):
        self.options = options
        return self

    def get_connection(self):
        try:
            import boto3
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'boto3' library. Run 'pip install boto3' to fix this."
            )

        if not self.connection:
            self.connection = boto3.Session(
                aws_access_key_id=self.options.get("client"),
                aws_secret_access_key=self.options.get("secret"),
            )

        return self.connection

    def get_bucket(self):
        return self.options.get("bucket")

    def get_name(self, path, alias):
        extension = os.path.splitext(path)[1]
        return f"{alias}{extension}"

    def put(self, file_path, content):
        self.get_connection().resource(
            "s3", endpoint_url=self.options.get("path")
        ).Bucket(self.get_bucket()).put_object(Key=file_path, Body=content)
        return content

    def put_file(self, file_path, content, name=None):
        file_name = self.get_name(content.name, name or str(uuid.uuid4()))
        
        # get content type from content (file)
        mimetype = mimetypes.guess_type(content.name)[0]

        if hasattr(content, "get_content"):
            content = content.get_content()
        

        self.get_connection().resource(
            "s3", endpoint_url=self.options.get("path")
        ).Bucket(self.get_bucket()).put_object(
            Key=os.path.join(file_path, file_name), Body=content, ContentType=mimetype
        )
        return os.path.join(file_path, file_name)

    def get(self, file_path):
        try:
            return (
                self.get_connection()
                .resource("s3", endpoint_url=self.options.get("path"))
                .Bucket(self.get_bucket())
                .Object(file_path)
                .get()
                .get("Body")
                .read()
                .decode("utf-8", "ignore")
            )
        except self.missing_file_exceptions():
            pass

    def missing_file_exceptions(self):
        import boto3

        return (boto3.exceptions.botocore.errorfactory.ClientError,)

    def exists(self, file_path):
        try:
            self.get_connection().resource(
                "s3", endpoint_url=self.options.get("path")
            ).Bucket(self.get_bucket()).Object(file_path).get().get("Body").read()
            return True
        except self.missing_file_exceptions():
            return False

    def missing(self, file_path):
        return not self.exists(file_path)

    def stream(self, file_path):
        return FileStream(
            self.get_connection()
            .resource("s3", endpoint_url=self.options.get("path"))
            .Bucket(self.get_bucket())
            .Object(file_path)
            .get()
            .get("Body")
            .read(),
            file_path,
        )

    def copy(self, from_file_path, to_file_path):
        copy_source = {"Bucket": self.get_bucket(), "Key": from_file_path}
        self.get_connection().resource(
            "s3", endpoint_url=self.options.get("path")
        ).meta.client.copy(copy_source, self.get_bucket(), to_file_path)

    def move(self, from_file_path, to_file_path):
        self.copy(from_file_path, to_file_path)
        self.delete(from_file_path)

    def prepend(self, file_path, content):
        value = self.get(file_path)
        content = content + value
        self.put(file_path, content)
        return content

    def append(self, file_path, content):
        value = self.get(file_path) or ""
        value += content
        self.put(file_path, content)

    def delete(self, file_path):
        return (
            self.get_connection()
            .resource("s3", endpoint_url=self.options.get("path"))
            .Object(self.get_bucket(), file_path)
            .delete()
        )

    def store(self, file, name=None):
        full_path = name or file.hash_path_name()
        self.get_connection().resource(
            "s3", endpoint_url=self.options.get("path")
        ).Bucket(self.get_bucket()).put_object(Key=full_path, Body=file.stream())
        return full_path

    def make_file_path_if_not_exists(self, file_path):
        if not os.path.isfile(file_path):
            if not os.path.exists(os.path.dirname(file_path)):
                # Create the path to the model if it does not exist
                os.makedirs(os.path.dirname(file_path))

            return True

        return False
    
    def get_secure_url(self, file_path, expires=2600):
        # get s3 signed url from file path
        try:
            return self.get_connection().client(
                    "s3",
                    endpoint_url=self.options.get("path")
                ).generate_presigned_url(
                "get_object",
                Params={
                    'Bucket': self.get_bucket(),
                    'Key': file_path
                },
                ExpiresIn=expires,
            )
        except Exception as e:
            print(e)
        return None
