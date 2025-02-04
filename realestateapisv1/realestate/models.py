from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy

# Create your models here.

class UserRole(models.TextChoices):
    TENANT = 'tenan', gettext_lazy("Tenant")
    INNKEEPER = 'innkr', gettext_lazy("Innkeeper")
    ADMIN = 'admin', gettext_lazy("Adminstrator")


class ApproveState(models.TextChoices):
    CANCEL = 'cc', gettext_lazy('Cancel')
    PENDING = 'pd', gettext_lazy('Pending')
    CONFIRM = 'cf', gettext_lazy('Confirm')


class CurrencyUnit(models.TextChoices):
    VIETNAM_DONG = 'vnd', gettext_lazy('Vietnam Dong')
    DOLLAR = 'dol', gettext_lazy('Dollar')


class HouseState(models.TextChoices):
    EMPTY = 'em', gettext_lazy('Con trong')
    EXECUTING = 'ex', gettext_lazy('Dang xu li')
    NO_SPACE = 'ns', gettext_lazy('Khong con cho')


class TypeAcquisition(models.TextChoices):
    RENT = 'ren', gettext_lazy('Cho thue')
    BUY = 'buy', gettext_lazy('Mua')
    ORDER = 'odr', gettext_lazy('Dat truoc')


class TypeHouse(models.TextChoices):
    APARTMENT = 'apar', gettext_lazy("Can ho")
    HOME = 'home', gettext_lazy('Nha rieng')
    VILLA = 'vill', gettext_lazy('Biet thu')
    STREET_HOUSE = 'strh', gettext_lazy('Nha mac pho')
    SHOP_HOUSE = 'shph', gettext_lazy('Shop')
    OFFICE = 'offc', gettext_lazy('Nha van phong')
    FACTORY = 'fact', gettext_lazy('Nha xuong')
    OTHER = 'othr', gettext_lazy('Nha loai khac')


class TypeOwnership(models.TextChoices):
    FULL = 'full', gettext_lazy('Nguyen can')
    PART = 'part', gettext_lazy('Mot phan')
    ROOM = 'room', gettext_lazy('Mot phong')
    FLOOR = 'flor', gettext_lazy('Mot tang')


class InteriorState(models.TextChoices):
    NOT_YET = 'noye', gettext_lazy('Chua co')
    HAVE = 'have', gettext_lazy('Da co')


class User(AbstractUser):
    avatar = CloudinaryField(null=False, default="image/upload/v1738591988/240_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws_okujdi.jpg")
    user_role = models.CharField(max_length=5, null=False, choices=UserRole.choices, default=UserRole.TENANT)

    def getRole(self):
        return 'User'


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class Article(models.Model):
    title = models.CharField(max_length=250, null=False)
    content = models.TextField(null=False)

    class Meta:
        abstract = True


class Address(models.Model):
    longtitude = models.FloatField(null=False)
    latetitude = models.FloatField(null=False)
    house = models.ForeignKey('HouseArticle', on_delete=models.CASCADE, unique=True)


class Deposit(models.Model):
    value = models.FloatField(null=False)
    currency_unit = models.CharField(max_length=3, choices=CurrencyUnit.choices, default=CurrencyUnit.VIETNAM_DONG)


class HouseArticle(Article, BaseModel):
    contact = models.CharField(max_length=11, null=False)
    location = models.CharField(max_length=250, null=False)
    approve_state = models.CharField(max_length=2, choices=ApproveState.choices, default=ApproveState.PENDING)
    deposit = models.ForeignKey(Deposit, on_delete=models.DO_NOTHING, null=False, default=0)
    area = models.FloatField(null=False, default=0)


class AdditionalInfo(models.Model):
    name = models.CharField(max_length=20, null=False)
    value = models.CharField(max_length=20, null=False)
    icon = models.CharField(max_length=20, default="tag")
    house = models.ForeignKey(HouseArticle, on_delete=models.DO_NOTHING)


class HouseBonusInfo(models.Model):
    house_state = models.CharField(max_length=2, null=True, choices=HouseState.choices)
    type_acquisition = models.CharField(max_length=3, null=True, choices=TypeAcquisition.choices)
    type_house = models.CharField(max_length=4, null=True, choices=TypeHouse.choices)
    type_ownership = models.CharField(max_length=4, null=True, choices=TypeOwnership.choices)
    interior_state = models.CharField(max_length=4, null=True, choices=InteriorState.choices)

    class Meta:
        abstract = True


class AcquisitionArticle(HouseArticle, HouseBonusInfo):
    allowed_human_quantity = models.IntegerField(null=False)
    legal_documents = models.CharField(max_length=20, null=False)
    innkeeper = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    display_image = CloudinaryField(default="image/upload/v1738630067/1-mua-nha-cu_yb4v56.jpg")

    house_state = models.CharField(max_length=2, null=False, choices=HouseState.choices, default=HouseState.EMPTY)
    type_acquisition = models.CharField(max_length=3, null=False, choices=TypeAcquisition.choices, default=TypeAcquisition.RENT)
    type_house = models.CharField(max_length=4, null=False, choices=TypeHouse.choices, default=TypeHouse.HOME)
    type_ownership = models.CharField(max_length=4, null=False, choices=TypeOwnership.choices, default=TypeOwnership.FULL)
    interior_state = models.CharField(max_length=4, null=False, choices=InteriorState.choices, default=InteriorState.NOT_YET)


class LookingArticle(HouseArticle, HouseBonusInfo):
    tenant = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)


class Image(models.Model):
    uri = CloudinaryField()
    acquisition_article = models.ForeignKey(AcquisitionArticle, on_delete=models.CASCADE)

