from django.db import models

# many  to many relationship
class Promotion(models.Model):
    description =  models.CharField(max_length=255)
    discount = models.FloatField()
    

class Collection(models.Model):
    title = models.CharField(max_length=255)
    # show the circular dependency  sol
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null= True, related_name='+')
    
    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['title']
    

class Product(models.Model):
    title = models.CharField(max_length=100)
   # A slug is a short label for something, containing only letters, numbers, underscores or hyphens.
   # They're generally used in URLs. In this example, we're using them so that we can have nice URLs
   # for products.
    slug = models.SlugField()
    description = models.TextField(null=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)

    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['title']

class Customer(models.Model):
    # store the default value
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    # choices in django
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        ('MEMBERSHIP_SILVER', 'Silver'),
        ('MEMBERSHIP_GOLD', 'Gold'),

    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=50, choices=MEMBERSHIP_CHOICES, default='MEMBERSHIP_BRONZE')
    def __str__(self):
        # combine first name and last name with th f string
        return f'{self.first_name} {self.last_name}'
    class Meta:
        ordering = ['first_name', 'last_name']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

   # A list of tuples. Each tuple has two elements. The first element is the value that will be stored
   # in the database. The second element is the human-readable value that will be displayed in the
   # admin.
    PAYMENT_STATUS_CHOICES = [
    (PAYMENT_STATUS_PENDING, 'Pending'),
    (PAYMENT_STATUS_COMPLETE, 'Complete'),
    (PAYMENT_STATUS_FAILED, 'Failed'),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    # protect our data to prevent deletion
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    # prevent negative values
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

class Adress(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
   
    # Creating a foreign key relationship between the Address model and the Customer model.
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    