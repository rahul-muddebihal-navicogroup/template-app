'''
Github Related Constants
'''

'''
Github Token to authenticate user to link the app center apps with github
It is also used to create additional branches on the given repository
Follow https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token to create Github API Token
'''
GITHUB_TOKEN = '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'

'''
Default Github Repository name
Used only if development environment === 'dev'
Else, user is prompted for Github Repository Name
'''
REPO_NAME = 'rahul-muddebihal/dummy-app'

'''
Development environment
In development environment, the user inputs are bypassed and default values are used
If environment !== 'dev' then user is prompted with questions for user input 
'''
DEVELOPMENT_ENVIRONMENT = 'dev'

'''
Additional branches created for a github repository. By default, we have main branch created during repository creation
'''
BRANCHES = ['develop', 'qa']
