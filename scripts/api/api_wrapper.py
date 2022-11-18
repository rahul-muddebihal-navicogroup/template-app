import requests
import requests.packages
from typing import List, Dict, Union, Tuple
from enum import Enum
from json import JSONDecodeError
import logging

from api.exceptions import ApiException
from api.models import Result

class HTTP_METHOD(Enum):
  '''
  Enum for all supported HTTP Methods
  '''
  GET = 1
  POST = 2
  PUT = 3
  DELETE = 4

class ApiWrapper:
  '''
  API Wrapper Class for all api requests
  '''
  def __init__(self, hostname: str, headers = None, logger: logging.Logger = None) -> None:
    '''
    Constructor for Api Class

    Parameters
    ----------
    hostname : str
      Ex: api.github.com
    headers : Dict
      Headers for all the requests
    logger : Logger
      Logger
    '''
    self.__url = f'https://{hostname}/'
    self.__headers = headers
    self.__session = requests.Session()
    self.__logger = logger or logging.getLogger(__name__)

  def __do(self, http_method: str, endpoint: str, params: Dict = None, json: Dict = None, data: Union[Dict, List, Tuple, bytes] = None) -> Result:
    '''
    Perform HTTP Request and handle all exceptions
    '''
    full_url = self.__url + endpoint
    headers = self.__headers
    log_line_pre = f'method={http_method}, url={full_url}, params={params}'
    log_line_post = ', '.join((log_line_pre, 'success={}, status_code={}, message={}'))
    
    # Log HTTP params and perform an HTTP request, catching and re-raising any exceptions
    try:
      self.__logger.debug(msg=log_line_pre)
      response = self.__session.request(method=http_method, url=full_url, headers=headers, params=params, json=json, data=data)
    except requests.exceptions.HTTPError as e:
      self.__logger.error(msg=(str(e)))
      raise ApiException('Request failed due to HTTP error') from e
    except requests.exceptions.TooManyRedirects as e:
      self.__logger.error(msg=(str(e)))
      raise ApiException('Request failed due to too many redirects') from e
    except requests.exceptions.ConnectionError as e:
      self.__logger.error(msg=(str(e)))
      raise ApiException('Request failed due to connection error') from e
    except requests.exceptions.Timeout as e:
      self.__logger.error(msg=(str(e)))
      raise ApiException('Request failed due to timeout') from e
    except requests.exceptions.RequestException as e:
      self.__logger.error(msg=(str(e)))
      raise ApiException('Request failed due to request exception') from e
    
    # Deserialize JSON output to Python object, or return failed Result on exception
    try:
      data_out = response.json()
    except (ValueError, JSONDecodeError) as e:
      self.__logger.error(msg=log_line_post.format(False, None, e))
      raise ApiException('Bad JSON in response') from e

    # If status_code in 200-299 range, return success Result with data, otherwise raise exception
    is_success = 299 >= response.status_code >= 200
    log_line = log_line_post.format(is_success, response.status_code, response.reason)
    
    if is_success:
      self.__logger.debug(msg=log_line)
      return Result(response.status_code, message=response.reason, data=data_out)
    
    self.__logger.error(msg=log_line)
    raise ApiException(f'{response.status_code}: {response.reason}')

  def get(self, endpoint: str, params: Dict = None) -> Result:
    '''
    HTTP GET Method
    
    Parameters
    ----------
    endpoint : str
      The API endpoint which will be appended to the hostname to form the full url
    params : Dict
      Additional query parameters to the API
    
    Returns
    ----------
    result : Result
      Response from the API
    '''
    return self.__do(http_method=HTTP_METHOD.GET.name, endpoint=endpoint, params=params)

  def post(self, endpoint: str, params: Dict = None, json: Dict = None, data: Union[Dict, List, Tuple, bytes] = None) -> Result:
    '''
    HTTP POST Method
    
    Parameters
    ----------
    endpoint : str
      The API endpoint which will be appended to the hostname to form the full url
    params : Dict
      Additional query parameters to the API
    data : Dict
      Request body to be sent to the server
    
    Returns
    ----------
    result : Result
      Response from the API
    '''
    return self.__do(http_method=HTTP_METHOD.POST.name, endpoint=endpoint, params=params, json=json, data=data)

  def put(self, endpoint: str, params: Dict = None, json: Dict = None, data: Union[Dict, List, Tuple, bytes] = None) -> Result:
    '''
    HTTP PUT Method
    
    Parameters
    ----------
    endpoint : str
      The API endpoint which will be appended to the hostname to form the full url
    params : Dict
      Additional query parameters to the API
    data : Dict
      Request body to be sent to the server
    
    Returns
    ----------
    result : Result
      Response from the API
    '''
    return self.__do(http_method=HTTP_METHOD.PUT.name, endpoint=endpoint, params=params, json=json, data=data)

  def delete(self, endpoint: str, params: Dict = None, data: Dict = None) -> Result:
    '''
    HTTP DELETE Method
    
    Parameters
    ----------
    endpoint : str
      The API endpoint which will be appended to the hostname to form the full url
    params : Dict
      Additional query parameters to the API
    data : Dict
      Request body to be sent to the server
    
    Returns
    ----------
    result : Result
      Response from the API
    '''
    return self.__do(http_method=HTTP_METHOD.DELETE.name, endpoint=endpoint, params=params, data=data)
