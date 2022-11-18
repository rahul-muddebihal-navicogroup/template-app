from typing import Dict

from api.api_wrapper import ApiWrapper
from constants import app_center_constants as APP_CENTER_CONSTANTS

class UploadAttachmentsApi:
  def __init__(self, app_center_token: str, host_name: str) -> None:
    headers = {
      'X-API-Token': app_center_token,
      'accept': 'application/json',
      'Content-Type': 'application/json'
    }
    self.__api = ApiWrapper(host_name, headers=headers)

  def upload_metadata(self, **kwargs):
    '''
    Upload file metadata
    
    Parameters
    ----------
    json : dict
      Request body
    kwargs : dict
      [id], [file_name], [file_size], [url_encoded_token], [json]
    '''
    id = kwargs.get('id', '')
    file_name = kwargs.get('file_name', '')
    file_size = kwargs.get('file_size', 0)
    url_encoded_token = kwargs.get('url_encoded_token', '')
    json = kwargs.get('json', {})

    endpoint = f"{APP_CENTER_CONSTANTS.UPLOAD_BASE_URLS['set_metadata']}/{id}/?file_name={file_name}&file_size={file_size}&token={url_encoded_token}"
    result = self.__api.post(endpoint=endpoint, json=json)
    return result.data

  def upload_chunk(self, data, **kwargs):
    '''
    Upload file chunk
    
    Parameters
    ----------
    data : bytes
      Bytes of data to be uploaded
    kwargs : dict
      [id], [chunk_number], [url_encoded_token]
    '''
    id = kwargs.get('id', '')
    chunk_number = kwargs.get('chunk_number', 0)
    url_encoded_token = kwargs.get('url_encoded_token', '')

    endpoint = f"{APP_CENTER_CONSTANTS.UPLOAD_BASE_URLS['upload_chunk']}/{id}?block_number={chunk_number}&token={url_encoded_token}"
    result = self.__api.post(endpoint=endpoint, data=data)
    return result.data

  def upload_finished(self, **kwargs):
    '''
    Upload finished
    
    Parameters
    ----------
    json: dict
      Request body
    kwargs : dict
      [id], [url_encoded_token], [json]
    '''
    id = kwargs.get('id', '')
    url_encoded_token = kwargs.get('url_encoded_token', '')
    json = kwargs.get('json', {})

    endpoint = f"{APP_CENTER_CONSTANTS.UPLOAD_BASE_URLS['upload_finished']}/{id}?token={url_encoded_token}"
    result = self.__api.post(endpoint=endpoint, json=json)
    return result.data
