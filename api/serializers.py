from rest_framework import serializers
from .models import (
    Project, ProjectImage, Category,
    Product, ProductCategory, CartItem, Favorite, Order,
    TeamMember, ClientLogo, DesignRequest, ContactMessage, SiteSettings
)
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


# Project Image Serializer
class ProjectImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectImage
        fields = '__all__'



class CategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)

    class Meta:
        model = Category
        fields = ['id', 'translations']

class ProjectSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Project)
    category = CategorySerializer(read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Project
        fields = ['id', 'translations', 'category', 'category_id', 'created_at', 'images']



# Product Catalog
class ProductCategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ProductCategory)

    class Meta:
        model = ProductCategory
        fields = ['id', 'translations']

class ProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)
    category = ProductCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'translations', 'image', 'price_per_day', 'category', 'category_id', 'availability', 'qty']


# Cart, Favorites, Orders
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ['user'] 

class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ['user']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


# Team & Client Logos
class TeamMemberSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=TeamMember)
    
    class Meta:
        model = TeamMember
        fields = ['id','translations','photo']

class ClientLogoSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ClientLogo)
    
    class Meta:
        model = ClientLogo
        fields = ['id','translations','logo']


# Forms


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'





class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'is_admin']

    def get_is_admin(self, obj):
        return obj.is_staff or obj.is_superuser

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'is_admin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class DesignRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = DesignRequest
        fields = '__all__'