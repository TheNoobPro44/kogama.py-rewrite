import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KoGaMa.py-Rewrite",
    packages = ['Kogama'],
    version="0.6",
    author="TheNoobPro44",
    license="MIT",
    description="KoGaMa.py-Rewrite is an API-Wrapper for the KoGaMa Website API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheNoobPro44/KoGaMa.py-Rewrite/",
    project_urls={
        "Documentation": "https://thenoobpro44.gitbook.io/kogama-py-rewrite/",
        "Bug Tracker": "https://github.com/TheNoobPro44/KoGaMa.py-Rewrite/issues"
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
