from rest_framework.serializers import ModelSerializer
from realestate.models import AcquisitionArticle, Image, Address, User, LookingArticle, HouseArticle, Deposit, AdditionalInfo
from cloudinary.utils import cloudinary_url

class CloudinaryModelSerializer(ModelSerializer):
    fields_mapping = {}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # xu li mapping name ve image general execute
        for old_name, new_name in self.fields_mapping.items():
            if old_name in data:
                if new_name.__eq__('image'):
                    image_source = data[old_name].split("image/upload/")[1]
                    data[old_name] = cloudinary_url(image_source, secure=True)[0]
            

        return data


class UserSerializer(CloudinaryModelSerializer):
    fields_mapping = {"avatar": "image"}

    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)

        u.set_password(u.password)
        u.save()
        
        print(u)

        return u

    class Meta:
        model = User
        fields = ['id', 'username', 'password','user_role', 'first_name', 'last_name', 'email', 'is_active', 'avatar']


class HouseArticleSerializer(ModelSerializer):

    class Meta:
        model = HouseArticle
        fields = '__all__'


class DepositSerializer(ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'


class AcquisitionArticleSerializer(CloudinaryModelSerializer):
    fields_mapping = {"display_image": "image"}
    deposit = DepositSerializer()

    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        required_fields = ['id', 'title', 
                           'display_image', 'location', 
                           'contact', 'deposit', 'area',
                           'updated_date']  # Các trường cần hiển thị
        for field in list(representation.keys()):
            if field not in required_fields:
                representation.pop(field)  # Xóa các trường không cần thiết

        return representation

    class Meta:
        model = AcquisitionArticle
        fields = '__all__'


class ImageSerializer(CloudinaryModelSerializer):
    fields_mapping = {'uri': 'image'}

    class Meta:
        model = Image
        fields = ['id', 'uri']


class AcquisitionArticleDetailSerializer(AcquisitionArticleSerializer):
    innkeeper = UserSerializer()

    class Meta:
        model = AcquisitionArticleSerializer.Meta.model
        exclude = ['active']


class LookingArticleSerializer(ModelSerializer):
    deposit = DepositSerializer()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        required_fields = ['id', 'title', 'location',
                           'deposit', 'area',
                            'contact', 'updated_date']
        for field in list(data.keys()):
            if field not in required_fields:
                data.pop(field)  # Xóa các trường không cần thiết
        return data

    class Meta:
        model = LookingArticle
        fields = '__all__'


class LookingArticleDetailSerializer(LookingArticleSerializer):
    class Meta:
        model = LookingArticleSerializer.Meta.model
        exclude = ['active']
        

class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['longtitude', 'latetitude', 'house']

    
class AdditionalInfoSerializer(ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = '__all__'

