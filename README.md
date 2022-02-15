#### Project description

**What is Minio-Driver?**

It's an extra storage driver support for Minio in masonite 4.

**Setup**

Install package using pip:

```shell
pip install minio-driver
```

Add provider inside config/providers.py.

```python
from minio_driver.MinioProvider import MinioProvider

PROVIDERS = [
    ...,
    # Application Providers
    MinioProvider,
]
```

**Storage Config**

Add following configuration inside config/filesystem.py after `"s3": {...},`

```python
"minio": {
    "driver": "minio",
    "client": env("MINIO_CLIENT"),
    "secret": env("MINIO_SECRET"),
    "bucket": env("MINIO_BUCKET"),
    "path": env("MINIO_ENDPOINT"),
},
```

Add following keys in `.env`.

```shell
MINIO_CLIENT=
MINIO_SECRET=
MINIO_BUCKET=
MINIO_ENDPOINT=
```

Update the storage driver value to `minio` in `.env`

```shell
STORAGE_DRIVER=minio
```

**Example**

```python
from masonite.controllers import Controller
from masonite.filesystem import Storage
from masonite.request import Request

class YourController(Controller):

    def your_function(self, request: Request, storage: Storage):
        file = request.input('file')

        # storing file
        path = storage.disk("minio").put_file('your_file_directory', file)

        # getting file_url from storage
        file_url = storage.disk("minio").get_secure_url(path)
        return file_url
```

Enjoy ;)
