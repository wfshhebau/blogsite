from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class BlogArticles(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(User,related_name="blog_posts",on_delete=models.CASCADE)
    # 注意：django2.0后,表与表之间关联的时候,必须要写on_delete参数,否则会报异常
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-publish",)      # 注意：这个逗号很关键，因为ordering要求tuple或list，没有逗号就不是tuple

    def __str__(self):
        return self.title