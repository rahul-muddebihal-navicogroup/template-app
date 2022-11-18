'''
Azure Key Vault Related Constants
'''

'''
Azure Tenant ID
Follow this https://learn.microsoft.com/en-us/azure/azure-portal/get-subscription-tenant-id to find the tenant id
'''
TENANT_ID = '276ae923-8fc9-4d78-a341-8719a5ab0e47'

'''
Default common azure key vault url dev environment. 
Used only if development environment === 'dev'
Else, user is prompted for common azure key vault url for each environment
'''
COMMON_ENV_VAULT_URL = 'https://ex-common-env-secrets-3.vault.azure.net/'

'''
Default OEM specific azure key vault url dev environment. 
Used only if development environment === 'dev'
Else, user is prompted for common azure key vault url for each environment
'''
OEM_VAULT_URL = 'https://ex-oem-env-secrets-3.vault.azure.net/'

# COMMON_ENV_VAULT_URL = 'https://common-env-keyvault-dev.vault.azure.net/'

# OEM_VAULT_URL = 'https://oem-1-keyvault-dev.vault.azure.net/'

'''
Development environment
In development environment, the user inputs are bypassed and default values are used
If environment !== 'dev' then user is prompted with questions for user input 
'''
DEVELOPMENT_ENVIRONMENT = 'dev'

'''
Since each environment has its own key vault.
The env_name specifies the environment from which the secrets should be extracted from
Once the keys are extracted, the pipeline configuration is created for each branch specified by branch
'''
ENVIRONMENTS = [
  {'name': 'dev', 'branch': 'develop' },
  {'name': 'qa', 'branch': 'qa' },
  {'name': 'prod', 'branch': 'main' }
]

'''
DEV Environment name and branch
'''
DEV_ENVIRONMENTS = [
  {'name': 'dev', 'branch': 'develop' }
]

'''
Default base directory key vault template json
'''
KEY_VAULT_TEMPLATE_PATH = 'key_vault_template'

'''
Default filename of the common env secrets that is used to upload secrets to Azure Key Vault
'''
BASE_COMMON_FILE_NAME = 'common_env_key_vault'

'''
Default filename of the common env secrets that is used to upload secrets to Azure Key Vault
'''
BASE_OEM_FILE_NAME = 'oem_env_key_vault'

'''
Default Mobile Provision path. Must be changed 
Used only if development environment === 'dev'
Else, user is prompted for Mobile Provision path
'''
MOBILE_PROVISON_PATH = '/Users/rahulmuddebihal/Downloads/Empower_OEM4_Adhoc-2.mobileprovision'

'''
Default P12 Certificate path. Must be changed 
Used only if development environment === 'dev'
Else, user is prompted for P12 Certificate
'''
P12_CERTIFICATE_PATH = '/Users/rahulmuddebihal/Downloads/powerProd2023.p12'

'''
Default Android Keystore Certificate path. Must be changed 
Used only if development environment === 'dev'
Else, user is prompted for Android Keystore Certificate path
'''
KEY_STORE_CERTIFICATE_PATH = '/Users/rahulmuddebihal/Downloads/android.keystore'

'''
Default P12 Certificate Password. Must be changed 
Used only if development environment === 'dev'
Else, user is prompted for P12 Certificate Password
'''
P12_CERTIFICATE_PASSWORD = 'River123'

'''
Default Android Keystore Certificate Password. Must be changed 
Used only if development environment === 'dev'
Else, user is prompted for Android Keystore Certificate Password
'''
KEY_STORE_CERTIFICATE_PASSWORD = 'River123'
