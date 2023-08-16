from django.db import models
from User.models import User

LOST_CHOICES = (
    ('Y', 'YES'),
    ('N', 'NO'),
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

SIZE_CHOICES =(
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large')
)


class Pet_info(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    register_number = models.CharField(max_length=100, unique=True, primary_key=True)  # 예시: 100 글자로 지정
    register_date = models.DateField(null=True, auto_now_add=True)
    pet_date = models.TextField(null=True)
    pet_name = models.TextField(null=True)
    pet_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    pet_image = models.ImageField(upload_to='pet_images/', null=True)  # 이미지를 저장할 필드
    pet_breed = models.TextField(null=True)
    pet_lost = models.CharField(max_length=1, choices=LOST_CHOICES, default="N")
    pet_size = models.CharField(max_length=1, choices=SIZE_CHOICES, default="S")

    class Meta:
        db_table = 'PET_INFO'


class Report_info(models.Model):
    report_number = models.CharField(max_length=100, null=False, primary_key=True)
    report_date = models.DateField(auto_now_add=True)
    pet_image = models.TextField()
    location = models.TextField()
    lat_lon = models.TextField()
    etc = models.TextField()

    class Meta:
        db_table = "REPORT_INFO"
