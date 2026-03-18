from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class Student(models.Model):
    full_name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=50)
    id_type = models.CharField(max_length=10) # PASSPORT or MYKAD or MYKID
    dob = models.DateField(max_length=12, default="") # YYYY-MM-DD
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, default="")
    address_line1 = models.CharField(max_length=200, default="")
    address_line2 = models.CharField(max_length=200, default="")
    postcode = models.CharField(max_length=10, default="")
    city = models.CharField(max_length=20, default="")
    state = models.CharField(max_length=20, default="")
    country = models.CharField(max_length=20, default="")
    previous_school = models.CharField(max_length=200, default="")
    student_type = models.CharField(max_length=50, default="")
    total_siblings = models.IntegerField(default=0)
    number_of_children = models.IntegerField(default=0)
    parent_name = models.CharField(max_length=200, default="")
    parent_contact = models.CharField(max_length=50, default="") # 012-3456789
    created_date = models.DateTimeField("date created") # YYYY-MM-DD HH:mm:ss

    def __str__(self):
        return self.full_name + " (" + str(self.age) + "yrs" + ")"


class Bill(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    bill_type = models.CharField(max_length=100) # REGISTRATION_FEE or MONTHLY 
    description = models.CharField(max_length=200, default="") # Anything
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    designated_month = models.CharField(max_length=10) # JANUARY, FEBRUARY and etc
    designated_year = models.CharField(max_length=10) # 2020, 2021, 2022 and etc
    payment_method = models.CharField(max_length=100) # QR or FPX or CASH or DEBIT
    payment_status = models.CharField(max_length=10) # PAID or PENDING or FAILED
    payment_date = models.DateTimeField("date created", null=True, blank=True) # YYYY-MM-DD HH:mm:ss

    def __str__(self):
        return self.student.full_name + "|" + self.bill_type + "|" + str(self.bill_amount)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Notice: No username argument here!
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Link the custom manager
    objects = UserManager() 