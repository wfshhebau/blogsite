from django.shortcuts import render
from .models import  BlogArticles

# Create your views here.
# 1.3.1 Display titles  p24
def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request, "blog/titles.html", {"blogs":blogs})

# 1.3.2 Check and Display article's content
def blog_article(request, article_id):
    article = BlogArticles.objects.get(id=article_id)
    pub = article.publish    # get publish time to ver pub
    return render(request, "blog/content.html",{"article":article,"publish":pub})



