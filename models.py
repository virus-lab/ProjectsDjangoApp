from django.shortcuts import reverse
from django.db import models
from django.utils import timezone

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
    budget = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project-information', kwargs={'pk': self.pk})


class Task(models.Model):
    priorities = (
        (1, '급함'),
        (2, '보통'),
        (3, '보류'),
    )
    name = models.CharField(max_length=15)
    priority = models.PositiveIntegerField(choices=priorities, default=2)
    cost = models.PositiveIntegerField(default=0)
    receipt = models.ImageField()
