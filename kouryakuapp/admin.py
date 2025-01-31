from django.contrib import admin

# Register your models here.

from .models import Category, KouryakuPost,Comment,AdminUpdate

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'title')
  list_display_links = ('id', 'title')
admin.site.register(Category, CategoryAdmin)

class KouryakuPostAdmin(admin.ModelAdmin):
  list_display = ('id', 'title')
  list_display_links = ('id', 'title')
admin.site.register(KouryakuPost, KouryakuPostAdmin)

admin.site.register(Comment)
admin.site.register(AdminUpdate)