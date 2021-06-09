# KoGaMa.py-Rewrite

[![Python Version](https://img.shields.io/badge/python-%E2%89%A53.8-yellow.svg)](https://www.python.org/downloads/)  [![Pypi](https://img.shields.io/pypi/v/KoGaMa.py-Rewrite)](https://pypi.org/project/KoGaMa.py-Rewrite/)  ![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)  [![Downloads](https://static.pepy.tech/badge/KoGaMa.py-Rewrite)](https://static.pepy.tech/badge/KoGaMa.py-Rewrite)  

KoGaMa.py-rewrite is an easy to use API-wrapper for KoGaMa.

# About

* KoGaMa.py-Rewrite is an API-Wrapper for KoGaMa, a online game, re-written in Python 3.8+. The original version was called [KoGaMa.py](https://github.com/Ars3ne/kogama.py), and was made by Ars3ne.

* With this library, you can create your own projects, like Anti-Spams Bots or even Auto-Moderator Bots! Some features such as: Reporting Users, Sending Comments.. have cooldowns in order to prevent user abuse.

* If you're found abusing of KoGaMa.py-Rewrite to create projects that violates the [Terms of Use](https://www.kogama.com/help/terms-and-conditions/), we have the right to send a report to the KoGaMa Moderation Team, and you can get banned.
Features can also be disabled without previous warnings, in order to prevent user abuse.

* I, TheNoobPro44, don't take any responsability in case your account get banned for Innapropiated or Bad use of this library, you've been warned.

* The only working versions are above 0.3.9!

### Key Features
- Easy to Use.
- Alot of Features.
- No Dependencies.

# Installation:
  In order to install this library, run the following command:
```
# Windows
pip install KoGaMa.py-Rewrite
```

```
# Unix/macOS
python3 -m pip install "KoGaMa.py-Rewrite"
```

### Example:
```python
from Kogama.kogama import KoGaMa

client = KoGaMa("www")
client.Login("Admin", "MySecretPassword")
client.PostFeed(12345678, "Hello, I'm using KoGaMa.py-Rewrite")
client.Logout()
```
-----

### Credits
- Tokeeto :: Helped me sending requests to the server & debbuging.
- MD :: Debbuging Code.
- Junko :: Debbuging Code.

### Documentation
 * The official documentation of KoGaMa.py-Rewrite can be found at:
     https://thenoobpro44.gitbook.io/kogama-py-rewrite/
