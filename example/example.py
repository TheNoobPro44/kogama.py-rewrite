from Kogama.kogama import KoGaMa

k = KoGaMa("www")
k.Login("Username", "Password")
k.PostFeed("12345678", "Hii!")
k.Logout()
