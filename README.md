# KoGaMa.py-Rewrite

KoGaMa.py-rewrite is a easy-to-use API wrapper for KoGaMa.

# About

* KoGaMa.py-Rewrite is an API-Wrapper for KoGaMa, a online game, re-written in Python 3.8+. The original version was called [KoGaMa.py](https://github.com/Ars3ne/kogama.py), and was made by Ars3ne.

* With this library, you can create your own projects, like Anti-Spams Bots or even Auto-Moderator Bots! Some features such as: Reporting Users, Sending Comments.. have cooldowns in order to prevent user abuse.

* If you're found abusing of KoGaMa.py-Rewrite to create projects that violates the [Terms of Use](https://www.kogama.com/help/terms-and-conditions/), we have the right to send a report to the KoGaMa Moderation Team, and you can get banned.
Features can also be disabled without previous warnings, in order to prevent user abuse.

* I, TheNoobPro44, don't take any responsability in case your account get banned for Innapropiated or Bad use of this library, you've been warned.

# Installation:
  In order to install this library, run the following command:
```
# Windows
pip install kogama.py-rewrite
```

### Example:
```python
from kogama import KoGaMa

client = KoGaMa("www")
client.Login("Admin", 12345678)
client.PostFeed("Hello, I'm using KoGaMa.py-Rewrite")
client.Logout()
```
-----
### Documentation
The documentation is still a W.I.P (Work In Progress)
