[app]
title = Wifi Connect App
package.name = wificonnect
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.0.1
requirements = python3,kivy,flask
orientation = portrait
fullscreen = 1

# Android configurations
android.api = 33
android.minapi = 21
android.allow_api_min = 21
android.ndk = 25b
android.sdk = 33
android.permissions = INTERNET, ACCESS_WIFI_STATE, CHANGE_WIFI_STATE

[buildozer]
log_level = 2
