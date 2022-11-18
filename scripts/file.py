import base64
import os

class File:
  '''
  Class to create a File 
  '''
  def __init__(self, file_path: str) -> None:
    self.__file_path = file_path
    self.__file_name = os.path.basename(file_path)
    self.__file_size = self.__get_file_size(file_path=file_path)

  def __get_file_size(self, file_path: str):
    file_stats = os.stat(file_path)
    return file_stats.st_size

  @property
  def file_name(self):
    return self.__file_name

  @property
  def file_path(self):
    return self.__file_path

  @property
  def file_size(self):
    return self.__file_size

  def encode_base64(self):
    '''
    Read the contents of the file and encode the file using Base 64
    
    Returns
    ----------
    encoded_string : bytes
      Encoded string in bytes
    '''
    encoded_string = ''
    with open(self.__file_path, 'rb') as file:
      encoded_string = base64.b64encode(file.read())
    return encoded_string
  
  def decode_base64(self, data: bytes, file_path: str):
    '''
    Read the data obtained from vault and decode the contents using Base 64 and create and write to the file locally

    Parameters
    ----------
    data : byte
      Encoded string in bytes
    file_name : str
      Save the file locally
    '''
    with open(f'{file_path}', 'wb') as file:
      file.write(base64.b64decode(data))

  def read_file_chunk(self, start: int, end: int):
    '''
    Private method to read a file in chunk

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
    file = open(f'{self.__file_path}', 'rb')
    file.seek(start, 0)
    return file.read(end-start)
