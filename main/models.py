from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.urls import reverse
# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=13, blank=True, unique=True, db_index=True, null=True)
    auth_code = models.CharField(max_length=6, blank=True) 

    # def get_absolute_url(self):
    #     print(self)
    #     return reverse("main:account", kwargs={"id": self.id})


    def __str__(self) -> str:
        return f"{self.username}"
    


class Category(models.Model):
    title = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f"{self.title}"


class Tag(models.Model):
    title = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f"{self.title}"
    


class Course(models.Model):
    LANGUAGES = (
        ('uz', 'O\'zbekcha'),
        ('ru', 'Ruscha'),
        ('en', 'Inglizcha'),
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    description = models.TextField()
    duration = models.DurationField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # 100.00
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    created_at = models.DateTimeField(verbose_name="Boshlanish vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilanish vaqti")
    language = models.CharField(max_length=100, blank=True, choices=LANGUAGES)
    rating = models.PositiveBigIntegerField(verbose_name="Rating", default=0)
    image = models.ImageField(upload_to="images", blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="tags", )

    class Meta:
        ordering = ['-rating']




