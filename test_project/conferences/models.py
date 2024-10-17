from django.db import models
from categories.models import Category
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class Conference(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateField(default=timezone.now().date)
    end_date = models.DateField(default=timezone.now().date)
    location = models.CharField(max_length=255)
    price = models.FloatField()
    capacity = models.IntegerField(validators=[MaxValueValidator(limit_value=900, message="Capacity must be less than 900")])
    program = models.FileField(upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg'], message="Only pdf, png, jpeg, jpg allowed")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="conferences")

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError('End date must be after start date.')

    class Meta:
        verbose_name_plural = 'conferences'
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__gte=timezone.now().date()),
                name="start_date_must_be_greater_than_today"
            )
        ]
    def __str__(self):
        return f"title conference {self.title} location {self.location} "
