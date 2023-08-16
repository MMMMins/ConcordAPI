from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER_CHOICES = (
    (0, 'Female'),
    (1, 'Male'),
    (2, 'Not to disclose')
)


class UserManager(BaseUserManager):
    def create_user(self, user_id, name, gender, phone, password=None, **extra_fields):
        if not user_id:
            raise ValueError('The ID must be set')

        user = self.model(
            user_id=user_id,
            username=name,
            gender=gender,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id,  password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(user_id, 'admin', 2, None, password, **extra_fields)


class User(AbstractUser):
    user_id = models.CharField(max_length=100, primary_key=True, unique=True)
    username = models.CharField(max_length=30)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=2)
    phone = models.TextField(null=True)


    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "USER_INFO"


class Schedule(models.Model):
    no = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    diary_date = models.TextField(null=True)
    etc = models.TextField()
    image_pass = models.TextField(null=True)

    class Meta:
        db_table = "SCHEDULE"