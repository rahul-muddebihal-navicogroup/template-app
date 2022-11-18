#!/bin/bash

# Script tipically used during the QA build process to quickly bump
# @brunswick/engage-core-app to the latest version

# Usage: run ./bump-coreapp.sh in the command line.
# If you have the Azure devops access token setup as DEVOPS_TOKEN the script will also create the PR.

git checkout develop
git pull origin develop

# We get the package info from the npm repository
coreAppPackageInfo=$(npm view @brunswick/engage-core-app --json)

# We get all existing versions
allVersions=$(jq '.versions[]' <<<"$coreAppPackageInfo")
declare -a allVersionsArray=($allVersions)
allVersionsArrayLength="${#allVersionsArray[@]}"

# We get the latest non beta version
for ((i = $(($allVersionsArrayLength - 1)); i > -1; i--)); do
    if [[ ${allVersionsArray[$i]} != *"beta"* ]]; then
        latestNonBetaRaw=${allVersionsArray[$i]}
        break
    fi
done

# We remove the double quotes
latestNonBeta="${latestNonBetaRaw:1:${#latestNonBetaRaw}-2}"

echo latestNonBeta $latestNonBeta

# We create a new branch
git checkout -b versionbump/bump-coreapp-to-$latestNonBeta

# We install the latest coreapp
yarn add @brunswick/engage-core-app@$latestNonBeta

# We commit and push the changes
git add package.json yarn.lock
git commit -m "bump core app to ${latestNonBeta}"
git push --set-upstream origin versionbump/bump-coreapp-to-$latestNonBeta

git checkout -

# We create the PR

# An access token to Azure Devops is required. Otherwise we exit the script.
if [ -n "${DEVOPS_TOKEN+1}" ]; then
  echo "DEVOPS_TOKEN is set."
else
  echo "DEVOPS_TOKEN is not set.  Please make the PR manually." >&2
  exit 1
fi

newBranch="versionbump/bump-coreapp-to-$latestNonBeta"

prTitle="Bump Core App to $latestNonBeta"

prData=$(curl -u bconline:$DEVOPS_TOKEN -X POST -H "Content-Type: application/json" \
    -d '{"sourceRefName":"'"refs/heads/$newBranch"'","targetRefName":"refs/heads/develop","title": "'"$prTitle"'"}' \
    'https://dev.azure.com/bconline/ASG/_apis/git/repositories/template-app/pullrequests\?api-version=6.0')

prId=$(jq '.pullRequestId' <<<"$prData")

# We copy the PR url to clipboard (macOS only)
echo "https://dev.azure.com/bconline/ASG/_git/template-app/pullrequest/$prId" | pbcopy

echo "PR has been successfully created at https://dev.azure.com/bconline/ASG/_git/template-app/pullrequest/$prId"
