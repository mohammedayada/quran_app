from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

SEX_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)
EDUCATION_CHOICES = (
    ('educated', 'educated'),
    ('uneducated', 'uneducated'),
    ('student', 'student'),
)
AMOUNT_OF_QURAN_CHOICES = (
    ('complete', 'complete'),
    ('incomplete', 'incomplete'),
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        user = self.create_user(
            email,
            password,
            **extra_fields
        )
        return user


# name , email , password, country, quran, sex, education, religion, hobby, date_of_birth
class User(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    name = models.CharField(max_length=200)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    education = models.CharField(max_length=50, choices=EDUCATION_CHOICES, null=True, blank=True)  # التعليم
    the_outcome_of_forensic_science = models.TextField(null=False, blank=False)  # حصيله العلم الشرعى
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50, null=False, blank=False)
    amount_of_quran = models.CharField(max_length=50, choices=AMOUNT_OF_QURAN_CHOICES, null=True, blank=True)  # مقدار حفظ القرأن
    quran_number = models.IntegerField(default=0, null=True, blank=True)  # عدد اجزاء القران المحفوظه
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, null=True, blank=True)
    hobby = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

    is_superuser = models.BooleanField('is_superuser', default=False)
    is_staff = models.BooleanField('is_staff', default=False)
    is_active = models.BooleanField('is_active', default=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'

    def __str__(self):
        return self.email
