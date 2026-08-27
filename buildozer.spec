[app]
title = Underwater Clicker
package.name = underwaterclicker
package.domain = org.pythonexpert
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ogg,mp3,ttf,woff,txt
source.exclude_dirs = .venv,.idea,__pycache__,bin,build,.buildozer
source.exclude_exts = pyc,pyo,xcf
version = 1.0
# Use the current Android Python runtime.  The application code is compatible
# with it; charset-normalizer 2.x is pure Python and works on Android.
requirements = python3,kivy,charset-normalizer==2.1.1
orientation = portrait
fullscreen = 1
# Android build settings.
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
# The develop branch contains current Android compatibility fixes.
p4a.branch = develop
[buildozer]
log_level = 2
warn_on_root = 1
