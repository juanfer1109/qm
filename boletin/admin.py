from django.contrib import admin

from . import models

class IssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'ed', 'release_date','published',)
    list_filter = ('published',)
    search_fields = ['name', 'ed',]

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('headline', 'issue', 'author',)
    list_filter = ('issue', 'author',)
    search_fields = ['headline', 'main_content',]

admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.Article, ArticleAdmin)
