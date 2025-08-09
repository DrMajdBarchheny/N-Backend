from django.urls import path
from ..views import apiViews

urlpatterns = [
    # Category
    path('api/categories/', apiViews.category_list, name='category-list'),

    # Projects
    path('api/projects/', apiViews.project_list, name='project-list'),
    path('api/projects/<int:pk>/', apiViews.project_detail, name='project-detail'),
    path('api/add-images/', apiViews.add_images, name='add-images'),    
    

    # Products
    path('api/products/', apiViews.product_list, name='product-list'),
    path('api/products/<int:pk>/', apiViews.product_detail, name='product-detail'),

    # Cart
    path('api/cart/', apiViews.cart_items, name='cart-items'),
    path('api/cart/<int:pk>/', apiViews.delete_cart_item, name='delete-cart-item'),

    # Favorites
    path('api/favorites/', apiViews.favorites_list, name='favorites-list'),
    path('api/favorites/<int:pk>/', apiViews.delete_favorite, name='delete-favorite'),

    # Orders
    path('api/orders/', apiViews.orders_list, name='orders-list'),

    # Team
    path('api/team/', apiViews.team_list, name='team-list'),

    # Clients
    path('api/clients/', apiViews.clients_list, name='clients-list'),

    # Design Request
    path('api/design-request/', apiViews.submit_design_request, name='design-request'),
    path('api/design-request-list/', apiViews.design_request_list, name='design-request-list'),#admin
    path('api/design-request-detail/<int:pk>/', apiViews.design_request_detail, name='design-request-detail'),



] 
