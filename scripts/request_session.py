from requests import Session, Response, exceptions

class RequestSession:
  '''
  A class that initializes a session using requests and provides methods to perform API calls
  '''

  def __init__(self, headers: dict[str, str]) -> None:
    '''
    Initialize the session object with appropriate headers
    '''
    self.session = Session()
    self.session.headers = headers

  def get(self, url: str, *args) -> Response:
    '''
    HTTP GET Method
    Parameters
    ----------
    url : str
      The API url
    '''
    try:
      return self.session.get(url)
    except exceptions.HTTPError as err:
      raise SystemExit(err)

  def post(self, url: str, data, *args) -> Response:
    '''
    HTTP POST Method
    Parameters
    ----------
    url : str
      The API url
    data: str
      The request body to be sent to the server
    '''
    try:
      return self.session.post(url, data)
    except exceptions.HTTPError as err:
      raise SystemExit(err)

  def delete(self, url: str, *args) -> Response:
    '''
    HTTP DELETE Method
    Parameters
    ----------
    url : str
      The API url
    '''
    try:
      return self.session.delete(url)
    except exceptions.HTTPError as err:
      raise SystemExit(err)

  def put(self, url: str, data, *args) -> Response:
    '''
    HTTP PUT Method
    Parameters
    ----------
    url : str
      The API url
    data: str
      The request body to be sent to the server
    '''
    try:
      return self.session.put(url, data)
    except exceptions.HTTPError as err:
      raise SystemExit(err)
