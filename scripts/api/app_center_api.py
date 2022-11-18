import logging
from typing import Dict
import urllib

from api.api_wrapper import ApiWrapper
from constants import app_center_constants as APP_CENTER_CONSTANTS

class AppCenterApi:
  '''
  API that handles requests for appcenter
  '''
  def __init__(self, app_center_token: str) -> None:
    headers = {
      'X-API-Token': app_center_token,
      'accept': 'application/json',
      'Content-Type': 'application/json'
    }
    self.__api = ApiWrapper('api.appcenter.ms', headers=headers)
    self.__logger = logging.getLogger(__name__)

  def delete_app(self, app_name: str):
    '''
    Allows the user to delete the app
    
    Parameters
    ----------
    app_name : str
      App name to be deleted
    '''
    endpoint = f"{APP_CENTER_CONSTANTS.BASE_ENDPOINTS['app_base_endpoint']}/{app_name}"
    self.__api.delete(endpoint=endpoint)
    self.__logger.info(msg=f'Successfully deleted: {app_name}')

  def create_app(self, json: Dict):
    '''
    Public method to create the app

    Parameters
    ----------
    json : Dict
      Request body sent to the server

    Returns
    ----------
    data : Any
    '''
    endpoint = f"{APP_CENTER_CONSTANTS.BASE_ENDPOINTS['org_base_endpoint']}/apps"
    result = self.__api.post(endpoint=endpoint, json=json)
    return result.data

  def repo_config(self, app_name: str, json: Dict):
    '''
    Public method to link the app with a github repository

    Parameters
    ----------
    app_name : str
      App name to link the github repository
    data : str
      Request body sent to the server

    Returns
    ----------
    data : Any
    '''
    endpoint = f"{APP_CENTER_CONSTANTS.BASE_ENDPOINTS['app_base_endpoint']}/{app_name}/repo_config"
    result = self.__api.post(endpoint=endpoint, json=json)
    return result.data

  def update_app_config(self, app_name: str, branch: str, json: Dict):
    '''
    Public method to update the app with the pipeline obtained from Azure Key Vault

    Parameters
    ----------
    app_name : str
      App name to link the github repository
    branch : str
      Branch name to configure the pipeline
    json : dict
      Request body sent to the server

    Returns
    ----------
    data : Any
    '''
    formatted_branch = urllib.parse.quote_plus(f'{branch}')
    endpoint = (f"{APP_CENTER_CONSTANTS.BASE_ENDPOINTS['app_base_endpoint']}/{app_name}/branches/{formatted_branch}/config")
    result = self.__api.post(endpoint=endpoint, json=json)
    return result.data

  def upload_file_asset(self, app_name: str, json: Dict = {}):
    '''
    Public method to initiate the file upload for a given app

    Parameters
    ----------
    app_name : str
      App name to which the attachment has to be linked
    json : Dict
      Request body

    Returns
    ----------
    data : Any
      Response data
    '''
    endpoint = f"{APP_CENTER_CONSTANTS.BASE_ENDPOINTS['app_base_endpoint']}/{app_name}/file_asset"
    result = self.__api.post(endpoint=endpoint, json=json)
    return result.data
