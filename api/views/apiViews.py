
from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# ---------- Category ----------
@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

# ---------- Project ----------
@api_view(['POST'])
@permission_classes([AllowAny])
def add_images(request):
        serializer = ProjectImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)




@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def project_list(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def project_detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        project.delete()
        return Response(status=204)

# ---------- Product ----------
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=204)

# ---------- Cart ----------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def cart_items(request):
    if request.method == 'GET':
        items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=201)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart_item(request, pk):
    try:
        item = CartItem.objects.get(pk=pk, user=request.user)
    except CartItem.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)
    item.delete()
    return Response(status=204)

# ---------- Favorites ----------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def favorites_list(request):
    if request.method == 'GET':
        favs = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_favorite(request, pk):
    try:
        fav = Favorite.objects.get(product_id=pk, user=request.user)
    except Favorite.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)
    fav.delete()
    return Response(status=204)

# ---------- Orders ----------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def orders_list(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# ---------- Team ----------
@api_view(['GET'])
@permission_classes([AllowAny])
def team_list(request):
    team = TeamMember.objects.exclude(id=2)
    
    serializer = TeamMemberSerializer(team, many=True)
    return Response(serializer.data)

# ---------- Clients ----------
@api_view(['GET'])
@permission_classes([AllowAny])
def clients_list(request):
    logos = ClientLogo.objects.all()
    serializer = ClientLogoSerializer(logos, many=True)
    return Response(serializer.data)

# ---------- Design Request ----------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_design_request(request):
    serializer = DesignRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

#admin
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def design_request_list(request):
    requests = DesignRequest.objects.all()
    serializer = DesignRequestSerializer(requests, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def design_request_detail(request, pk):
    try:
        response = DesignRequest.objects.filter(user=pk)
    except DesignRequest.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)
    serializer = DesignRequestSerializer(response,many=True)
    return Response(serializer.data)
    



