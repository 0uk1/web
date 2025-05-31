from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.CharField(max_length=100, verbose_name="Автор")
    year = models.IntegerField(verbose_name="Год издания")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", default=0)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Добавлено")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='books/', blank=True, null=True, verbose_name="Изображение")

    def __str__(self):
        return f"{self.title} ({self.author})"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Корзина")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def total_price(self):
        return self.book.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    items = models.ManyToManyField(CartItem, verbose_name="Товары")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing', verbose_name="Статус")

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"