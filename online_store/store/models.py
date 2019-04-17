from django.db import models
from django.utils import timezone


# Create your models here.
class Product(models.Model):
    ProductID = models.AutoField(primary_key=True, unique=True)
    ProductPrice = models.DecimalField(max_digits=6, decimal_places=2)
    ProductDescription = models.TextField()
    ProductName = models.TextField()

    def __str__(self):
        return self.ProductName


def product_images_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'store/img/products/{0}_{1}'.format(str(instance.ImageProduct.ProductID).zfill(8), filename)


class ProductImage(models.Model):
    ImageProduct = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    Image = models.ImageField(upload_to=product_images_directory_path)


class Transaction(models.Model):
    TransactionID = models.AutoField(primary_key=True, unique=True)
    TransactionDateTime = models.DateTimeField(auto_now_add=True)
    TransactionProducts = models.TextField()
    CustomerEmail = models.TextField()
    CustomerAddress = models.TextField()
    CustomerCity = models.CharField(max_length=50)
    CustomerState = models.CharField(max_length=2)
    CustomerZIP = models.IntegerField()

    def __str__(self):
        return str(self.TransactionDateTime) + " " + str(self.CustomerEmail)


class Coupon(models.Model):
    type_choices = (('P', 'PercentageOff'), ('D', 'DollarsOff'))
    CouponID = models.AutoField(primary_key=True, unique=True)
    CouponName = models.TextField()
    CouponValue = models.IntegerField()
    CouponCode = models.CharField(max_length=5)
    CouponStart = models.DateTimeField()
    CouponEnd = models.DateTimeField()
    CouponType = models.CharField(max_length=1, choices=type_choices)
    ApplicableItems = models.TextField()

    def __str__(self):
        return self.CouponName

    def is_valid(self):
        # TODO fix datetime comparison
        print(self.CouponStart, self.CouponEnd, timezone.now())
        if self.CouponStart < timezone.now() < self.CouponEnd:
            return True
        return False
