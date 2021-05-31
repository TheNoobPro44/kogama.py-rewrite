class NotAValidServer(Exception):
  """This exception is raised when a user inputs a invalid Server."""
  pass

class InvalidInformation(Exception):
  """This exception is raised when a user inputs a invalid information, such as Username or Password."""
  pass
class FailedLogin(Exception):
  """This exception is raised when a user fails to Login."""
  pass

class FeedError(Exception):
  """This exception is raised when a user fails to send a post in his Feed."""
  pass

class DisallowedURlInput(Exception):
  """This exception is raised when a user tries to send a message with links."""
  pass

class TooMuchRequests(Exception):
  """This exception is raised when a user sends too much requests."""
  pass

class ReasonNotFound(Exception):
  """This exception is raised when a report reason is not found."""
  pass

class TemplateNotFound(Exception):
  """This exception is raised when a user inputs a invalid template name."""
  pass

class FieldIsRequired(Exception):
  """This exception is raised when a required field is empty."""
  pass
