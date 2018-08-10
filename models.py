import string

from django.db import models
from django.shortcuts import reverse
from django.utils import timezone

from random import choice

# Create your models here.


class Information(models.Model):
    secure_levels = (
        (1, '모두 공개'),
        (2, '팀원 공개'),
        (3, '비공개'),
    )
    name = models.CharField(
        max_length=30,
        verbose_name='프로젝트 이름',
        unique=True,
    )
    project_manager = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='project_manager',
        verbose_name='총괄 디렉터',
    )
    directors = models.ManyToManyField(
        'auth.User',
        blank=True,
        related_name='project_directors',
        verbose_name='팀원',
    )
    description = models.TextField(
        blank=True,
        verbose_name='프로젝트 설명',
    )
    secure_level = models.PositiveIntegerField(
        choices=secure_levels,
        verbose_name='참여 가능 범위',
    )
    published_date = models.DateField(editable=False)
    budget = models.PositiveIntegerField(default=0, verbose_name='예산')
    tasks = models.ManyToManyField(
        'projects.Task',
        verbose_name='업무 리스트',
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project-information', kwargs={'pk': self.pk})


class Task(models.Model):

    def custom_path(instance, filename):
        arr = [choice(string.ascii_letters) for _ in range(8)]
        pid = ''.join(arr)
        extension = filename.split('.')[-1]
        date = timezone.now()
        return 'files/%s/%s/%s/%s.%s' % (
            date.year,
            date.month,
            date.day,
            pid,
            extension,
        )

    priorities = (
        (1, '급함'),
        (2, '보통'),
        (3, '보류'),
    )
    published_director = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='published_director', verbose_name='작성한 디렉터')
    description = models.CharField(max_length=15, verbose_name='내용')
    granted_to = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='granted_to', verbose_name='담당 디렉터')
    priority = models.PositiveIntegerField(choices=priorities, default=2, verbose_name='우선순위')
    cost = models.PositiveIntegerField(default=0, verbose_name='비용')
    receipt = models.ImageField(upload_to=custom_path, blank=True, verbose_name='영수증')
    deadline = models.DateTimeField(verbose_name='데드라인')
    published_date = models.DateTimeField(default=timezone.now, editable=False, verbose_name='등록날짜')

    def __str__(self):
        return self.description


class Notice(models.Model):
    title = models.CharField(max_length=15)
    content = models.CharField(max_length=100)
    alarm_to = models.ManyToManyField('projects.AlarmCheck')
    registered_date = models.DateTimeField(auto_now=True)


class AlarmCheck(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)
