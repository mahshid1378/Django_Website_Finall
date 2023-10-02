from django.contrib import admin
from .models import Article, Category, IPAddress

# Admin header change
admin.site.site_header = "Weblog"

# Register your models here.
def make_published(modeladmin, request, queryset):
        rows_updated = queryset.update(status='p')
        if rows_updated == 1:
            message_bit = "published"
        else:
            message_bit = "publiesd."
        modeladmin.message_user(request, "{} article {}".format(rows_updated, message_bit))
make_published.short_description = "Publication of selected articles"

def make_draft(modeladmin, request, queryset):
        rows_updated = queryset.update(status='d')
        if rows_updated == 1:
            message_bit = "It was drafted."
        else:
            message_bit = "It was drafted."
        modeladmin.message_user(request, "{} article {}".format(rows_updated, message_bit))
make_draft.short_description = "Drafting of selected articles"


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('position', 'title','slug', 'parent','status')
	list_filter = (['status'])
	search_fields = ('title', 'slug')
	prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'thumbnail_tag','slug', 'author', 'jpublish','is_special', 'status', 'category_to_str')
	list_filter = ('publish','status', 'author')
	search_fields = ('title', 'description')
	prepopulated_fields = {'slug': ('title',)}
	ordering = ['-status', '-publish']
	actions = [make_published, make_draft]


admin.site.register(Article, ArticleAdmin)
admin.site.register(IPAddress)