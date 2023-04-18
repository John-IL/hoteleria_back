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
    module = models.ForeignKey(Modules, on_delete=models.CASCADE, verbose_name='module relation')
    section = models.ForeignKey(Sections, on_delete=models.CASCADE, verbose_name='section relation')
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
    created_at = models.DateTimeField(auto_now_add=True)

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
    personal_enum = (
    (1,'ADMINISTRADOR'),
    (2,'CHEF'),
    (3,'SEGURIDAD'),
    (4,'RECEPCIONISTA'),
    (5,'LIMPIEZA'),
    )
      
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    country = models.ForeignKey(StaticCountries, on_delete=models.CASCADE, verbose_name='country relation')
    phone = models.CharField(max_length=45)
    email = models.CharField(max_length=45, blank=False, unique=True)
    document_type = models.ForeignKey(StaticDocumentTypes, on_delete=models.CASCADE, verbose_name='document type relation')
    document_number = models.CharField(max_length=30, blank=False)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, verbose_name='role relation')
    personal_type = models.IntegerField(choices=personal_enum)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = UserProfileManager()

    REQUIRED_FIELDS = ['first_name','last_name','country','phone','document_type',
                       'document_number','role','password']
    
    USERNAME_FIELD = 'email'
    
class UserSections(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='user relation')
    module_section = models.ForeignKey(ModuleSections, on_delete=models.CASCADE, verbose_name='module')
    created_at = models.DateTimeField(auto_now_add=True)

class PaymentMethods(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class RoomCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    image = models.TextField()
    description = models.TextField()
    high_america = models.DecimalField(max_digits=10 ,decimal_places=2)
    low_america = models.DecimalField(max_digits=10 ,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class RoomCategoryDetail(models.Model):
    room_category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, verbose_name="room categoy relation")
    description = models.TextField()
    icon = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
class Promotion(models.Model):
    name = models.CharField(max_length=250)
    image = models.TextField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Floor(models.Model):
    number = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Room(models.Model):
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, verbose_name="room category relation")
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, verbose_name="promotion relation")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name="floor relation")
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=200)
    guest_number = models.IntegerField()
    number = models.IntegerField()
    description = models.TextField()
    has_bed = models.BooleanField(default=False)
    has_tv = models.BooleanField(default=False)
    has_hot_water = models.BooleanField(default=False)
    has_jacuzzi = models.BooleanField(default=False)
    has_private_bathroom = models.BooleanField(default=False)
    has_couch = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.SmallIntegerField() ## add choice field
    created_at = models.DateTimeField(auto_now_add=True)

class RoomImages(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="room relation")
    image = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Reserve(models.Model):
    reserve_date = models.DateField()
    observation = models.TextField()
    client =  models.ForeignKey(Clients, on_delete=models.CASCADE, verbose_name="client relation")
    payment_method = models.ForeignKey(PaymentMethods, on_delete=models.CASCADE, verbose_name="payment method relation")
    personal = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="personal relation")
    created_at = models.DateTimeField(auto_now_add=True)

class ReserveDateDetail(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    reserve = models.ForeignKey(Reserve, on_delete=models.CASCADE, verbose_name="reserve date relation")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="room detail relation")

class Testimonials(models.Model):
    reserve = models.ForeignKey(Reserve, on_delete=models.CASCADE, verbose_name="reserve relation")
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, verbose_name="client relation")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="room relation")
    desription = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Banners(models.Model):
    image = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)