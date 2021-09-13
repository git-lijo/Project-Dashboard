from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User


class Company(models.Model):

    class Meta:
        verbose_name_plural = "companies"

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Tag(models.Model):
    caption = models.CharField(max_length=16)

    def __str__(self):
        return self.caption


class Project(models.Model):

    company = models.ForeignKey(
        'projects.Company', on_delete=models.PROTECT, related_name='projects')

    title = models.CharField('Project title', max_length=128)
    start_date = models.DateField('Project start date', blank=True, null=True)
    end_date = models.DateField('Project end date', blank=True, null=True)

    estimated_design = models.PositiveSmallIntegerField(
        'Estimated design hours')
    actual_design = models.DecimalField(
        'Actual design hours', max_digits=6, decimal_places=2)

    estimated_development = models.PositiveSmallIntegerField(
        'Estimated development hours')
    actual_development = models.DecimalField(
        'Actual development hours', max_digits=6, decimal_places=2)

    estimated_testing = models.PositiveSmallIntegerField(
        'Estimated testing hours')
    actual_testing = models.DecimalField(
        'Actual testing hours', max_digits=6, decimal_places=2)

    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-update', kwargs={'pk': self.pk, 'slug': slugify(self.title)})

    @property
    def has_ended(self):
        return self.end_date is not None and self.end_date < timezone.now().date()

    @property
    def total_estimated_hours(self):
        return self.estimated_design + self.estimated_development + self.estimated_testing

    @property
    def total_actual_hours(self):
        return self.actual_design + self.actual_development + self.actual_testing

    @property
    def is_over_budget(self):
        return self.total_actual_hours > self.total_estimated_hours


class ProjectLogging(models.Model):

    userid = models.ForeignKey(User, on_delete='user')

    initial_value_design = models.DecimalField(
        'Initial design hours', max_digits=6, decimal_places=2)
    latest_value_design = models.DecimalField(
        'New design hours', max_digits=6, decimal_places=2)
    change_delta_design = models.DecimalField(
        'Difference in design hours', max_digits=6, decimal_places=2)

    initial_value_development = models.DecimalField(
        'Initial development hours', max_digits=6, decimal_places=2)
    latest_value_development = models.DecimalField(
        'New development hours', max_digits=6, decimal_places=2)
    change_delta_development = models.DecimalField(
        'Difference in development hours', max_digits=6, decimal_places=2)

    initial_value_testing = models.DecimalField(
        'Initial testing hours', max_digits=6, decimal_places=2)
    latest_value_testing = models.DecimalField(
        'New testing hours', max_digits=6, decimal_places=2)
    change_delta_testing = models.DecimalField(
        'Difference in testing hours', max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.userid)