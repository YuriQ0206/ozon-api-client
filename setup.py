from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ozon_api_client",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Ozon广告API的Python客户端",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ozon-api-client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "pytest-mock>=3.6.1",
            "flake8>=4.0.1",
            "black>=22.3.0",
            "isort>=5.10.1",
        ],
    },
)
