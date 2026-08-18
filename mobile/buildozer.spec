title = LotteryLab Mobile
package.name = lotterylab
package.domain = org.lotterylab

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,db

version = 1.0.0

requirements = python3,kivy==2.3.1,requests

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

[buildozer]

log_level = 2
warn_on_root = 1

android.api = 33
android.minapi = 24
