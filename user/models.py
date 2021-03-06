from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField("사용자 아이디", max_length=12, unique=True)
    email = models.EmailField("이메일", max_length=100)
    password = models.CharField("비밀번호", max_length=128)
    fullname = models.CharField('이름', max_length=20)
    join_date = models.DateTimeField('생성시각', auto_now_add=True)
    
    def __str__(self):
        return self.username

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    list_display = ('id', 'username')

class Hobby(models.Model):
    hobby = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.hobby}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    intro = models.TextField()
    age = models.IntegerField()
    hobby = models.ManyToManyField(Hobby)

    def __str__(self):
        return f"{self.user.username}'s profile"
