#!/usr/bin/env bash
export AZURE_DEVOPS_EXT_PAT=$(echo $NPM_PASS | base64 --decode)
az config set extension.use_dynamic_install=yes_without_prompt
echo $(echo $NPM_PASS | base64 --decode) | az devops login
gem install cocoapods-azure-universal-packages
