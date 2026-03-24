from django.db import models

# Create your models here
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField()
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    original_price = models.IntegerField()
    price = models.IntegerField()
    published_date = models.DateField()
    language = models.CharField(max_length=50)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.title} wriiten by {self.author}"

