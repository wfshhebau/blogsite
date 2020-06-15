from django.shortcuts import render, get_object_or_404
from .models import BlogArticles

# Create your views here.
# 1.3.1 显示标题  p24
def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request,"blog/titles.html",{"blogs":blogs})

# 1.3.2 显示内容  p29
def blog_article(request,article_id):
    #article = BlogArticles.objects.get(id=article_id)
    article = get_object_or_404(BlogArticles,id=article_id)     # 引入该方法，当网页不存在自动返回404
    pub = article.publish
    return render(request,"blog/content.html",{"article":article,"publish":pub})
