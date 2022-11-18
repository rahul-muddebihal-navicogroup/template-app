# This script will run every time a build finishes succesfully
# It will create a sourcemap and a bundle for iOS or Android and
# upload it to Bugsnag so we can get accurate stacktraces

if [ "$AGENT_JOBSTATUS" == "Succeeded" ]; then
    BUGSNAG_API_KEY=$RN_BUGSNAG_KEY
    # eg: 1.1.4-qa
    APP_VERSION=$VERSION_NAME
    # the unique identifier for the current build
    BUNDLE_VERSION=$APPCENTER_BUILD_ID

    # It's important that bugsnag receives the correct APP_VERSION (branch name usually)
    # and BUNDLE_VERSION (build number automatically incremented by AppCenter)

    echo "APP_VERSION IS $APP_VERSION"
    echo "BUNDLE IS $BUNDLE_VERSION"
    echo "BUGSNAG API_KEY $BUGSNAG_API_KEY"

    # Checking if it's a build for the iOS app
    if [ "$APPCENTER_XCODE_PROJECT" ]
    then
        echo "Running iOS Bugsnag sourcemap"

        # Generating iOS bundle and map
        npx react-native bundle \
            --platform ios \
            --dev false \
            --entry-file index.ios.js \
            --bundle-output ios-release.bundle \
            --sourcemap-output ios-release.bundle.map

        # Uploading iOS map
        curl --http1.1 https://upload.bugsnag.com/react-native-source-map \
            -F apiKey=$BUGSNAG_API_KEY \
            -F appVersion=$APP_VERSION \
            -F appBundleVersion=$BUNDLE_VERSION \
            -F dev=false \
            -F platform=ios \
            -F sourceMap=@ios-release.bundle.map \
            -F bundle=@ios-release.bundle \
            -F projectRoot=`pwd`

    else
        echo "Running Android Bugsnag sourcemap"

        # Generating Android bundle and map
        npx react-native ram-bundle \
            --dev false \
            --entry-file index.android.js \
            --platform android \
            --sourcemap-output android-release.bundle.map \
            --bundle-output android-release.bundle

        # Uploading Android map
        curl --http1.1 https://upload.bugsnag.com/react-native-source-map \
            -F apiKey=$BUGSNAG_API_KEY \
            -F appVersion=$APP_VERSION \
            -F appVersionCode=$BUNDLE_VERSION \
            -F dev=false \
            -F platform=android \
            -F sourceMap=@android-release.bundle.map \
            -F bundle=@android-release.bundle \
            -F projectRoot=`pwd`
    fi
fi

# if [[ $RN_ENV == 'qa' || $RN_ENV == 'prod' && $AGENT_JOBSTATUS == "Succeeded" && "$APPCENTER_XCODE_PROJECT" ]]; then
#     cd ..
#     zip -r $RN_VERACODE_FILENAME $APPCENTER_SOURCE_DIRECTORY
#     python3 -m pip install veracode-api-signing
#     python3 $APPCENTER_SOURCE_DIRECTORY/veracode.py $RN_VERACODE_API_ID $RN_VERACODE_API_KEY $RN_VERACODE_FILENAME $RN_ENV $RN_VERACODE_APPNAME    
# fi
