#### Project description

**What is Minio-Driver?**
It's an extra storage driver for masonite. It adds support for minio server.

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

Add following configuration inside config/storage.py after `"disk": {"location": "storage/uploads"},`

```json
"minio": {
    "endpoint": env("MINIO_URL", "https://min.io"),
    "client": env("MINIO_CLIENT", "AxJz..."),
    "secret": env("MINIO_SECRET", "HkZj..."),
    "bucket": env("MINIO_BUCKET", "s3bucket"),
},
```

Add following keys in `.env`.

```
MINIO_CLIENT=
MINIO_SECRET=
MINIO_BUCKET=
MINIO_URL=
```

**Example**

```python

from masonite.request import Request
from masonite import Upload

def your_function(request: Request, upload: Upload):
    file = request.input('file')
    key = upload.store(file)
    file_url = upload.url(key, 3600) # url accepts file key and the expiry time for signed url
    return file_url
```

Enjoy ;)
