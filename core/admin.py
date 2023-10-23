from django.contrib import admin
from .models import (
    Exchange,
    CryptoCurrencyPair
)
# Register your models here.

class ExchangeAdmin(admin.ModelAdmin):
    
    # @admin.display(description="belong_to")
    # def admin_belong_to(self,instance):
    #     return ", ".join(_.name for _ in instance.belong_to.all())

    list_display = ['uid','name','created_at','updated_at']


    class Meta:
        model = Exchange


class CryptoCurrencyPairAdmin(admin.ModelAdmin):
    
    # @admin.display(description="belong_to")
    # def admin_belong_to(self,instance):
    #     return ", ".join(_.name for _ in instance.belong_to.all())

    list_display = ['uid','exchange','symbol','created_at','updated_at']


    class Meta:
        model = CryptoCurrencyPair

admin.site.register(CryptoCurrencyPair,CryptoCurrencyPairAdmin)
admin.site.register(Exchange,ExchangeAdmin)