

# Register your models here.
from django.contrib import admin

from parler.admin import TranslatableAdmin


from .models import *

# Register your models here.

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('__str__',)
    search_fields = ('translations__name',) 

@admin.register(Project)
class ProjectAdmin(TranslatableAdmin):
    list_display = ('__str__', 'category', 'created_at')
    search_fields = ('translations__name',) 


@admin.register(ProductCategory)
class ProductCategoryAdmin(TranslatableAdmin):
    list_display = ['id', 'get_name']
    search_fields = ('translations__name',) 

    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)
    get_name.short_description = 'Name'


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['id', 'get_name', 'price_per_day', 'availability', 'qty', 'category']

    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)
    get_name.short_description = 'Name'


@admin.register(TeamMember)
class TeamMemberAdmin(TranslatableAdmin):
    list_display = ['id', 'get_name', 'get_title']

    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)
    get_name.short_description = 'Name'

    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)
    get_title.short_description = 'Title'


@admin.register(ClientLogo)
class ClientLogoAdmin(TranslatableAdmin):
    list_display = ['id', 'get_name']

    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)
    get_name.short_description = 'Name'


admin.site.register(ProjectImage)

admin.site.register(Favorite)

admin.site.register(CartItem)

admin.site.register(Order)

admin.site.register(DesignRequest)

admin.site.register(ContactMessage)

admin.site.register(SiteSettings)


