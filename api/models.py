from django.db import models

# Create your models here.

class Roles(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Modules(models.Model):
    name = models.CharField(max_length=50, unique=True)
    route = models.CharField(max_length=50, unique=True)
    initial = models.CharField(max_length=50, blank=True)
    icons = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Sections(models.Model):
    name = models.CharField(max_length=50, unique=True)
    route = models.CharField(max_length=50)
    is_new = models.BooleanField(default=True)
    icon = models.CharField(max_length=50)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class ModuleSections(models.Model):
    module_id = models.ForeignKey(Modules, on_delete=models.CASCADE, verbose_name='module relation')
    section_id = models.ForeignKey(Sections, on_delete=models.CASCADE, verbose_name='section relation')
    created_at = models.DateTimeField(auto_now_add=True)

class StaticDocumentTypes(models.Model):
    name = models.CharField(max_length=50, unique=True)
    sunat_code = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class StaticCountries(models.Model):
    name = models.CharField(max_length=50, unique=True)
    iso = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

class Clients(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    country = models.ForeignKey(StaticCountries, on_delete=models.CASCADE, verbose_name='country relation')
    phone = models.CharField(max_length=45)
    email = models.CharField(max_length=45, blank=False)
    document_type = models.ForeignKey(StaticDocumentTypes, on_delete=models.CASCADE, verbose_name='document type relation')
    document_number = models.CharField(max_length=30, blank=False)

class PersonalType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Personals(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    country = models.ForeignKey(StaticCountries, on_delete=models.CASCADE, verbose_name='country relation')
    phone = models.CharField(max_length=45)
    email = models.CharField(max_length=45, blank=False)
    document_type = models.ForeignKey(StaticDocumentTypes, on_delete=models.CASCADE, verbose_name='document type relation')
    document_number = models.CharField(max_length=30, blank=False)
    type = models.ForeignKey(PersonalType, on_delete=models.CASCADE, verbose_name='personal type relation')