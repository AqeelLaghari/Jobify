# Fix: Emulator Showing Old Version of Flutter App

## Problem Analysis
Your Flutter app (`myapp`) builds successfully but the Android emulator displays an older version instead of your latest code changes. This is a common Flutter development issue caused by stale build artifacts or cached APK installations.

## Root Causes
1. **Flutter build cache** contains old compiled artifacts in `myapp/build/`
2. **Old APK still installed** on the emulator — Flutter's incremental install sometimes fails to overwrite
3. **Hot reload limitations** — major widget tree or initialization changes require a full rebuild
4. **Android emulator snapshot** restoring an old system image with the previous app installed
5. **Multiple devices/emulators** connected — app may be launching on a different device than expected

## Fix Plan
- [x] Step 1: Stop any running Flutter processes
- [x] Step 2: Clean Flutter build cache (`flutter clean`)
- [x] Step 3: Re-fetch dependencies (`flutter pub get`)
- [x] Step 4: Check available devices (`flutter devices` found emulator-5554)
- [x] Step 5: Fix root `android/build.gradle.kts` — added missing `repositories { google(); mavenCentral() }` inside `buildscript`
- [x] Step 6: Build and run fresh on the emulator (`flutter run -d emulator-5554`)
- [x] Step 7: APK built & installed successfully — app is now running updated version on emulator

## Prevention
- Always use `flutter clean` after major dependency or platform changes
- Avoid relying solely on hot reload for AndroidManifest or native code changes
- Use `flutter run --verbose` to inspect which device is targeted

