from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
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
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Sections(models.Model):
    name = models.CharField(max_length=50, unique=True)
    route = models.CharField(max_length=50)
    is_new = models.BooleanField(default=True)
    icon = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
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

class UserProfileManager(BaseUserManager):
    ''' Funciones para manegar los usuarios'''

    def create_user(self, first_name, last_name, country, phone, email, document_type,document_number,role, password=None):
        ''' crear nuevo usuario '''
        if not email:
            raise ValueError('El usuario debe tener un email')

        country_id = StaticCountries.objects.get(id=country)
        document = StaticDocumentTypes.objects.get(id=document_type)
        role_id = Roles.objects.get(id=role)

        user = self.model(first_name=first_name, last_name=last_name, country=country_id, 
                          phone=phone, email=email, document_type=document,document_number=document_number,
                          role=role_id)
        user.set_password(password)
        user.is_superuser = False ## eliminar en produccion
        user.is_staff = False ## eliminar en produccion
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, country, phone, email, document_type,document_number,role, password):

        if password is None:
            raise ValueError('El usuario necesita una contraseña')

        user = self.create_user(first_name, last_name, country, 
                          phone, email, document_type,document_number,
                          role, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    country = models.ForeignKey(StaticCountries, on_delete=models.CASCADE, verbose_name='country relation')
    phone = models.CharField(max_length=45)
    email = models.CharField(max_length=45, blank=False, unique=True)
    document_type = models.ForeignKey(StaticDocumentTypes, on_delete=models.CASCADE, verbose_name='document type relation')
    document_number = models.CharField(max_length=30, blank=False)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, verbose_name='role relation')
    personal = models.ForeignKey(Personals, blank=True, null=True, on_delete=models.CASCADE, verbose_name='personal relation')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserProfileManager()

    REQUIRED_FIELDS = ['first_name','role']
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        '''obtener nombre completo'''
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.first_name
    

class UserSections(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='user relation')
    module_section_id = models.ForeignKey(ModuleSections, on_delete=models.CASCADE, verbose_name='module')
    created_at = models.DateTimeField(auto_now_add=True)