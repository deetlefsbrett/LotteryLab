[app]

# ---------------------------------------------------------
# Application
# ---------------------------------------------------------

title = LotteryLab Mobile
package.name = lotterylab
package.domain = org.lotterylab

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,json,atlas

version = 1.0
orientation = portrait

# ---------------------------------------------------------
# Python / Kivy
# ---------------------------------------------------------

requirements = python3,kivy==2.3.1,requests==2.31.0,charset-normalizer==3.4.1

# ---------------------------------------------------------
# Android
# ---------------------------------------------------------

android.api = 36
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True
android.debug_artifact = apk
android.permissions = INTERNET

# ---------------------------------------------------------
# Python-for-Android
# ---------------------------------------------------------

p4a.bootstrap = sdl2

# ---------------------------------------------------------
# Build settings
# ---------------------------------------------------------

fullscreen = 0
log_level = 2
warn_on_root = 1
