#!/usr/bin/env bash
if [ -z "$VERSION_NAME" ]
then
    echo "You need define the VERSION_NAME variable in App Center"
    exit
fi
PROJECT_NAME=EmpowerMobileAppOEM4
INFO_PLIST_FILE=$APPCENTER_SOURCE_DIRECTORY/ios/$PROJECT_NAME/Info.plist
ANDROID_GRADLE_FILE=$APPCENTER_SOURCE_DIRECTORY/android/app/build.gradle

SDKMANAGER=$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager
echo y | $SDKMANAGER --uninstall "build-tools;31.0.0"
echo y | $SDKMANAGER --uninstall "build-tools;32.0.0"

if [ -e "$ANDROID_GRADLE_FILE" ]
then
    echo "Updating version name to $VERSION_NAME in build.gradle"
    sed -i '' 's/versionName "[0-9.]*-[a-z]*"/versionName "'$VERSION_NAME'"/' $ANDROID_GRADLE_FILE

    echo "File content:"
    cat $ANDROID_GRADLE_FILE
fi

if [ -e "$INFO_PLIST_FILE" ]
then
    echo "Updating version name to $VERSION_NAME in Info.plist"
    plutil -replace CFBundleShortVersionString -string $VERSION_NAME $INFO_PLIST_FILE
    echo "Updating CodePush Deployment key name to $RN_IOS_CODEPUSH_KEY in Info.plist"
    plutil -replace CodePushDeploymentKey -string $RN_IOS_CODEPUSH_KEY $INFO_PLIST_FILE
    echo "File content:"
    cat $INFO_PLIST_FILE
fi

GOOGLE_JSON_FILE=$APPCENTER_SOURCE_DIRECTORY/android/app/google-services.json
if [ -z "$GOOGLE_JSON" ]
then
    echo "You need to define the GOOGLE_JSON variable in App Center for android"
fi
if [ -e "$GOOGLE_JSON_FILE" ]
then
    echo "Updating Google Json"
    echo "$GOOGLE_JSON" > $GOOGLE_JSON_FILE
    sed -i -e 's/\\"/'\"'/g' $GOOGLE_JSON_FILE
    echo "File content:"
    cat $GOOGLE_JSON_FILE
fi

IOS_GOOGLE_JSON_FILE=$APPCENTER_SOURCE_DIRECTORY/ios/GoogleService-Info.plist
if [ -z "$IOS_GOOGLE_JSON" ]
then
    echo "You need to define the IOS_GOOGLE_JSON variable in App Center for ios"
fi
if [ -e "$IOS_GOOGLE_JSON_FILE" ]
then
    echo "Updating IOS Google Json"
    echo "$IOS_GOOGLE_JSON" > $IOS_GOOGLE_JSON_FILE
    sed -i -e 's/\\"/'\"'/g' $IOS_GOOGLE_JSON_FILE
    echo "File content:"
    cat $IOS_GOOGLE_JSON_FILE
fi

# AppCenter config
IOS_APPCENTER_CONFIG_PLIST_FILE=$APPCENTER_SOURCE_DIRECTORY/ios/$PROJECT_NAME/AppCenter-Config.plist
ANDROID_APPCENTER_CONFIG_PLIST_FILE=$APPCENTER_SOURCE_DIRECTORY/android/app/src/main/assets/appcenter-config.json
if [ -e "$IOS_APPCENTER_CONFIG_PLIST_FILE" ]
then
    echo "Updating iOS AppCenter key in AppCenter-Config.plist"
    plutil -replace AppSecret -string $APP_SECRET_VALUE $IOS_APPCENTER_CONFIG_PLIST_FILE
    echo "File AppCenter-Config.plist content:"
    cat $IOS_APPCENTER_CONFIG_PLIST_FILE
fi
if [ -e "$ANDROID_APPCENTER_CONFIG_PLIST_FILE" ]
then
    echo "Updating Android AppCenter key in appcenter-config.json"
    sed -i -e 's/"{APP_SECRET_VALUE}"/"'$APP_SECRET_VALUE'"/g' $ANDROID_APPCENTER_CONFIG_PLIST_FILE
    echo "File appcenter-config.json content:"
    cat $ANDROID_APPCENTER_CONFIG_PLIST_FILE
fi

# verify cocoapods versions
CUR_COCOAPODS_VER=`sed -n -e 's/^COCOAPODS: \([0-9.]*\)/\1/p' ios/Podfile.lock`
ENV_COCOAPODS_VER=`pod --version`
# check if not the same version, reinstall cocoapods version to current project's
if [ $CUR_COCOAPODS_VER != $ENV_COCOAPODS_VER ];
then
    echo "Uninstalling all CocoaPods versions"
    sudo gem uninstall cocoapods --all --executables
    echo "Installing CocoaPods version $CUR_COCOAPODS_VER"
    sudo gem install cocoapods -v $CUR_COCOAPODS_VER
else
    echo "CocoaPods version is suitable for the project"
fi;

#Add bconline private pod 
cd ios
NPM_PASSWORD_DECODED=$(echo $NPM_PASS | base64 --decode)
pod repo add bconline-engage-ios-podspecs https://$NPM_USER:$NPM_PASSWORD_DECODED@dev.azure.com/bconline/ASG/_git/engage-ios-podspecs
cd ..

# Creates an .env from ENV variables for use with react-native-config
ENV_WHITELIST=${ENV_WHITELIST:-"^RN_"}
cd $APPCENTER_SOURCE_DIRECTORY
printf "Creating an .env file with the following whitelist:\n"
printf "%s\n" $ENV_WHITELIST
set | egrep -e $ENV_WHITELIST | sed 's/^RN_//g' > .env
printf "\n.env created with contents:\n\n"
cat .env
