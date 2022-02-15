from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="minio_driver",
    version="0.1.6",
    author="Yubaraj Shrestha",
    author_email="companion.krish@outlook.com",
    description="Minio Storage Driver for Masonite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yubarajshrestha/minio-masonite-driver",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Masonite",
    ],
    packages=["minio_driver"],
    package_dir={"minio_driver": "src"},
    install_requires=[
        "masonite>=4.0,<5.0",
    ],
    license="MIT",
    include_package_data=True,
    keywords=["masonite", "storage", "minio", "masonite-storage-driver"],
)
