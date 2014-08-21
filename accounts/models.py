from django.db import models

from django.contrib.auth.models import AbstractBaseUser, AbstractUser, UserManager, PermissionsMixin, BaseUserManager

#from mpv.models import Share
"""
class User(AbstractBaseUser):
    #user = models.ManyToManyField('self', related_name='users', symmetrical=False)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #shares = models.ManyToManyField(Share)

    USERNAME_FIELD = 'email'
    #objects = CustomUserManager()

    def __str__(self):
        return self.email

    objects = UserManager()

    @classmethod
    def get_by_id(cls, uid):
        return User.objects.get(pk=uid)


    @classmethod
    def create(cls, name, email, password):
        new_user = cls(name=name, email=email)
        new_user.set_password(password)
        new_user.save()
        return new_user
    """


#https://docs.djangoproject.com/en/1.5/topics/auth/customizing/
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyUserManager.normalize_email(email),

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):

    ## Put AbstractBaseUser
    #username = models.CharField(max_length=255, unique=True)
    #user = models.ManyToManyField('self', related_name='users', symmetrical=False)
    email = models.CharField(max_length=255, unique=True)
    #user = models.ManyToManyField('self', related_name='users', symmetrical=False)
    name = models.CharField(max_length=255, default="user")
    #shares = models.ManyToManyField(Share)

    USERNAME_FIELD = 'email'

    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @classmethod
    def get_by_id(cls, uid):
        return User.objects.get(pk=uid)

    @classmethod
    def create(cls, name, email, password):
        new_user = cls(name=name, email=email)
        new_user.set_password(password)
        new_user.save()
        return new_user

    #https://docs.djangoproject.com/en/1.5/topics/auth/customizing/
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    """
    @classmethod
    def create_superuser(self, email, password):

        #Creates and saves a superuser with the given email, date of
        #birth and password.

        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
    """

    objects = MyUserManager()