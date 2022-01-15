class failed_login(Exception):
    """ This exception is raised when a user fails to log in. """
    pass

class disallowed_url_input(Exception):
    """ This exception is raised when a user tries to send a message with an url (outside of KoGaMa Domains). """
    pass

class too_many_requests(Exception):
    """ This exception is raised when a user sends too many requests. """
    pass

class unauthorized_request(Exception):
    """ This exception is raised when a user tries to perform an unauthorized request. """
    pass