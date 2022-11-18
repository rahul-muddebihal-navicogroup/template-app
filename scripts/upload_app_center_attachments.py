'''
Reference: https://github.com/microsoft/appcenter-cli/blob/a240f462cc62aa48ecbc11ac4480e3d7ed0b477e/appcenter-file-upload-client-node/src/ac-fus-uploader.ts#L337
'''
import os
import json
import math
import datetime
import sys

from api.app_center_api import AppCenterApi
from api.upload_attachments_api import UploadAttachmentsApi
from file import File
from constants import app_center_constants as APP_CENTER_CONSTANTS

class UploadAppCenterAttachments:
  '''
  Class to upload attachments to app center
  '''
  def __init__(self, environment: str) -> None:
    self.__environment = environment
    self.__app_center_api = AppCenterApi(app_center_token=APP_CENTER_CONSTANTS.APP_CENTER_TOKEN)
    self.__upload_attachments_api = None
    self.__upload_success_response = {}
    self.__max_number_of_concurrent_uploads = 10
    self.__file = None
    self.__upload_data = {
      'asset_id': '00000000-0000-0000-0000-000000000000',
      'blob_partitions': 0,
      'callback_url': '',
      'correlation_id': '00000000-0000-0000-0000-000000000000',
      'correlation_vector': '',
      'chunk_size': 0,
      'log_to_console': False,
      'tenant': '',
      'url_encoded_token': '',
      'total_blocks': 0,
      'upload_domain': '',
      'file_name': '',
      'file_size': 0,
      'file_path': ''
    }
    self.__upload_status = {
      'auto_retry_count': 0,
      'average_speed': 0,
      'blocks_completed': 0,
      'chunks_failed_count': 0,
      'chunk_queue': [],
      'connected': True,
      'end_time': datetime.datetime.now(),
      'inflight_set': set(),
      'abort_controller': '',
      'max_error_count': 20,
      'service_callback': {
        'auto_retry_count': 5,
        'auto_retry_delay': 1,
        'failure_count': 0,
      },
      'start_time': datetime.datetime.now(),
      'state': '',
      'transfer_queue_rate': [],
    }

  def __enqueue_chunks(self, chunks):
    '''
    Private method to keep track of chunks

    Parameters
    ----------
    chunks : list(int)
      Iterate through list of chunks that must be uploaded and append it to the chunk queue
    '''
    if len(self.__upload_status['chunk_queue']) == 0:
      self.__upload_status['chunk_queue'] = chunks
      return

    status = self.__upload_status
    filtered_chunks = [chunk for chunk in chunks if chunk not in status['chunk_queue']]
    self.__upload_status['chunk_queue'].append(filtered_chunks)

  def __finish_upload(self):
    '''
    Private method to verify the upload and make an API call to finish upload
    '''
    print('Verifying upload on server')

    id = self.__upload_data['asset_id']
    url_encoded_token = self.__upload_data['url_encoded_token']

    result = self.__upload_attachments_api.upload_finished(id=id, url_encoded_token=url_encoded_token)

    self.__upload_success_response = result
    print('Successfully uploaded the file')
    print()

  def __file_chunk(self, start, end):
    '''
    Private method to read a file in chunks

    Parameters
    ----------
    start : int
      File seek to the start position as mentioned by start
    end : int
      File seek to the end position as mentioned by end
    
    Returns
    ----------
    chunk : bytes
      A chunk of file based on start and end position
    '''
    return self.__file.read_file_chunk(start=start, end=end)

  def __upload_chunk(self, chunk, chunk_number):
    '''
    Private method to upload a chunk of file

    Parameters
    ----------
    chunk : bytes
      A chunk of file that should be uploaded
    chunk_number : int
      Keep track of chunk number and passing to the API
    
    Returns
    ----------
    chunk : bytes
      A chunk of file based on start and end position
    '''

    self.__upload_status['inflight_set'].add(chunk_number)
    print('Starting upload for chunk: ', chunk_number)

    # Obtain the necessary information from the response of initiate file asset upload
    id = self.__upload_data['asset_id']
    url_encoded_token = self.__upload_data['url_encoded_token']

    # Upload the chunk to the file server
    result = self.__upload_attachments_api.upload_chunk(data=chunk, id=id, chunk_number=chunk_number, url_encoded_token=url_encoded_token)

    print(f'ChunkSucceeded: {chunk_number}. ')
    self.__upload_status['inflight_set'].remove(chunk_number)

    # Recursively call the upload method to get the next chunk 
    self.__single_threaded_upload()

  def __single_threaded_upload(self):
    '''
    Private method to find the chunk of file and trigger the upload chunk
    '''

    # If the condition is true, trigger the finish upload
    if len(self.__upload_status['chunk_queue']) == 0 and len(self.__upload_status['inflight_set']) == 0:
      self.__upload_status['end_time'] = datetime.datetime.now()
      self.__finish_upload()
      return

    # Pop out the topmost chunk number from the queue
    chunk_number = self.__upload_status['chunk_queue'].pop()

    # Find the start and end positions of the file
    start = (chunk_number - 1) * self.__upload_data['chunk_size'];
    end = min(chunk_number * self.__upload_data['chunk_size'], self.__upload_data['file_size']);
    chunk = self.__file_chunk(start, end)

    # Trigger chunk upload
    self.__upload_chunk(chunk, chunk_number)

  def __start_upload(self):
    '''
    Private method to start uploading the file
    '''
    print('Starting single threaded upload with chunks: ', self.__upload_status['chunk_queue'])
    concurrent_uploads = min(self.__max_number_of_concurrent_uploads, len(self.__upload_status['chunk_queue']))
    
    for i in range(concurrent_uploads):
      self.__single_threaded_upload()
    
    return self.__upload_success_response

  def __upload_file_metadata(self):
    upload_domain = self.__upload_data['upload_domain']
    id = self.__upload_data['asset_id']
    url_encoded_token = self.__upload_data['url_encoded_token']
    file_name = self.__upload_data['file_name']
    file_size = self.__upload_data['file_size']

    # Create upload attachments api
    domain = upload_domain[8:]
    self.__upload_attachments_api = UploadAttachmentsApi(app_center_token=APP_CENTER_CONSTANTS.APP_CENTER_TOKEN, host_name=domain)

    result = self.__upload_attachments_api.upload_metadata(id=id, file_name=file_name, file_size=file_size, url_encoded_token=url_encoded_token)

    self.__upload_data['chunk_size'] = result.get('chunk_size')
    self.__upload_data['blob_partitions'] = result.get('blob_partitions')
    self.__upload_data['total_blocks'] = math.ceil(file_size / self.__upload_data['chunk_size'])

    print('Chunks to upload: ', self.__upload_data['total_blocks'])

    # Enqueue chunks
    self.__enqueue_chunks(result.get('chunk_list'))

    # Returns the success response
    return self.__start_upload()

  def __upload_file_asset(self, app_name: str):
    '''
    Private method to upload file asset

    Parameters
    ----------
    app_name : str
      App name to which the file metadata

    Returns
    ----------
    response : Any
      Success response that uploadId and filename and file server location
    '''
    result = self.__app_center_api.upload_file_asset(app_name=app_name)

    # Obtain the necessary information from the response of initiate file asset upload
    self.__upload_data['upload_domain'] = result.get('uploadDomain')
    self.__upload_data['url_encoded_token'] = result.get('urlEncodedToken')
    self.__upload_data['asset_id'] = result.get('id')

    # Upload file metadata
    return self.__upload_file_metadata()

  def init_app(self, app_name: str, file: File):
    '''
    Public method to initiate uploading the file asset

    Parameters
    ----------
    app_name : str
      App name to which the file has to be linked
    file : File
      File object
    
    Returns
    ----------
    response : Any
      Success response after the file has finished uploading the file
    '''
    self.__file = file
    self.__upload_data['file_name'] = file.file_name
    self.__upload_data['file_path'] = file.file_path
    self.__upload_data['file_size'] = file.file_size
    
    return self.__upload_file_asset(app_name)


def main():
  arg_length = len(sys.argv)

  # Defaults to development environment
  environment = APP_CENTER_CONSTANTS.DEVELOPMENT_ENVIRONMENT

  # If non-dev environment, argument should be passed
  if arg_length == 2:
    environment = str(sys.argv[0])

  upload_app_center_attachments_app = UploadAppCenterAttachments(environment=environment)
  
  # Invoke the upload_app_center_attachments app
  file = File('/Users/rahulmuddebihal/Downloads/Empower_OEM4_Adhoc-2.mobileprovision')
  upload_app_center_attachments_app.init_app(app_name='hello-ios', file=file)

if __name__ == '__main__':
  main()
