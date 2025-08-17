from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils.text import slugify

#Add a custom manager for myUser
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



#  1. Custom User Model
class myUser(AbstractUser):
    username = None  # Remove default username
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='users/', null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = MyUserManager()  #Add this line

    def __str__(self):
        return self.email

        

#  2. Participant Model
class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    image = models.ImageField(upload_to='participants/', null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.email}'


#  3. Speaker Model
class Speaker(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='speakers/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


#  4. Meetop Model
class Meetop(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='meetops/', null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(Participant, blank=True)
    speakers = models.ManyToManyField(Speaker, blank=True)
    activate = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    meetup_date = models.DateField(null=True, blank=True)
    meetup_time = models.TimeField(null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    # Addslug to meetops
    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
