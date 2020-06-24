from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
# 创建数据模型类,继承自 django.db.models.Model
class BlogArticles(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_post")
    # ForeignKey()反应“一对多”关系，这里就是User对BlogArticles。User.related_name可反向查询BlogArticles
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-publish",)   # ,号很关键

    def __str__(self):
        return self.title


