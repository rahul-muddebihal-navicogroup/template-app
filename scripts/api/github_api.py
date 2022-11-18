import logging

from api.api_wrapper import ApiWrapper
from api.models import GithubResponse

class GithubApi:
  def __init__(self, github_token: str) -> None:
    headers = {
      'accept': 'application/vnd.github.v3+json',
      'Authorization': f'token {github_token}'
    }
    self.__api = ApiWrapper('api.github.com', headers)
    self.__logger = logging.getLogger(__name__)

  def __get_request(self, endpoint: str):
    '''
    Fetch Github request

    Parameters
    ----------
    endpoint : str
      The API endpoint

    Returns
    ----------
    response : GithubResponse
    '''
    result = self.__api.get(endpoint=endpoint)
    data = result.data

    response = GithubResponse(json=data)

    return response

  def __post_request(self, endpoint: str, json):
    '''
    Post data to Github
    
    Parameters
    ----------
    endpoint : str
      The API url
    data : Dict
      The request body 
    
    Returns
    ----------
    data : Any
    '''
    result = self.__api.post(endpoint=endpoint, json=json)
    data = result.data
    
    return data

  def get_branch_sha(self, repo_name: str, branch_name = "main"):
    '''
    Provides the SHA of the given branch

    Parameters
    ----------
    repo_name : str
      The repository name in the owner/repo_name format. Ex: magento/knowledge-base
    branch_name : str
      Defaults to master branch. If you don't want to use the master branch, use a different argument
    
    Returns
    ----------
    sha : str
    ''' 
    endpoint = f'repos/{repo_name}/branches/{branch_name}'
    response = self.__get_request(endpoint=endpoint)
    try:
      sha = response.json['commit']['sha']
    except KeyError as e:
      self.__logger.error(msg=str(e))
    
    return sha
  
  def create_new_branch(self, repo_name: str, master_branch_sha: str, new_branch_name: str):
    '''
    Creates a new branch from the SHA of the master branch

    Parameters
    ----------
    repo_name : str
      The repository name in the owner/repo_name format. Ex: magento/knowledge-base
    master_branch_sha : str
      SHA of the main/master branch
    new_branch_name : str
      New branch name
    
    Returns
    ----------
    response : Any
    '''
    endpoint = f'repos/{repo_name}/git/refs'

    json = {
      "ref": f'refs/heads/{new_branch_name}',
      "sha": master_branch_sha
    }

    response = self.__post_request(endpoint=endpoint, json=json)

    return response
