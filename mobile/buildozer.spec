[app]

title = LotteryLab Mobile
package.name = lotterylab
package.domain = org.lotterylab

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,json,atlas

version = 1.0

orientation = portrait

requirements = python3,kivy,requests

android.api = 35
android.minapi = 24

android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True
android.debug_artifact = apk

android.permissions = INTERNET

p4a.bootstrap = sdl2

fullscreen = 0

log_level = 2
warn_on_root = 1
