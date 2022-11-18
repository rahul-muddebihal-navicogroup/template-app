import sys
import time
import json

from github import Github
from key_vault import KeyVault
from api.app_center_api import AppCenterApi
from constants import app_center_constants as APP_CENTER_CONSTANTS

'''
To run the app
For development mode:
python3 app_center.py
For non-dev mode:
python3 app_center.py <arg> # arg can be anything except dev
Ex: python3 app_center.py qa
'''

class AppCenterApp:
  def __init__(self, display_name: str, app_name: str, description: str, os: str, platform: str, release_type: str):
    self.__display_name = display_name
    self.__description = description
    self.__os = os
    self.__platform = platform
    self.__release_type = release_type
    self.__app_name = self.__format_app_name(app_name)

  def __format_app_name(self, app_name = ''):
    delimiter = '-'
    
    if app_name == '':
      app_name = self.__display_name
      app_name = app_name.lower().split(' ')
      app_name = f'{delimiter.join(app_name)}-{self.__os}'.lower()
    
    return app_name

  def get_json(self):
    return {
      'display_name': self.__display_name,
      'description': self.__description,
      'os': self.__os,
      'platform': self.__platform,
      'release_type': self.__release_type,
      'name': self.__app_name,
    }

class AppCenter:
  '''
  Class to create an app in App Center, fetch secrets from Azure Key Vault and configure Pipeline
  '''
  def __init__(self, environment: str) -> None:
    self.__environment = environment
    self.__app_center_api = None
    self.__key_vault = KeyVault(environment=environment)

  def __configure_repository(self, created_app):
    '''
    Private method to configure Repository for the App Center Apps
    '''
    if self.__environment != APP_CENTER_CONSTANTS.DEVELOPMENT_ENVIRONMENT:
      repo_url = input(f'Enter your Repository URL for configuration. You must have admin access to the repository: \n')
    else:
      repo_url = APP_CENTER_CONSTANTS.GITHUB_URL

    print()
    data = {'repo_url':  repo_url}
    app_name = created_app.get('name')
    print(f'Waiting for app to come online {app_name}. Takes approximately 60 seconds')
    time.sleep(60)
    self.__app_center_api.repo_config(app_name=app_name, json=data)
    print(f'Repository configured successfully for {app_name}')
    print()

  def __retrieve_pipeline_config_keyvault(self, app_name: str, platform: str, env_name: str):
    '''
    Private method to contruct pipeline configuration for keyvault
    
    Parameters
    ----------
    app_name : str
      App name
    platform : str
      Platform name
    env_name : str
      Environment name from which the secrets are extracted from
    '''

    return self.__key_vault.get_vault_secrets(app_name=app_name, platform=platform, env_name=env_name)

  def __configure_pipeline(self, created_app):
    '''
    Private method to configure pipeline for all the created apps for each environment/branche
    
    Parameters
    ----------
    created_app : dict
      Created app
    '''
    for env in APP_CENTER_CONSTANTS.ENVIRONMENTS:
      env_name = env['env_name']
      branch = env['branch']
      app_name = created_app.get('name')
      os = created_app.get('os')
      app_display_name = created_app.get('display_name')

      print()
      # Extract config from a reference app or Keyvault
      pipeline_config = self.__retrieve_pipeline_config_keyvault(app_name=app_name, platform=os, env_name=env_name)
      
      print(f'Configuring Pipeline for Branch - {branch} of {app_display_name}')
      self.__app_center_api.update_app_config(app_name=app_name, branch=branch, json=pipeline_config)
      
      print(f'Successfully Configured Pipeline for {app_name}')
      print()

  def __create_app_center_apps(self):
    '''
    Private method to create Apps in App Center
    '''
    for i in range(len(APP_CENTER_CONSTANTS.OS)):
      os = APP_CENTER_CONSTANTS.OS[i]

      if self.__environment != APP_CENTER_CONSTANTS.DEVELOPMENT_ENVIRONMENT:
        app_display_name = input(f'Enter your App Center Display Name for {os}: \n')
        print()
        app_name = input(f'Enter your App Center App ID for {os}: \n')
        print()
        app_description = input(f'Enter short description for your {os} App: \n')
        print()
      else:
        app_display_name = f'hello'.lower()
        app_name = ''
        app_description = ''

      
      app = AppCenterApp(
        display_name=app_display_name, 
        app_name=app_name, 
        description=app_description, 
        os=os, 
        platform=APP_CENTER_CONSTANTS.PLATFORM, 
        release_type=APP_CENTER_CONSTANTS.RELEASE_TYPE
      )
      # Creating the app
      app_json = app.get_json()
      print(f"Creating {os} App with Display Name as {app_json['display_name']} and App ID as {app_json['name']}")
      created_app = self.__app_center_api.create_app(app_json)

      # Configure Repository
      self.__configure_repository(created_app=created_app)

      # Configure pipeline
      self.__configure_pipeline(created_app=created_app) 

  def init_app(self):
    '''
    Initiate the app creation process
    '''

    '''
    If environment is dev, default constants are utilized.
    Else, user is promted with questions
    '''
    if self.__environment != APP_CENTER_CONSTANTS.DEVELOPMENT_ENVIRONMENT:
      app_center_token = input(f'Enter your App Center API Token: \n')
      print()
    else:
      app_center_token = APP_CENTER_CONSTANTS.APP_CENTER_TOKEN

    # Create a app_center api
    self.__app_center_api = AppCenterApi(app_center_token=app_center_token)
    
    '''
    For Development ONLY,
    delete the apps created, before performing the next set of actions
    '''
    if self.__environment == APP_CENTER_CONSTANTS.DEVELOPMENT_ENVIRONMENT:
      for app_name in APP_CENTER_CONSTANTS.EXAMPLE_APPS:
        self.__app_center_api.delete_app(app_name=app_name)
        # pass

    # Create develop and qa branches for github
    print(f'Creating develop and qa branches for the selected repository')
    print()
    github = Github(environment=self.__environment)
    github.init_app()
    print()

    # Create app center apps
    self.__create_app_center_apps()

def main():
  arg_length = len(sys.argv)

  # Defaults to development environment
  environment = APP_CENTER_CONSTANTS.DEVELOPMENT_ENVIRONMENT

  # If non-dev environment, argument should be passed
  if arg_length == 2:
    environment = str(sys.argv[0])

  appcenter_app = AppCenter(environment=environment)
  
  # Invoke the appcenter app
  appcenter_app.init_app()

if __name__ == '__main__':
  main()
