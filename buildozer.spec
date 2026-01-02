[app]
title = EV Aggregator
package.name = evaggregator
package.domain = com.zerocost
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0,kivymd==1.1.1,kivy_garden.mapview,httpx,beautifulsoup4,openssl,pyjnius,certifi
orientation = portrait
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
