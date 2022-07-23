from django.contrib import admin
from cart_and_orders.admin import CodesAdmin
from cart_and_orders.models import Codes

from categories_and_products.models import Game, PromoCode,Code_Categories

# Register your models here.



class GameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'Gameslug': ('gameName',), }
    list_filter = ("gameName", "created",)
    list_display = ('gameName', "created", "id",)
    search_fields = ['gameName']

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        form.base_fields["background_image"].help_text = " * width: 1000px, height: 312px are recommended"
        form.base_fields["profile_image"].help_text = " * width: 2048px, height: 2048px are recommended"
        return form


class Code_Categories_Admin(admin.ModelAdmin):
    prepopulated_fields = {'categoryslug': ('codeCategory',), }
    list_filter = ("codeCategory", "created",)
    list_display = ('codeCategory', "created", "price","game","active","id","New_Products","Most_Popular","Best_Offer")
    search_fields = ['codeCategory']

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        form.base_fields["background_image"].help_text = " * width: 1000px, height: 312px are recommended"
        form.base_fields["image"].help_text = " * width: 2048px, height: 2048px are recommended"
        return form

class PromoCodeAdmin(admin.ModelAdmin):
    list_filter = ("active", "Promocode",)
    list_display = ('Promocode', "percentage", 'created', "active")

    search_fields = ['Promocode']





admin.site.register(Game, GameAdmin)
admin.site.register(Code_Categories, Code_Categories_Admin)


# admin.site.register(PromoCode, PromoCodeAdmin)
