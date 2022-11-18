#!/usr/bin/env sh

############################################################
# Help                                                     #
############################################################
help() {
  # Display Help
  echo "Additional arguments can be passed to the script"
  echo
  echo "Syntax: sh ./create_key_vault.sh [-c|o|h]"
  echo "options:"
  echo "c     Create Common environment key vault(s)"
  echo "o     Create OEM specific environment key vault(s)"
  echo "h     Print this Help"
  echo
}

############################################################
# Generate Vault Names                                     #
############################################################
initiate_process() {
  local env_list=("dev" "qa" "prod")
  local vault_type=$1
  local oem_name=$2
  
  if [ $vault_type == "common" ]
  then 
    vault_name_prefix="common-env-keyvault"
  else
    vault_name_prefix=$oem_name"-keyvault"
  fi

  for env in ${env_list[@]}; do
    vault_name=$vault_name_prefix"-"$env
    env_upper=$(echo "$env" | awk '{print toupper($0)}')

    if [[ ${#vault_name} -lt 3 || ${#vault_name} -gt 50 ]]
    then
      echo "Invalid Vault Name ${vault_name}. Name must be between 3 and 24 characters"
      exit 1
    fi
    
    echo "Creating ${vault_name}"
    create_key_vault $vault_name $env_upper $vault_type $oem_name
  done
}

############################################################
# Create Key Vault using AZ CLI                            #
############################################################
create_key_vault() {
  resource_group="rg-mobile-pipeline-keyvault"
  vault_name=$1
  env=$2
  vault_type=$3
  oem_name=$4
  oem_name_upper=$(echo "$oem_name" | awk '{print toupper($0)}')
  
  if [ $vault_type == "common" ]
  then
    tag_key="COMMON_KEY_VAULT_"$env
    tag_value="COMMON_KEY_VAULT_"$env
  else
    tag_key="OEM_KEY_VAULT_"$env
    tag_value=$oem_name_upper"_KEY_VAULT_"$env
  fi

  # az login
  az keyvault create --location eastus --name "$vault_name" --resource-group "$resource_group" --tags $tag_key=$tag_value
}

############################################################
# Create Common Key Vault                                  #
############################################################
create_common_key_vault() {
  echo "Creating Common Key Vault"

  initiate_process "common"

  exit 1
}

############################################################
# Create OEM Specific Key Vault                            #
############################################################
create_oem_key_vault() {
  echo "Creating OEM Specific Key Vault"
  echo "Enter the OEM Name:"
  read oem_name

  initiate_process "oem" $oem_name

  exit 1
}

############################################################
############################################################
# Main program                                             #
############################################################
############################################################

if ! [ -x "$(command -v az)" ]; then
  echo "Error: Azure CLI is not installed." >&2
  echo "Use the link to download and install Azure Cli: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli"
  exit 1
fi

############################################################
# Process the input options. Add options as needed.        #
############################################################
while getopts "och" option; do
  case $option in
    h)
      help
      exit;;
    c)
      create_common_key_vault
      exit;;
    o)
      create_oem_key_vault
      exit;;
    \?) 
      echo "Error: Invalid option"
      exit;;
  esac
done

echo "No argument passed. Creating OEM Specific Key Vault"
create_oem_key_vault
