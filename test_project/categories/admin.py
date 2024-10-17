from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_at",
        "updated_at",
    )
    
    search_fields = ("title",)
    list_per_page = 10
    ordering = ("created_at",)
    readonly_fields = ("created_at", "updated_at")  

    fieldsets = (
        ('Informations de catégorie', {
            'fields': ('title',)
        }),
        ('Données de suivi', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    list_filter = ('created_at',)


admin.site.register(Category, CategoryAdmin)
