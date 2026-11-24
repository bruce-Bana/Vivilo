# Vivilo Android

Android source package and GitHub Actions APK build pipeline.

## Add the source archive

Upload the prepared project archive from this conversation to the repository root and name it exactly:

`vivilo-source.zip`

The archive must contain `settings.gradle.kts` and `app/build.gradle.kts` at its root (not nested in an extra directory).

## Build

After `vivilo-source.zip` is committed, GitHub Actions automatically runs tests and builds a debug APK. You can also run it manually from **Actions → Build Vivilo Android APK → Run workflow**.

The APK and SHA-256 checksum are published as the `vivilo-android-apk` workflow artifact. This is a debug-signed APK for testing and sideloading; a Play Store release requires a separately configured signing key stored as GitHub Actions secrets.

## Project details

- Android application ID: `com.vivilo.media`
- Build system: Gradle Kotlin DSL
- CI runtime: Ubuntu + JDK 17 + Android SDK
