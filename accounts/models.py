from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    user.save(using=self._db)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"
        PARENT = "PARENT","Parent"

    base_type = Types.STUDENT

    _type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','_type']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self._type = self.base_type
        return super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return "/users/%i/" % (self.pk)

# class StudentManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         return super().get_queryset(*args, **kwargs).filter(_type=User.Types.STUDENT)

# class StudentProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="StudentProfile")#related_name is used to call object
#     roll = models.IntegerField()
#     _class = models.IntegerField()
#     parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="Parent")
#     address = models.CharField( max_length=200, null=True, blank=True)
#     discount = models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.user.first_name}'s Profile"

# class Student(User):
#     base_type = User.Types.STUDENT
#     objects = StudentManager()

#     class Meta:
#         proxy = True

#     @property
#     def more(self):
#         return self.StudentProfile
