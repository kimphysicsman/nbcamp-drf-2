from django.contrib import admin
from .models import Product, Review
from django.utils.html import mark_safe

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_preview','title', 'author']
    list_display_links = ('id', 'title', 'author')
    list_filter = ('author', )
    search_fields = ('title', 'author')

    fieldsets = (
        ("info", {'fields': ('title', 'content', 'created_at',)}),
        ('show_date', {'fields': ( 'show_end_at', )}),
        ('thumbnail', {'fields': ('thumbnail', 'image_tag', )}),
        )
    
    def get_readonly_fields(self, request, obj=None):
        return ('created_at', 'image_tag', )

    def image_tag(self, obj):
        if obj.thumbnail:
            return mark_safe(f'<img src="{obj.thumbnail.url}" width="150" height="150" />')
        return None

    def image_preview(self, obj):
        if obj.thumbnail:
            return mark_safe(f'<img src="{obj.thumbnail.url}" width="50" height="50" />')
        return None
    
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

admin.site.register(Product, ProductAdmin)
admin.site.register(Review)