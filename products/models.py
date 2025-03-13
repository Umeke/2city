from django.db import models

class Product(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductPhoto(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    image_url = models.URLField()
    city_id = models.IntegerField(null=True, blank=True, db_index=True)

    def __str__(self):
        return f"{self.product.name} - {self.image_url} (city_id={self.city_id})"
