import os

from django.core.validators import FileExtensionValidator
from django.db import models


# Create your models here.
class Thursday(models.Model):
    date = models.DateField()
    assigned_company = models.ForeignKey('thursdays.Company', on_delete=models.SET_NULL, null=True, blank=True)
    scheduled = models.BooleanField(default=False)
    is_currently_available = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Pizza My Mind Dates"
        ordering = ['date', ]

    def __str__(self):
        return 'PMM on ' + str(self.date)


def company_directory_path(instance, filename):
    """
    :param instance:
    :param filename:
    :return:
    """
    return instance.name + '/' + filename


class Company(models.Model):
    # helpful links for images/files:
    # https://docs.djangoproject.com/en/2.0/topics/files/
    # https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.FileField
    # https://docs.djangoproject.com/en/2.0/topics/http/file-uploads/
    name = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    email_one = models.EmailField()
    email_two = models.EmailField(null=True, blank=True)

   # logo = models.ImageField(upload_to=company_directory_path, null=True, blank=True)
    ppt = models.FileField(upload_to=company_directory_path, null=True, blank=True,
                           validators=[FileExtensionValidator(allowed_extensions=['ppt', 'pptx'])])

    pmm_date = models.ForeignKey(Thursday, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'
