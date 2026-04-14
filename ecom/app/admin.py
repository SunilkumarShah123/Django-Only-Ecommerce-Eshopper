from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_display = ("email", "username", "is_staff", "is_superuser", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("username",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    search_fields = ("email", "username")
    ordering = ("email",)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', )

admin.site.register(Category,CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'sub_slug': ('subname',)}
    list_display = ('subname', 'sub_slug','cate__name' )

admin.site.register(SubCategory,SubCategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'slug','category__name','sub_category__subname' )

admin.site.register(Product,ProductAdmin)

class CarouselAdmin(admin.ModelAdmin):
    list_display = ('heading', 'subheading', 'carsousel_product')

admin.site.register(carsousel, CarouselAdmin)

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'brand_slug': ('title',)}
    list_display = ('title',)   

admin.site.register(Brand,BrandAdmin)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'phone_number')
    search_fields = ('name', 'email', 'phone_number')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'product', 'user', 'created_at')
    search_fields = ('comment', 'product__product_name', 'user__username')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'date', 'is_pay')
    search_fields = ('product__product_name', 'user__username')

