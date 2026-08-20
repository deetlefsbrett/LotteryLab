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

# Keep Python 3.12.13 consistent with the GitHub runner.
requirements = python3,kivy==2.3.1,requests

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
p4a.branch = develop

# ---------------------------------------------------------
# Build settings
# ---------------------------------------------------------

fullscreen = 0
log_level = 2
warn_on_root = 1
