from django.contrib import admin

# Register your models here.
from daily.models import DailyPost

# 注册DailyPost到admin中
admin.site.register(DailyPost)