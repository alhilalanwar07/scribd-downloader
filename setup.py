from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="scribd-downloader",
    version="1.0.0",
    author="Assistant",
    author_email="assistant@example.com",
    description="A tool to download documents from Scribd",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alhilalanwar07/scribd-downloader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "scribd-downloader=scribd_downloader:main",
        ],
    },
    keywords="scribd downloader document pdf",
    project_urls={
        "Bug Reports": "https://github.com/alhilalanwar07/scribd-downloader/issues",
        "Source": "https://github.com/alhilalanwar07/scribd-downloader",
    },
)