from Kogama.kogama import KoGaMa

k = KoGaMa("WWW") # Selecting our server.. (WWW or BR)
k.Login("MyCoolUsername", "Really_Secured_Password") # Loging into our account.
k.PostFeed("12345678", "Hii! How are you! ^^") # We input the ID of the user we want to post the feed message on, then our message.
k.run() # Keeping the player Alive/Online..
