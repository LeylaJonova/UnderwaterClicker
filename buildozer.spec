[app]
title = Underwater Clicker
package.name = underwaterclicker
package.domain = org.pythonexpert
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ogg,mp3,ttf,woff,txt
source.exclude_dirs = .venv,.idea,__pycache__,bin,build,.buildozer
source.exclude_exts = pyc,pyo,xcf
version = 1.0
# The app only uses Kivy and Python's standard library.
requirements = python3,kivy
orientation = portrait
fullscreen = 1
# Android build settings.
android.api = 33
android.minapi = 23
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
[buildozer]
log_level = 2
warn_on_root = 1
