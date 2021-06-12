from django.contrib import admin
from .models import Customer, Product, Order, Tag, Comment, OrderItem, ShippingInformation, Payment
# Register your models here.
admin.site.register(Customer);
admin.site.register(Product);
admin.site.register(Order);
admin.site.register(Tag);
admin.site.register(Comment);
admin.site.register(OrderItem);
admin.site.register(ShippingInformation);
admin.site.register(Payment);
