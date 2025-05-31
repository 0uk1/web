from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Book, Cart, CartItem, Order
from .forms import BookForm, UserRegisterForm, CustomLoginForm, UserProfileForm, CartItemForm
from django.contrib.auth import login


class BookListView(ListView):
    model = Book
    ordering = ['title']
    paginate_by = 5
    template_name = 'store/book_list.html'


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'store/book_form.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'store/book_form.html'
    success_url = reverse_lazy('book_list')


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'store/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')


class RegisterView(FormView):
    template_name = 'store/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'store/login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        # Добавьте этот импорт в начале файла
        from django.contrib.auth import login

        login(self.request, form.get_user())
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'store/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        context['cart'] = cart
        return context


class AddToCartView(LoginRequiredMixin, CreateView):
    model = CartItem
    form_class = CartItemForm

    def form_valid(self, form):
        book = get_object_or_404(Book, pk=self.kwargs['book_id'])
        cart, created = Cart.objects.get_or_create(user=self.request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book,
            defaults={'quantity': form.cleaned_data['quantity']}
        )

        if not created:
            cart_item.quantity += form.cleaned_data['quantity']
            cart_item.save()

        messages.success(self.request, f"{book.title} добавлен в корзину")
        return redirect('book_list')


class RemoveFromCartView(LoginRequiredMixin, DeleteView):
    model = CartItem
    success_url = reverse_lazy('cart')

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = []

    def form_valid(self, form):
        cart = get_object_or_404(Cart, user=self.request.user)
        if not cart.items.exists():
            messages.error(self.request, "Ваша корзина пуста")
            return redirect('cart')

        order = form.save(commit=False)
        order.user = self.request.user
        order.total_price = cart.total_price()
        order.save()

        for item in cart.items.all():
            order.items.add(item)

        cart.items.all().delete()
        messages.success(self.request, "Заказ успешно оформлен")
        return redirect('order_detail', pk=order.pk)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'store/order_detail.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'store/order_list.html'
    ordering = ['-created_at']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)