from datetime import datetime, timedelta

from django.db import models

from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.conf import settings

from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django.urls import reverse
from django.template.defaultfilters import slugify

from helpers.models import TrackingModel

class AccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address!')

        if not username:
            raise ValueError('Users must have a username!')

        user = self.model(
        email = self.normalize_email(email),
        username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, username, password):

        user = self.create_user( 
            email = self.normalize_email(email),
            username = username,
            password = password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using = self._db)
        return user

    def create_bot(self, email, username):
        bot = self.create_user( 
            email = self.normalize_email(email),
            username = username,
            password = 'botpassword',
        )

        bot.is_staff = True

        bot.save(using = self._db)
        return bot



class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    
    username_validator = UnicodeUsernameValidator()
    
    username = models.CharField(
        _('username'),
        max_length=150,
		unique=True,
		help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
		validators=[username_validator],
		error_messages={
			'unique': _("A user with this username already exists."),
		},
    )
    slug = models.SlugField()
    email = models.EmailField(_('email address'), unique=True, 
    error_messages={
        'unique': _("A user with this email already exists."),
        },
	)
    is_staff = models.BooleanField(
		_('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
	)
    is_active = models.BooleanField(
		_('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
		),
	)
    email_verified = models.BooleanField(
		_('email_verified'),
        default=False,
        help_text=_(
            "Designates whether this user's email is verified."
		),
	)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = AccountManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_absolute_url(self):
        return reverse('users:view_profile', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

# try:
#     User.objects.get(email='botty@community.com', username='Community Bot')
# except User.DoesNotExist:
#     User.objects.create_bot(email='botty@community.com', username='Community Bot')





