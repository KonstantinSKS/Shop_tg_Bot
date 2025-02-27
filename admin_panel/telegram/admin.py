from django.contrib import admin
from django.contrib.auth.models import Group

from admin_panel.telegram.models import TgUser, Product, Category, Subcategory


admin.site.unregister(Group)


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'is_unblocked',
        'bot_unblocked',
        'is_subscribed',
    )

    def has_add_permission(self, request, obj=None):
        """Убирает возможность создания пользователей через админку."""
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + (
                'id', 'username', 'bot_unblocked', 'is_subscribed')
        return self.readonly_fields


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'image',
        'subcategory',
    )
    list_filter = (
        'title',
        'subcategory',)
    search_fields = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
    )
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'category',
    )
    search_fields = ('title',)
    list_filter = ('category',)
