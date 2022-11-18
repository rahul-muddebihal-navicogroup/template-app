import sys

from api.github_api import GithubApi
from constants import github_constants as GITHUB_CONSTANTS

'''
To run the app
For development mode:
python3 github.py
For non-dev mode:
python3 github.py <arg> # arg can be anything except dev
Ex: python3 github.py qa
'''

class Github:
  def __init__(self, environment: str) -> None:
    self.__environment = environment

  def init_app(self):
    if self.__environment != GITHUB_CONSTANTS.DEVELOPMENT_ENVIRONMENT:
      github_token = input(f'Enter your Github token: \n')
      print()
      repo_name = input(f'Enter your Github Repo name: Example: <Organization>/<Repository Name>\n')
      print()
    else:
      github_token = GITHUB_CONSTANTS.GITHUB_TOKEN
      repo_name = GITHUB_CONSTANTS.REPO_NAME

    # Create a github api
    github_api = GithubApi(github_token=github_token)

    # Get the SHA from the master branch
    sha = github_api.get_branch_sha(repo_name=repo_name)
    
    for branch in GITHUB_CONSTANTS.BRANCHES:
      new_branch = github_api.create_new_branch(repo_name, sha, branch)
      print(f'Successfully created new branch: {branch} branch in {repo_name}')
    
def main():
  arg_length = len(sys.argv)

  # Defaults to development environment
  environment = GITHUB_CONSTANTS.DEVELOPMENT_ENVIRONMENT

  # If non-dev environment, argument should be passed
  if arg_length == 2:
    environment = str(sys.argv[0])

  github_app = Github(environment=environment)
  
  # Invoke the git app
  github_app.init_app()
  
if __name__ == '__main__':
  main()
