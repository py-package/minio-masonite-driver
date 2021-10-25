from masonite.contracts.UploadContract import UploadContract
from masonite.drivers.upload.BaseUploadDriver import BaseUploadDriver
from masonite.exceptions import DriverLibraryNotFound
from masonite.managers.UploadManager import UploadManager
from masonite.helpers import config
import os


class UploadMinioDriver(BaseUploadDriver, UploadContract):

    def __init__(self, upload: UploadManager):
        self.upload = upload
        self.config = config("storage")

    def store(self, fileitem, filename=None, location=None):
        """Store the file into minio server.

        Arguments:
            fileitem {cgi.Storage} -- Storage object.

        Keyword Arguments:
            location {string} -- The location on disk you would like to store the file. (default: {None})
            filename {string} -- A new file name you would like to name the file. (default: {None})

        Raises:
            DriverLibraryNotFound -- Raises when the boto3 library is not installed.

        Returns:
            string -- Returns the file name just saved.
        """
        try:
            import boto3
        except ImportError:
            raise DriverLibraryNotFound(
                'Could not find the "boto3" library. Please pip install this library by running "pip install boto3"'
            )

        driver = self.upload.driver("disk")
        driver.accept_file_types = self.accept_file_types
        driver.store(fileitem, filename=filename, location="storage/temp")
        file_location = driver.file_location

        if filename is None:
            filename = self.get_name(fileitem)

        # Check if is a valid extension
        self.validate_extension(self.get_name(fileitem))

        session = boto3.Session(
            aws_access_key_id=self.config.DRIVERS["minio"]["client"],
            aws_secret_access_key=self.config.DRIVERS["minio"]["secret"],
        )

        client = session.client(
            "s3",
            endpoint_url=self.config.DRIVERS["minio"]["endpoint"],
        )

        if location:
            location = os.path.join(location, filename)
        else:
            location = os.path.join(filename)

        client.upload_file(file_location, self.config.DRIVERS["minio"]["bucket"], location)

        return filename
