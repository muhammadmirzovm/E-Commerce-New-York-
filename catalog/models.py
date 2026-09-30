from django.db import models
from django.utils.text import slugify
from django.conf import settings
class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    parent = models.ForeignKey("self",on_delete=models.SET_NULL,null=True,blank=True,related_name="children")
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
            if self.parent:
                return f"{self.parent.name} → {self.name}"
            return self.name
    def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.name)
            super().save(*args, **kwargs)


class Product(models.Model):
    seller = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE,
       related_name="products"
    )
    category = models.ForeignKey(
       Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)

    price = models.DecimalField(max_digits=12, decimal_places=2) 
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField()

    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True) 

    main_image = models.ImageField(upload_to="products/main/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class Review(models.Model):
    product = models.ForeignKey(  # qaysi productga yozildi
        Product,  # agar shu fayl ichida Product bo'lsa Product deb yozsa ham bo'ladi
        on_delete=models.CASCADE,
        related_name="reviews")
    user = models.ForeignKey(  # kim yozdi
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews")
    rating = models.PositiveSmallIntegerField(default=5)  # 1-5 oralig'ida bo'ladi
    comment = models.TextField(blank=True)  # izoh ixtiyoriy
    created_at = models.DateTimeField(auto_now_add=True)  # yozilgan vaqt
    class Meta:
        constraints = [
            models.UniqueConstraint(  # bir user bir productga faqat 1 marta yozsin
                fields=["product", "user"],
                name="unique_review_per_user_product"
            )
        ]
    def __str__(self):
        return f"{self.product.name} - {self.user.username} ({self.rating})"

