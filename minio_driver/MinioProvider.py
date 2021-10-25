"""A MinioProvider Service Provider."""

from masonite.managers.UploadManager import UploadManager
from masonite.provider import ServiceProvider
from masonite.view import View

from . import UploadMinioDriver
from masonite.helpers import config
from masonite.helpers.static import static
from masonite import Upload


class MinioProvider(ServiceProvider):
    """Provides Services To The Service Container."""

    wsgi = False

    def register(self):
        """Register objects into the Service Container."""
        self.app.bind('UploadMinioDriver', UploadMinioDriver)

    def boot(self, manager: UploadManager, view: View):
        """Boots services required by the container."""
        self.app.bind("Upload", manager.driver(config("storage").DRIVER))
        self.app.swap(Upload, manager.driver(config("storage").DRIVER))
        view.share({"static": static})
