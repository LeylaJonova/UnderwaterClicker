[app]

# Назва, яка буде відображатися на телефоні.
title = Underwater Clicker

# Технічне ім'я застосунку: лише малі латинські літери та цифри.
package.name = underwaterclicker

# Ідентифікатор пакета для Android.
package.domain = org.pythonexpert

# Коренева папка проєкту з main.py.
source.dir = .

# Файли, які необхідно додати до APK.
source.include_exts = py,kv,png,jpg,jpeg,ogg,mp3,ttf,woff,txt

# Не додаємо службові папки та вихідні файли редактора зображень.
source.exclude_dirs = .venv,.idea,__pycache__,bin,build
source.exclude_exts = pyc,pyo,xcf

# Головна залежність застосунку.
requirements = python3,kivy

# Екран додатка працює тільки вертикально.
orientation = portrait

# Повноекранний режим на Android.
fullscreen = 1

# Версія Android API для збірки.
android.api = 33
android.minapi = 23

# Архітектура більшості сучасних Android-пристроїв.
android.archs = arm64-v8a

# Не копіюємо приватний ключ: Buildozer створить debug-APK.

[buildozer]

# Рівень деталізації журналу збірки.
log_level = 2

# Запит на підтвердження, якщо файли збірки потрібно видалити.
warn_on_root = 1

# Версія застосунку
version = 1.0
