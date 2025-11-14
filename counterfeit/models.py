from django.db import models
from django.core.validators import MinLengthValidator

class Product(models.Model):
    """Model to store authentic product information"""
    name = models.CharField(max_length=200, help_text="Product name")
    product_id = models.CharField(
        max_length=100, 
        unique=True, 
        validators=[MinLengthValidator(3)],
        help_text="Unique product identification code"
    )
    description = models.TextField(help_text="Product description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def __str__(self):
        return f"{self.name} ({self.product_id})"
