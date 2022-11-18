import json
import sys
import os
from copy import deepcopy
from typing import Dict, List
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from constants import key_vault_constants as KEY_VAULT_CONSTANTS
from file import File
from upload_app_center_attachments import UploadAppCenterAttachments

'''
To run the app
For development mode:
python3 key_vault.py
For non-dev mode:
python3 key_vault.py <arg> # arg can be anything except dev
Ex: python3 key_vault.py qa
'''

class KeyVault():
  '''
  Class to create and retrieve secrets from Azure Key Vault
  '''
  def __init__(self, environment) -> None:
    self.__environment = environment
    self.__secret_clients = {
      'dev': {
        'common_vault_url': None,
        'oem_vault_url': None,
        'common_client': None,
        'oem_client': None,
      },
      'qa': {
        'common_vault_url': None,
        'oem_vault_url': None,
        'common_client': None,
        'oem_client': None,
      },
      'prod': {
        'common_vault_url': None,
        'oem_vault_url': None,
        'common_client': None,
        'oem_client': None,
      }
    }

  def __authenticate_key_vault(self, env_name: str):
    '''
    Private method to authenticate the users via the default method

    Parameters
    ----------
    env_name : str
      Environment name for which the common vault url and oem specific vault urls are utilized
    '''

    # If environment variable does not contain AZURE_TENANT_ID use the default Azure Tenant ID
    if not os.environ.get('AZURE_TENANT_ID'):
      os.environ['AZURE_TENANT_ID'] = KEY_VAULT_CONSTANTS.TENANT_ID

    '''
    Store the common and OEM specific vault url for each environment in a dictonary
    So that user is not prompted for every app

    If environment is dev, default constants are utilized.
    Else, user is promted with questions
    '''
    if self.__environment != KEY_VAULT_CONSTANTS.DEVELOPMENT_ENVIRONMENT:
      if not self.__secret_clients[env_name]['common_vault_url'] and not self.__secret_clients[env_name]['oem_vault_url']:
        self.__secret_clients[env_name]['common_vault_url'] = input(f'Enter your {env_name} Environment vault url for Common Variables: \n')
        print()
        self.__secret_clients[env_name]['oem_vault_url'] = input(f'Enter your {env_name} Environment vault url for OEM Specific Variables: \n')
        print()
    else:
      self.__secret_clients[env_name]['common_vault_url'] = KEY_VAULT_CONSTANTS.COMMON_ENV_VAULT_URL
      self.__secret_clients[env_name]['oem_vault_url'] = KEY_VAULT_CONSTANTS.OEM_VAULT_URL

    credential = DefaultAzureCredential()
    self.__secret_clients[env_name]['common_client'] = SecretClient(vault_url=self.__secret_clients[env_name]['common_vault_url'], credential=credential)
    self.__secret_clients[env_name]['oem_client'] = SecretClient(vault_url=self.__secret_clients[env_name]['oem_vault_url'], credential=credential)

  '''
  Set secrets in Key Vault
  '''
  def __set_secret(self, secret_client, secret_name: str, secret_value, **kwargs):
    '''
    Private method to set secret in the Key Vault

    Parameters
    ----------
    secret_client : Any
      Secret Client contains the vault url and other properties/methods to perform operations on the key vault
    secret_name : str
      Secret key name to add/update
    secret_value : str
      Secret key value to add/update the value of the secret_name
    kwargs : dict
      Other arguments that can be passed such as tags, content_type, enabled flag
    '''
    secret = secret_client.set_secret(secret_name, secret_value, **kwargs)

  def __set_secrets_list(self, secret_client, list: List, **kwargs):
    '''
    Private method to set a list of secrets

    Parameters
    ----------
    secret_client : Any
      Secret Client contains the vault url and other properties/methods to perform operations on the key vault
    list : list
      A list that will be iterated over and added/updated in the key vault
    kwargs : dict
      Other arguments that can be passed such as tags, content_type, enabled flag
    '''
    for secret in list:
      name = secret.get('name', 'name')
      secret_value = secret.get('value', 'value')
      secret_name = f'{name.replace("_", "-")}'
      self.__set_secret(secret_client=secret_client, secret_name=secret_name, secret_value=secret_value, **kwargs)

  def __set_key_vault(self, json_data: Dict, env_name: str, key_vault_type = 'common'):
    '''
    Private method to iterate through the data and extract arguments such as content_type, tags, etc

    Parameters
    ----------
    json : dict
      JSON data from the [file].json
    env_name : str
      Environment to store the secrets into
    key_vault_type : str
      Used to set the appropriate secret client based on the vault_type
    '''

    if key_vault_type == 'common':
      secret_client = self.__secret_clients[env_name]['common_client']
    else:
      secret_client = self.__secret_clients[env_name]['oem_client']

    # Construct the content type. Very important feature, used extensively while extracting the secrets from the vault
    for key, value in json_data.items():
      if isinstance(value, type({})):
        content_type = 'dict'
      elif isinstance(value, type([])):
        content_type = 'list'
      elif isinstance(value, type(True)):
        content_type = 'bool'
      elif isinstance(value, type('')):
        content_type = 'str'
      elif isinstance(value, type(b'')):
        content_type = 'cert'
        value = value.decode('utf-8')
      else:
        content_type = type(value)
      
      # Construct the tags
      tags = {
        f'{key}': f'{key_vault_type}_{key}'
      }

      enabled = True

      if content_type == 'list':
        self.__set_secrets_list(
          secret_client=secret_client, 
          list=value, 
          content_type=content_type, 
          tags=tags, 
          enabled=enabled
        )
      else:
        secret_value = json.dumps(value) if content_type == 'dict' else value
        secret_name = f'{key.replace("_", "-")}'
        self.__set_secret(
          secret_client=secret_client, 
          secret_name=secret_name, 
          secret_value=secret_value, 
          content_type=content_type, 
          tags=tags, 
          enabled=enabled
        )

  def __set_certificates(self, env_name: str):
    '''
    Obtain the file path for the certificates/provision files stored on the users machine
    If environment is dev, default constants are utilized.
    Else, user is promted with questions

    Parameters
    ----------
    env_name : str
      Environment to store the secrets into
    '''
    if self.__environment != KEY_VAULT_CONSTANTS.DEVELOPMENT_ENVIRONMENT:
      mobile_provision_path = input(f'Please enter the Absolute Path of your Mobile Provision that is used for {env_name} Environment: \n')
      print()
      p12_certificate_path = input(f'Please enter the Absolute Path of your p12 Certificate that is used for {env_name} Environment: \n')
      print()
      keystore_certificate_path = input(f'Please enter the Absolute Path of your KeyStore Certificate that is used for {env_name} Environment: \n')
      print()
      p12_certificate_password = input(f'Please enter the Password for your p12 Certificate that is used for {env_name} Environment: \n')
      print()
      keystore_certificate_password = input(f'Please enter the Password for your KeyStore Certificate that is used for {env_name} Environment: \n')
      print()
    else:
      mobile_provision_path = KEY_VAULT_CONSTANTS.MOBILE_PROVISON_PATH
      p12_certificate_path = KEY_VAULT_CONSTANTS.P12_CERTIFICATE_PATH
      keystore_certificate_path = KEY_VAULT_CONSTANTS.KEY_STORE_CERTIFICATE_PATH
      p12_certificate_password = KEY_VAULT_CONSTANTS.P12_CERTIFICATE_PASSWORD
      keystore_certificate_password = KEY_VAULT_CONSTANTS.KEY_STORE_CERTIFICATE_PASSWORD

    # Construct File objects
    mobile_provision_file = File(file_path=mobile_provision_path)
    p12_certificate_file = File(file_path=p12_certificate_path)
    keystore_certificate_file = File(file_path=keystore_certificate_path)

    # Construct the dictionary after encode the file into base64
    data = {
      'mobileprovision': mobile_provision_file.encode_base64(),
      'p12': p12_certificate_file.encode_base64(),
      'keystore': keystore_certificate_file.encode_base64(),
      'mobileprovision_filename': mobile_provision_file.file_name,
      'p12_filename': p12_certificate_file.file_name,
      'keystore_filename': keystore_certificate_file.file_name,
      'p12_password': p12_certificate_password,
      'keystore_password': keystore_certificate_password
    }

    print(f"Setting OEM Certificates in Key Vault for {env_name}")
    self.__set_key_vault(json_data=data, env_name=env_name, key_vault_type='oem')
    print(f"Successfully set OEM Certificates in Key Vault for {env_name}")

  def set_vault_secrets(self):
    '''
    Public method to set secrets in Azure Key Vault
    '''

    '''
    Iterate through each environment and read the json data from environment specific file and add/update secrets in Azure Key vault
    '''
    for env in KEY_VAULT_CONSTANTS.ENVIRONMENTS:
      env_name = env['name']
      self.__authenticate_key_vault(env_name=env_name)
      # Do the same process for common env secrets and oem env secrets
      for i in range(2):
        if i == 0:
          file_name = KEY_VAULT_CONSTANTS.BASE_COMMON_FILE_NAME
          key_vault_type = 'common'
        else:
          file_name = KEY_VAULT_CONSTANTS.BASE_OEM_FILE_NAME
          key_vault_type = 'oem'
      
        full_file_name = f"{file_name}_{env['name']}.json"
        ADDITIONAL = 'template/scripts'
        # Constuct the appropriate file name based on the environment
        if self.__environment != KEY_VAULT_CONSTANTS.DEVELOPMENT_ENVIRONMENT:
          file_path = os.path.join(os.getcwd(), ADDITIONAL, KEY_VAULT_CONSTANTS.KEY_VAULT_TEMPLATE_PATH, full_file_name)
        else:
          file_path = os.path.join(os.getcwd(), ADDITIONAL, KEY_VAULT_CONSTANTS.KEY_VAULT_TEMPLATE_PATH, full_file_name)

        # Read the json file
        file = open(file_path)

        # Load the json data
        json_data = json.load(file)

        print(f"Setting {key_vault_type} Key Vault for {env['name']}")
        self.__set_key_vault(json_data=json_data, env_name=env_name, key_vault_type=key_vault_type)
        print(f"Successfully set {key_vault_type} Key Vault for {env['name']}")
        print()

    # Get certificate path and upload it to Key Vault
    self.__set_certificates(env_name=env_name)

  '''
  Get secrets in Key Vault
  '''

  '''
  1. Upload the file
  2. Retrieve the success response from upload_attachment
  3. Append the uploadId, filename and password(if any) to the response object
  4. Return the response object to appcenter for pipeline config
  '''
  def __handle_file_uploads(self, data, app_name: str, env_name: str, tag_key: str):
    '''
    Private method to handle base 64 encoded data stored in Key Vault

    Parameters
    ----------
    data : byte
      Encoded string in bytes
    app_name : str
      App name to upload the decoded file
    env_name : str
      Save the file locally as [env_name].[tag_key]
    tag_key : str
      Used as an extension  
    '''
    
    # Create File object
    file_name = f'{env_name}.{tag_key}'
    file_path = os.path.join(os.getcwd(), file_name)
    # Create an empty file
    with open(file_path, 'w') as f:
      pass
    
    file = File(file_path=file_path)

    # Decode and download the file
    file.decode_base64(data=data, file_path=file_path)

    file = File(file_path=file_path)

    # Create UploadAttachments Object and upload file
    upload_app_center_attachments = UploadAppCenterAttachments(self.__environment)
    result = upload_app_center_attachments.init_app(app_name=app_name, file=file)

    if result['error'] == False:
      # Step 3. Extract upload id and file name
      if tag_key == 'mobileprovision':
        self.__provisioning_profile_upload_id = os.path.basename(result['location'])
        self.__provisioning_profile_filename = os.path.basename(result['absolute_uri'])
      elif tag_key == 'p12':
        self.__certificate_upload_id = os.path.basename(result['location'])
        self.__certificate_filename = os.path.basename(result['absolute_uri'])
      
      # We can delete the locally created file
      os.remove(file_path)
      print(f'Successfully deleted {file_name}')
      print()
    else:
      # Upload failed
      print('Upload Failed. Try again later')

  def __construct_certificate_params(self, response, **kwargs):
    '''
    Private method to construct params related to certificates and provisioning

    Parameters
    ----------
    response : dict
      Update the response dictionary
    kwargs : dict
      Other arguments used to update the response dictionary
    
    Returns
    ----------
    response : dict
      Updated response dictionary
    '''
    response['toolsets']['xcode']['provisioningProfileUploadId'] = self.__provisioning_profile_upload_id
    response['toolsets']['xcode']['provisioningProfileFilename'] = self.__provisioning_profile_filename
    response['toolsets']['xcode']['certificateUploadId'] = self.__certificate_upload_id
    response['toolsets']['xcode']['certificateFilename'] = self.__certificate_filename
    response['toolsets']['xcode']['certificatePassword'] = kwargs['certificatePassword']
    response['toolsets']['android']['keystoreEncoded'] = kwargs['keystore']
    response['toolsets']['android']['keystorePassword'] = kwargs['keystore_password']
    response['toolsets']['android']['keystoreFilename'] = kwargs['keystore_filename']

    return response

  def __get_key_vault(self, app_name: str, env_name: str, vault_type: str):
    '''
    Private method to get secrets from the Azure Key Vault

    Parameters
    ----------
    app_name : str
      App name to handle file uploads
    env_name : str
      To extract the secrets from the correct environment
    vault_type : str
      Type of vault. Either Common/OEM Specific
    
    Returns
    ----------
    response : dict
      Pipeline configuration
    '''
    if vault_type == 'common':
      secret_client = self.__secret_clients[env_name]['common_client']
    else:
      secret_client = self.__secret_clients[env_name]['oem_client']

    secret_properties = secret_client.list_properties_of_secrets()

    response = {
      'environmentVariables': [],
      'toolsets': {
        'android': {},
        'xcode': {}
      }
    }

    for property in secret_properties:
      content_type = property.content_type
      tags = property.tags

      if not content_type or not tags:
        continue

      tag_key = list(tags.keys())[0]
      name = property.name.replace('-', '_')
      value = secret_client.get_secret(property.name).value

      if content_type == 'list':
        response[tag_key].append({
          'name': name,
          'value': value
        })
      elif content_type == 'dict':
        response[tag_key] = json.loads(value)
      elif content_type == 'bool':
        response[tag_key] = bool(value)
      elif content_type == 'cert' and tag_key != 'keystore':
        self.__handle_file_uploads(data=value, app_name=app_name, env_name=env_name, tag_key=tag_key)
      else:
        # content_type == str
        if tag_key == 'p12_password':
          certificatePassword = value
        elif tag_key == 'keystore':
          keystore = value
        elif tag_key == 'keystore_password':
          keystore_password = value
        elif tag_key == 'keystore_filename':
          keystore_filename = value
        elif tag_key == 'p12_filename' or tag_key == 'mobileprovision_filename':
          continue
        else:
          response[tag_key] = value
    
    if vault_type == 'oem':
      response = self.__construct_certificate_params(
        response,
        certificatePassword = certificatePassword,
        keystore = keystore,
        keystore_password = keystore_password,
        keystore_filename = keystore_filename
      )
    
    return response

  def __construct_response(self, app_name: str, platform: str, env_name: str):
    '''
    Private method to construct response pertaining to each platform

    Parameters
    ----------
    app_name : str
      App name to handle file uploads
    platform : str
      Platform type and delete certain properties from the response that are not required by the platform
    env_name : str
      To extract the secrets from the correct environment
    
    Returns
    ----------
    response : dict
      Pipeline configuration based on the platform
    '''

    for i in range(2):
      if i == 0:
        # Get Common ENV
        print(f'Retrieving Common Key Vault for {env_name} Environment')
        response_common = self.__get_key_vault(app_name=app_name, env_name=env_name, vault_type='common')
        print(f'Successfully retrieved Common Key Vault for {env_name} Environment')
        print()
      else:
        # Set OEM ENV
        print(f'Retrieving OEM Key Vault for {env_name} Environment')
        response_oem = self.__get_key_vault(app_name=app_name, env_name=env_name, vault_type='oem')
        print(f'Successfully retrieved OEM Key Vault for {env_name} Environment')
        print()
    
    oem_android = {
      **response_oem,
      'toolsets': deepcopy(response_oem['toolsets'])
    }
    # Delete xcode property from android object
    del oem_android['toolsets']['xcode']
    oem_ios = {
      **response_oem,
      'toolsets': deepcopy(response_oem['toolsets'])
    }
    # Delete android property from ios object
    del oem_ios['toolsets']['android']

    if platform == 'Android':
      return {
        **response_common,
        **oem_android,
        'environmentVariables': [*response_common['environmentVariables'], *response_oem['environmentVariables']]
      }
    else:
      return {
        **response_common,
        **oem_ios,
        'environmentVariables': [*response_common['environmentVariables'], *response_oem['environmentVariables']]
      }

  def get_vault_secrets(self, app_name = 'hello-ios-2', platform: str = 'iOS', env_name = 'dev'):
    '''
    Public method to get secrets from the vault

    Parameters
    ----------
    app_name : str
      App name to upload certificates for every file
    platform : str
      Return platform specific configuration
    env_name : str
      To save the file locally
    
    Returns
    ----------
    response : dict
      Pipeline configuration
    '''
    
    # Since this module can be accessed outside, we need to authenticate the users for token
    self.__authenticate_key_vault(env_name=env_name)

    return self.__construct_response(app_name=app_name, platform=platform, env_name=env_name)

# Main function is used only to set the secrets
def main():
  arg_length = len(sys.argv)

  # Defaults to development environment
  environment = KEY_VAULT_CONSTANTS.DEVELOPMENT_ENVIRONMENT
  # environment = 'qa'

  # If non-dev environment, argument should be passed
  if arg_length == 2:
    environment = str(sys.argv[0])
  
  key_vault = KeyVault(environment=environment)
  key_vault.set_vault_secrets()
  # key_vault.get_vault_secrets()

if __name__ == '__main__':
  main()
