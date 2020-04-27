# 引入表单类
from django import forms
from daily.models import DailyPost

class DailyPostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = DailyPost
        # 定义表单包含的字段
        fields = ('todaytask', 'autotask', 'tomorrowtask')