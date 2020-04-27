from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
# 博客文章数据模型
class DailyPost(models.Model):
    # 日报作者作者。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 今日任务。models.CharField 为字符串字段
    # todaytask = models.CharField(max_length=500)
    todaytask = models.TextField()
    # 明日任务。
    # tomorrowtask = models.CharField(max_length=500)
    tomorrowtask = models.TextField()

    # 自动化任务。
    autotask = models.TextField(blank=True)
    # 日报创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)
    #日报上报图片
    dailyfile = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)


    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        ordering = ('-created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.todaytask