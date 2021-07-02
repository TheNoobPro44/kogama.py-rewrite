from Kogama.kogama import KoGaMa

k = KoGaMa("www") # Selecting our server.. (WWW or BR)
k.Login("MyCoolUsername", "ReallySecuredPassword") # Loging into our account.
k.PostFeed("12345678", "Hii! How are you! ^^") # We input the ID of the user we want to post the feed message on, then our message.
k.run() # Keeping the player alive / online..
