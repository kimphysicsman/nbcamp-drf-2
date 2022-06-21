from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    list_display_links = ('id', 'title', 'author')
    list_filter = ('author', )
    search_fields = ('title', 'author')

    fieldsets = (
        ("info", {'fields': ('title', 'content', 'created_at',)}),
        ('show_date', {'fields': ('show_start_at', 'show_end_at', )}),
        ('thumbnail', {'fields': ('thumbnail', )}),
        )
    
    def get_readonly_fields(self, request, obj=None):
        return ('created_at', )


admin.site.register(Product, ProductAdmin)