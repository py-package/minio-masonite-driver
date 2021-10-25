from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="minio_driver",
    version='0.0.7',
    packages=['minio_driver'],
    author="Yubaraj Shrestha",
    author_email="companion.krish@outlook.com",
    install_requires=[
        'masonite',
    ],
    description="Minio Storage Driver for Masonite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    include_package_data=True,
    keywords=["masonite", "storage", "minio", "masonite-storage-driver"]
)
