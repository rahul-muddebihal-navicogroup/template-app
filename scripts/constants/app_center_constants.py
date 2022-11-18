'''
App Center Related Constants
'''

'''
App Center Token for all App Center API requests. Must be changed
Follow https://learn.microsoft.com/en-us/appcenter/api-docs/ to create App Center API Token
'''
APP_CENTER_TOKEN = '2a11bcb51e7fbe6ba4052db153b994c904171f13'

'''
Default Github Repository Url
Used only if development environment === 'dev'
Else, user is prompted for Github Repository Url
'''
GITHUB_URL = 'https://github.com/rahul-muddebihal/dummy-app.git'

'''
The OS the app will be running on
Supported OS - [ Android, iOS, macOS, Tizen, tvOS, Windows, Linux, Custom ]
'''
OS = ['Android', 'iOS']

'''
The platform of the app
Supported Platform - [ Java, Objective-C-Swift, UWP, Cordova, React-Native, Unity, Electron, Xamarin, WPF, WinForms, Unknown, Custom ]
'''
PLATFORM = 'React-Native'

'''
A one-word descriptive release-type value that starts with a capital letter but is otherwise lowercase
'''
RELEASE_TYPE = 'Alpha'

'''
Additional branches created for a github repository. By default, we have main branch created during repository creation
@deprecated
'''
BRANCHES = ['develop', 'qa']

'''
Since each environment has its own key vault.
The env_name specifies the environment from which the secrets should be extracted from
Once the keys are extracted, the pipeline configuration is created for each branch specified by branch
'''
ENVIRONMENTS = [
  {'env_name': 'dev', 'branch': 'develop' },
  {'env_name': 'qa', 'branch': 'qa' },
  {'env_name': 'prod', 'branch': 'main' }
]

'''
App Center organization base url to create apps
'''
ORG_BASE_URL = f'https://api.appcenter.ms/v0.1/orgs/nauticon'

'''
App Center app base url for other APIs
'''
APP_BASE_URL = f'https://api.appcenter.ms/v0.1/apps/nauticon'

'''
App Center Endpoints
'''
BASE_ENDPOINTS = {
  'org_base_endpoint': 'v0.1/orgs/nauticon', # App Center organization base endpoint to create apps
  'app_base_endpoint': 'v0.1/apps/nauticon', # App Center app base endpoint for other APIs
}


'''
App Center base urls used for uploading file assets
'''
UPLOAD_BASE_URLS = {
  'cancel_upload': 'upload/cancel',
  'set_metadata': 'upload/set_metadata',
  'upload_chunk': 'upload/upload_chunk',
  'upload_finished': 'upload/finished',
  'upload_status': 'upload/status',
}

'''
Organization owner
'''
OWNER = 'nauticon'

'''
Used to delete app on creation
For development only
'''
EXAMPLE_APPS = ['hello-android', 'hello-ios']

'''
Development environment
In development environment, the user inputs are bypassed and default values are used
If environment !== 'dev' then user is prompted with questions for user input 
'''
DEVELOPMENT_ENVIRONMENT = 'dev'
