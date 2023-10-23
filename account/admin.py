from django.contrib import admin
from account.models import (
    User
)

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    
    # @admin.display(description="belong_to")
    # def admin_belong_to(self,instance):
    #     return ", ".join(_.name for _ in instance.belong_to.all())

    list_display = ['user_uid','username','email','is_superuser','is_staff','is_active']


    class Meta:
        model = User

admin.site.register(User,UserAdmin)