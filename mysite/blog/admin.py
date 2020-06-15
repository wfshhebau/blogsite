from django.contrib import admin

from .models import BlogArticles
# Register your models here.

# 添加 BlogArticlesAdmin()，使显示内容更丰富
class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish")
    list_filter = ("publish", "author")
    search_fields = ("title", "body")
    raw_id_fields = ("author",)   # 注意逗号
    date_hierarchy = "publish"
    ordering = ['-publish','author']

admin.site.register(BlogArticles, BlogArticlesAdmin)
# 注意:将模型类和内联类一起注册，因为内联类BlogArticlesAdmin中没有模型,不符合django模型注册规则