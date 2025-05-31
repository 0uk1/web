from django.urls import path
from .views import (
    BookListView, BookCreateView, BookUpdateView, BookDeleteView,
    RegisterView, LoginView, ProfileView, CartView, AddToCartView,
    RemoveFromCartView, OrderCreateView, OrderDetailView, OrderListView
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('<int:pk>/update/', BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),

    # Аутентификация
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='book_list'), name='logout'),

    # Личный кабинет
    path('profile/', ProfileView.as_view(), name='profile'),

    # Корзина
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<int:book_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', RemoveFromCartView.as_view(), name='remove_from_cart'),

    # Заказы
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/', OrderListView.as_view(), name='order_list'),
]