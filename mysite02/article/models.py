from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ArticleColumn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_column')
    column = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)      # the column created time

    def __str__(self):
        return self.column



#++++++++++++++++文章标签数据模型++++++++++
# 注意：1 要写在ArticlePost的前面；2 要在ArticlePost()中加article_tag字段
class ArticleTag(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="tag")
    tag = models.CharField(max_length=300)
    def __str__(self):
        return self.tag




#++++++++++++++++发表文章的数据模型++++++++++
# Creat 文章Post的Modle
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from slugify import slugify
class ArticlePost(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="article")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    column = models.ForeignKey(ArticleColumn,on_delete=models.CASCADE,related_name="article_column")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    # P167 Chap4.3 点赞功能
    users_like = models.ManyToManyField(User,related_name="articles_like",blank=True)
    # P195 Chap4.7.1 文章标签
    article_tag = models.ManyToManyField(ArticleTag,related_name="article_tag",blank=True)


    class Meta:
        ordering = ("title",)
        index_together = (("id","slug"),)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(ArticlePost,self).save(*args,**kwargs)

    # 获取链接地址中的id和slug，传给article.urls下的name=article_detail的url
    def get_absolute_url(self):
        return reverse("article:article_detail", args=[self.id,self.slug])

    # 获取链接地址中的id和slug，传给article.urls下的name=list_article_detail的url
    def get_url_path(self):
        return reverse("article:list_article_detail",args=[self.id,self.slug])



# 创建评论Comment数据模型
from django.db import models
from django.contrib.auth.models import User
class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name="comments")
    commentator = models.CharField(max_length=30)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return "comment by {0} on {0}".format(self.commentator.username, self.article)    # 为啥要有.username呢？

