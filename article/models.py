from django import forms
from django.contrib.auth.models import User  # 引入作者模块
from django.db import models
from django.utils import timezone

# Create your models here.


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now())  #默认时间是系统当前时间
    updated = models.DateTimeField(auto_created=True)  #每次数据更新时写入当前的时间

    class Meta:
        ordering = ('-created', )  #对现实的文章进行(倒)排序

    def __str__(self):
        return self.title
