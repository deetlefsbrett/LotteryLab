[app]

# (str) Title of your application
title = LotteryLab Mobile

# (str) Package name
package.name = lotterylab

# (str) Package domain
package.domain = org.lotterylab

# (str) Source code directory
source.dir = .

# (str) Application version
version = 1.0.0

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,atlas,db

# (list) Requirements
requirements = python3,kivy==2.3.1,requests

# (str) Orientation
orientation = portrait

# (bool) Fullscreen
fullscreen = 0

# (list) Android permissions
android.permissions = INTERNET

# (int) Android API
android.api = 33

# (int) Minimum Android API
android.minapi = 24


[buildozer]

# (int) Log level
log_level = 2

# (bool) Warn when running Buildozer as root
warn_on_root = 1
