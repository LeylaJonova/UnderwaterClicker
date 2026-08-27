[app]
title = Underwater Clicker
package.name = underwaterclicker
package.domain = org.pythonexpert
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ogg,mp3,ttf,woff,txt
source.exclude_dirs = .venv,.idea,__pycache__,bin,build,.buildozer
source.exclude_exts = pyc,pyo,xcf
version = 1.0
# Pin the stable Android runtime to Python 3.12.  charset-normalizer 2.x is
# pure Python and avoids the incompatible Android wheel pulled by newer p4a.
requirements = python3==3.12.11,hostpython3==3.12.11,kivy,charset-normalizer==2.1.1
orientation = portrait
fullscreen = 1
# Android build settings.
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
# The current p4a develop branch uses Python 3.14 and is not yet suitable for
# this dependency set.  The stable branch supports the pinned Python version.
p4a.branch = master
[buildozer]
log_level = 2
warn_on_root = 1
