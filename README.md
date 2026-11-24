# Vivilo Android

Android source package and GitHub Actions APK build pipeline.

## Add the source archive

Upload the prepared project archive from this conversation to the repository root and name it exactly:

`Vivilo-GitHub-Actions-Ready.zip`

The archive must contain `settings.gradle.kts` and `app/build.gradle.kts` at its root (not nested in an extra directory).

## Build

After `Vivilo-GitHub-Actions-Ready.zip` is committed, GitHub Actions automatically runs tests and builds a debug APK. You can also run it manually from **Actions → Build Vivilo Android APK → Run workflow**.

The APK and SHA-256 checksum are published as the `vivilo-android-apk` workflow artifact. This is a debug-signed APK for testing and sideloading; a Play Store release requires a separately configured signing key stored as GitHub Actions secrets.

## Project details

- Android application ID: `com.vivilo.media`
- Build system: Gradle Kotlin DSL
- CI runtime: Ubuntu + JDK 17 + Android SDK


## In-app updates and versioning

Vivilo checks the **latest GitHub Release** from the in-app update button in the home header. Published releases include:

- `vivilo.apk` — signed Android package
- `vivilo.apk.sha256` — SHA-256 checksum verified before installation
- `vivilo-version.json` — monotonically increasing Android version code and display version

The updater uses HTTPS, compares the installed `versionCode`, downloads the APK into the app's private cache, verifies its checksum, and opens Android's package installer. Android always asks the user to approve the installation; Vivilo cannot silently install or bypass that system confirmation. On Android 8+, allow Vivilo to install unknown apps when Android requests it.

### One-time signing setup (required)

Android only accepts an in-place update when the new APK is signed with the same private key as the installed APK. GitHub Actions therefore builds a stable-signed release APK. Add these repository Actions secrets:

- `VIVILO_KEYSTORE_BASE64` — base64 text of the private upload keystore
- `VIVILO_STORE_PASSWORD` — keystore password
- `VIVILO_KEY_ALIAS` — signing alias
- `VIVILO_KEY_PASSWORD` — key password (same as store password for the supplied PKCS12 keystore)

Never commit the keystore or its passwords to the repository. Keep a secure backup: losing the key prevents future in-place updates.

The first stable-signed build cannot update an earlier APK that was signed with a temporary GitHub-hosted debug key. That first transition requires removing the older installation and installing the stable-signed build. Removing the old app clears its private app data; back up anything important first. After the stable-signed build is installed, subsequent releases can update in place.

The workflow increments the Android version code using the GitHub Actions run number and publishes the version manifest with each latest release.
