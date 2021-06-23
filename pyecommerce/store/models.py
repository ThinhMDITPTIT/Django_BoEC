from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    dob = models.DateField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username


def create_customer(sender, **kwargs):
    if kwargs['created']:
        customer = Customer.objects.create(user=kwargs['instance'])


post_save.connect(create_customer, sender=User)


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Crop Top', 'Crop Top'),
        ('Jacket', 'Jacket'),
        ('Pant', 'Pant'),
        ('Shoes', 'Shoes'),
        ('Sport equipment', 'sport equipment'),
    )
    name = models.CharField(max_length=255, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=255, null=True, choices=CATEGORY)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images")
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    # @property
    # def get_product_by_name(self):
    #     orderitems = self.orderitem_set.all()
    #     totalprice = sum([item.get_total for item in orderitems])
    #     return totalprice

class Comment(models.Model):
    content = models.TextField()
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, null=True)
    enable = models.BooleanField(default=True)



class Order(models.Model):
    iscompleted = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        totalprice = sum([item.get_total for item in orderitems])
        return totalprice

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        totalitems = sum([item.quantity for item in orderitems])
        return totalitems


class Payment(models.Model):
    CATEGORYPAYMENT = (
        ('COD', 'COD'),
        ('ZALOPAY', 'ZALOPAY'),
        ('MOMO', 'MOMO'),
        ('VNPAY', 'VNPAY'),
    )
    ispay = models.BooleanField(default=False)
    transid = models.CharField(max_length=200, null=True, blank=True)
    method = models.CharField(max_length=200, null=True, choices=CATEGORYPAYMENT)
    order = models.OneToOneField(Order, null=True, on_delete=models.SET_NULL)
    pay_date = models.DateTimeField(auto_now_add=True, null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    @property
    def get_total_price(self):
        total_price = self.order.get_cart_total
        return total_price

    @property
    def payment_factory(self):
        if self.method == "COD":
            self.ispay = False;
        elif self.method == "VNPAY":
            self.ispay = True;
        self.save()


class OrderItem(models.Model):
    OPTION = (
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('XLarge', 'XLarge'),
    )
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    option = models.TextField(max_length=200, null=True, blank=True, choices=OPTION)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingInformation(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancel', 'Cancel'),
    )
    status = models.CharField(max_length=200, choices=STATUS, default='New')
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    order = models.OneToOneField(Order, null=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=11, null=True)
    order_date = models.DateTimeField(verbose_name=('Order Date'))


    def __str__(self):
        return str(self.address) + str(self.city)
