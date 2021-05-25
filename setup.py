import setuptools
import os

README = open("README.md").read()

setuptools.setup(
  name = 'KoGaMa.py-Rewrite',
  version = '0.1',
  license='MIT',
  description = 'An API wrapper for KoGaMa re-written in Python.',
  long_description = README,
  long_description_content_type="text/markdown",
  author = 'TheNoobPro44',
  author_email = 'TheNewbiePro44@gmail.com',
  url = 'https://github.com/TheNoobPro44/KoGaMa.py-Rewrite/',
  keywords = ['kogama', 'api'],
  python_requires=">=3.5.3",
  install_requires=[
          'requests',
          'beautifulsoup4',
          'lxml',
      ],
  classifiers=[
    'Development Status :: 1 - Development',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9.5',
    'Programming Language :: Python :: 3.9.5',
  ],
)
