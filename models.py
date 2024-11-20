from django.db import models
from .constants import PaymentStatus
# Create your models here.

class categories(models.Model):
	name = models.CharField(max_length=30)
	status = models.BooleanField(default=True)
	def __str__(self):
		return self.name

class products(models.Model):
	pname = models.CharField(max_length=100)
	pprice = models.CharField(max_length=100)
	sdescrip = models.TextField()
	ldescrip = models.TextField()
	product_category = models.ForeignKey(categories,on_delete = models.CASCADE)
	quantity = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.slug

class product_image(models.Model):
	single_product=models.ForeignKey(products,on_delete=models.CASCADE)
	image=models.ImageField(upload_to='product_image/',null=True)
	active=models.BooleanField(default=True)

	def __str__(self):
		return self.single_product.pname

class data(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	contact = models.IntegerField(primary_key=True)
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=20)

class Order(models.Model):
    name = models.CharField(("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(("Amount"), null=False, blank=False)
    status = models.CharField(
        ("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        ("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        ("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        ("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"
        
    def mark_as_paid(self):
        self.status = PaymentStatus.SUCCESS
        self.save()