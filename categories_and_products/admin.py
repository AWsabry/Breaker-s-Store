from django.contrib import admin

from categories_and_products.models import Game, Codes, PromoCode,Code_Categories

# Register your models here.



class GameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'Gameslug': ('gameName',), }
    list_filter = ("gameName", "created",)
    list_display = ('gameName', "created", "id",)
    search_fields = ['gameName']


class Code_Categories_Admin(admin.ModelAdmin):
    prepopulated_fields = {'categoryslug': ('codeCategory',), }
    list_filter = ("codeCategory", "created",)
    list_display = ('codeCategory', "created", "price","game","id","New_Products","Most_Popular","Best_Offer")
    search_fields = ['codeCategory']


class CodesAdmin(admin.ModelAdmin):
    list_filter = ("code", "category", "created")
    list_display = ("code", "category",
                    "stock", "id", "created", "active",)
    list_display_links = [
        'category',
    ]
    search_fields = ['codeName']


class PromoCodeAdmin(admin.ModelAdmin):
    list_filter = ("active", "Promocode",)
    list_display = ('Promocode', "percentage", 'created', "active")

    search_fields = ['Promocode']





admin.site.register(Game, GameAdmin)
admin.site.register(Code_Categories, Code_Categories_Admin)
admin.site.register(Codes, CodesAdmin)
# admin.site.register(PromoCode, PromoCodeAdmin)
