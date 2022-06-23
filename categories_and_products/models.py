from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

# Create your models here.


class Game(models.Model):
    gameName = models.CharField(max_length=250, blank=True)
    Gameslug = models.SlugField(unique=True, db_index=True)
    profile_image = models.ImageField(upload_to="games", blank=True)
    background_image = models.ImageField(upload_to="games", blank=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
        

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

       
    def get_absolute_url(self):
        return reverse('categories_and_products:GamesCodes', args=[self.Gameslug])

    
    def __str__(self):
        return self.gameName

    class Meta:
        verbose_name_plural = "Games"

class Code_Categories(models.Model):
    codeCategory = models.CharField(max_length=250, blank=True)
    categoryslug = models.SlugField(unique=True, db_index=True)
    image = models.ImageField(upload_to="categories", blank=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True,)
    price = models.FloatField(default=0)
    Most_Popular = models.BooleanField(default=False)
    Best_Offer = models.BooleanField(default=False)
    New_Products = models.BooleanField(default=False)

     

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.codeCategory
    
    def get_absolute_url(self):
        return reverse('categories_and_products:code_details', args=[self.id])


    # def discountpercentage(self):
    #     if self.oldPrice :
    #         discountAmount = self.oldPrice - self.price
    #         self.offPercentage = (discountAmount/self.oldPrice) * 100
    #         return (int(self.offPercentage))
    #     else:
    #         pass
    # offerPercentage = property(discountpercentage)

    class Meta:
        verbose_name_plural = "Code Categories"


class Codes(models.Model):    
    code = models.CharField(max_length=1000, blank=True)
    category = models.ForeignKey(Code_Categories, on_delete=models.CASCADE, blank=True, null=True,)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField()

    def __str__(self):
        return self.code


    
    class Meta:
        verbose_name_plural = "Codes"


class PromoCode(models.Model):
    Promocode = models.CharField(max_length=10, unique=True, blank=True,null=True)
    percentage = models.FloatField(default=0.0, validators=[
                                   MinValueValidator(0.0), MaxValueValidator(1.0)], blank=True,null=True,)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.percentage = round(self.percentage, 2)
        super(PromoCode, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "PromoCodes"
