from django.shortcuts import render
from rest_framework.viewsets import ViewSet, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from realestate import serializers
from realestate.models import AcquisitionArticle, Image, Address, Deposit, User, HouseArticle, LookingArticle, AdditionalInfo
from realestate.paginators import ArticlePaginator
from realestate.models import Image
from rest_framework import status
from oauth2_provider.models import Application
from rest_framework import permissions
from realestate import perms
from django.db.models import Q

# Create your views here.

class HouseArticleViewSet(ViewSet, generics.ListAPIView):
    queryset = HouseArticle.objects.filter(active=True).all()
    serializer_class = serializers.HouseArticleSerializer

    def deposit_execute_create(self, request, **kwargs):
        data = request.data.copy()
        deposit = data.pop('deposit')
        #before create
        for k, v in kwargs.items():
            data[k] = v

        if deposit:
            data['deposit'] = Deposit.objects.create(**deposit).id

        return data
    
    def get_queryset(self):
        query = super().get_queryset()
        User.objects.filter()
        
        params = self.request.query_params

        print(params)

        location = params.get('location', None)
        start_deposit = params.get('start_deposit', 0)
        end_deposit = params.get('end_deposit', 100000000)
        start_area = params.get('area', 0)
        end_area = params.get('end_area', 100000000)

        if location:
            p_location = location.strip().split(' ')
            query_where = Q()
            for p in p_location:
                query_where &= Q(location__icontains=p)
            
            query.filter(query_where)
        
        query = query.filter(Q(deposit__value__gt=start_deposit) & Q(deposit__value__lt=end_deposit))
        query = query.filter(Q(area__gt=start_area) & Q(area__lt=end_area))

        return query
    
    @action(methods=['get'], detail=True, url_path='additionals')
    def get_additional_infos(self, request, pk):
        adds = self.get_object().additionalinfo_set.all()
        return Response(serializers.AdditionalInfoSerializer(adds, many=True).data)


class AcquisitionViewSet(HouseArticleViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = AcquisitionArticle.objects.filter(active=True).all()
    serializer_class = serializers.AcquisitionArticleSerializer
    pagination_class = ArticlePaginator

    def get_queryset(self):
        query = super().get_queryset()

        human_quantity = self.request.query_params.get('human_quantity',0)
        query = query.filter(allowed_human_quantity__gte=human_quantity)

        return query
    
    def get_permissions(self):
        if self.action in ['create']:
            return [perms.InnkeeperPermission()]

        return super().get_permissions()
    
    # can chung thuc
    def create(self, request, *args, **kwargs):
        data_clone = request.data.copy()
        images = data_clone.pop('images')
        address = data_clone.pop('address')

        data_clone = self.deposit_execute_create(request, innkeeper=request.user.id)
        
        #create obj in model
        serializer = self.get_serializer(data=data_clone)
        serializer.is_valid(raise_exception=True)
        ac_article = serializer.save()
        headers = self.get_success_headers(serializer.data)

        #after create
        if address:
            Address.objects.create(**address, house=ac_article)
        if images:
            for image in images:
                Image.objects.create(**image, acquisition_article= ac_article)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        data = self.get_object()
        return Response(serializers.AcquisitionArticleDetailSerializer(data).data)

    @action(methods=['get', 'post'], detail=True, url_path='images')
    def get_images(self, request, pk):
        if request.method.__eq__('POST'):
            print("have access to post method")
            print(request.data)
            image = Image.objects.create(**request.data, acquisition_article= self.get_object())
            return Response(serializers.ImageSerializer(image).data)
        else:
            print("have access to get method")
            
            data = self.get_object().image_set.all()
            return Response(serializers.ImageSerializer(data, many=True).data)
    
    @action(methods=['get'], detail=True, url_path='address')
    def get_address(self, request, pk):
        data = self.get_object().address_set.first()
        if data:
            return Response(serializers.AddressSerializer(data).data)
        else:
            return Response(None, status=status.HTTP_204_NO_CONTENT)


class LookingViewSet(HouseArticleViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = LookingArticle.objects.filter(active=True).all()
    serializer_class = serializers.LookingArticleSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [perms.TenantPermission()]
        return super().get_permissions()

    
    def retrieve(self, request, *args, **kwargs):
        return Response(serializers.LookingArticleDetailSerializer(request.data).data)

    
    def create(self, request, *args, **kwargs):
        data_clone = request.data.copy()
        data_clone = self.deposit_execute_create(request, tenant=request.user.id)
        serializer = self.get_serializer(data=data_clone)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AdditionalInfoViewSet(ViewSet, generics.ListAPIView):
    queryset = AdditionalInfo.objects.all()
    serializer_class = serializers.AdditionalInfoSerializer


class UserViewSet(ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        u = serializer.save()
        headers = self.get_success_headers(serializer.data)
        
        data_res = serializer.data.copy()
        app = Application.objects.create(
            user=u,
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD,
            name='RealEstateClient',
        )

        data_res['client_id']=app.client_id
        data_res['client_secret']=app.client_secret

        return Response(data_res, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'],detail=False, url_path='current-user', permission_classes=[permissions.IsAuthenticated])
    def get_current_user(self, request):
        return Response(serializers.UserSerializer(request.user).data)