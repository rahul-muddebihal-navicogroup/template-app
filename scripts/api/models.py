from typing import List, Dict

class Result:
  def __init__(self, status_code: int, message: str = '', data: List[Dict] = None) -> None:
    '''
    Result returned from API Wrapper

    Parameters
    ----------
    status_code : int
      Standard HTTP Status code
    message : str
      Human readable result
    data : List[Dict]
      Python List of Dictionaries (or maybe just a single Dictionary on error)
    '''
    self.status_code = int(status_code)
    self.message = str(message)
    self.data = data if data else []

class GithubResponse:
  '''
  Github Response Model
  '''
  def __init__(self, json, next_page = None):
    self.json = json
    self.next_page = next_page
