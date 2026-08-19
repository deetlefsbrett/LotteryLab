[app]

title = LotteryLab Mobile
package.name = lotterylab
package.domain = org.lotterylab

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,db

version = 1.0.0

requirements = python3==3.12.9,hostpython3==3.12.9,kivy,requests

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.api = 33
android.minapi = 24

p4a.branch = master


[buildozer]

log_level = 2
warn_on_root = 1
