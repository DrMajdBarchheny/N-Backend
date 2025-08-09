

# Create your models here.
from django.db import models
from parler.models import TranslatableModel, TranslatedFields


from django.contrib.auth.models import User


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255)
    )

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

class Project(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255),
        description=models.TextField()
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/',null=True, blank=True)

    def __str__(self):
        return self.project.safe_translation_getter('title', any_language=True)
   


# B: Rental Catalog

class ProductCategory(TranslatableModel):
    translations=TranslatedFields(
       name = models.CharField(max_length=100) 
    )
    

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)


class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255),
        description=models.TextField(blank=True),
    )
    image = models.ImageField(upload_to='product_images/',null=True, blank=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    availability = models.BooleanField(default=True)
    qty = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.qty <= 0:
            self.availability = False
        else:
            self.availability = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# C: Team, Client, Forms

class TeamMember(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        title=models.CharField(max_length=100),
        bio=models.TextField(),
    )
    photo = models.ImageField(upload_to='team/')

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)


class ClientLogo(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
    )
    logo = models.ImageField(upload_to='clients/')

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)


class DesignRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contact = models.CharField(max_length=100)
    event_type = models.CharField(max_length=100)
    event_date = models.DateField()
    details = models.TextField(blank=True)
    # attachment = models.FileField(upload_to='design_requests/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class SiteSettings(models.Model):
    company_profile_pdf = models.FileField(upload_to='site/')
    whatsapp_number = models.CharField(max_length=20)
    location_url = models.URLField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return "Site Settings"