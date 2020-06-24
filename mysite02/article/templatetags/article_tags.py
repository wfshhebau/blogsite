from django import template
register = template.Library()

from article.models import ArticlePost


#+++++++++++++++显示文章的总数++++++++++++++++
@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()

#+++++++++++++++显示某一作者的文章总数++++++++++++++++
@register.simple_tag
def author_total_articles(user):    # 在article/models.py中，ArticlePost与User有个外键，related_name="article"
    return user.article.count()


#+++++++++++++++汇总最新发布的文章++++++++++++++++
@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by("-created")[:n]
    return {"latest_articles":latest_articles}


#+++++++++++++++汇总评论最多的(n)篇文章++++++++++++++++
# models中的Comment与ArticlePost之前有个外键：related_name="comments")
from django.db.models import Count
@register.simple_tag
def most_commented_articles(n=3):
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by("-total_comments")[:n]



#+++++++++++++++自定义模板选择器(过滤器)函数----将Markdown编码转成HTML代码++++++++++++++++
from django.utils.safestring import mark_safe
import markdown
@register.filter(name='markdown')    # name='markdown'的作用是重命名markdown_filter(text)，为什么不能直接使用markdown(text)呢？因为import markdown
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))

