from django.contrib import admin
from realestate.models import User, HouseArticle, AcquisitionArticle, Image, LookingArticle, Deposit

# Register your models here.


admin.site.register(User)
admin.site.register(HouseArticle)
admin.site.register(AcquisitionArticle)
admin.site.register(LookingArticle)
admin.site.register(Image)
admin.site.register(Deposit)