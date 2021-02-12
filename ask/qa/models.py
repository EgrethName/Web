import uuid
import datetime
from django.db import models
from django.contrib.auth.hashers import make_password


class SiteUser(models.Model):
    username = models.CharField(unique=True, max_length=15)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)


class Session(models.Model):
    key = models.CharField(unique=True, max_length=50)
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    expires = models.DateTimeField()


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-id')

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    objects = QuestionManager()
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(SiteUser, null=True, on_delete=models.CASCADE)
    likes = models.ManyToManyField(SiteUser, related_name='question_like_user')

    def get_url(self):
        return '/question/%d' % self.pk


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(SiteUser, null=True, on_delete=models.CASCADE)


def do_login(username, password):
    try:
        user = SiteUser.objects.get(username=username)
    except SiteUser.DoesNotExist:
        return
    hashed_pass = make_password(password, salt='1', hasher='md5')
    if user.password != hashed_pass:
        return None
    session = Session()
    session.key = uuid.uuid4().hex
    session.user = user
    session.expires = datetime.datetime.today() + datetime.timedelta(days=30)
    session.save()
    return session.key
