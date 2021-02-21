import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from os.path import splitext
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Username must be provided')

        if not password:
            raise ValueError('Password must be provided')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(username, password, **extra_fields)


class QuestionManager(models.Manager):
    def new(self):
      return self.order_by('-id')

    def popular(self):
      return self.order_by('-rating')


class AnswerManager(models.Manager):
    def new(self):
      return self.order_by('-id')

    def popular(self):
      return self.order_by('-rating')


class UUIDFileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        _, ext = splitext(name)
        return uuid.uuid4().hex + ext


class User(AbstractBaseUser, PermissionsMixin):

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    objects = UserAccountManager()

    username = models.CharField('username', unique=True, blank=False, null=False, max_length=255)
    email = models.EmailField('email', null=True)
    first_name = models.CharField('first name', blank=True, null=True, max_length=400)
    second_name = models.CharField('second name', blank=True, null=True, max_length=400)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    is_verified = models.BooleanField('verified', default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)
    userpic = models.ImageField(upload_to=settings.USERPICS_DIR,
                                storage=UUIDFileStorage(location=settings.MEDIA_ROOT + '/' + settings.USERPICS_DIR,
                                                        base_url=settings.MEDIA_URL + '/' + settings.USERPICS_DIR),
                                default=settings.NO_PIC_USER_PATH)

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.second_name}'

    def __unicode__(self):
        return self.username


class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='question_like_user')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Вопрос {self.title} от {self.author}'


class Answer(models.Model):
    objects = AnswerManager()
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='answer_like_user')

    def __str__(self):
        return f'Ответ {self.author} на {self.question}'
