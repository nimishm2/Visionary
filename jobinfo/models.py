from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse


class Season(models.Model):
    season_id = models.AutoField(primary_key=True)
    season_sequence = models.IntegerField(unique=True)
    season_name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return '%s' % self.season_name

    class Meta:
        ordering = ['season_sequence']


class Year(models.Model):
    year_id = models.AutoField(primary_key=True)
    year = models.IntegerField(unique=True)

    def __str__(self):
        return '%s' % self.year

    class Meta:
        ordering = ['year']


class AppCycle(models.Model):
    appCycle_id = models.AutoField(primary_key=True)
    year = models.ForeignKey(Year, related_name='appCycles', on_delete=models.PROTECT)
    season = models.ForeignKey(Season, related_name='appCycles', on_delete=models.PROTECT)

    def __str__(self):
        return '%s - %s' % (self.year.year, self.season.season_name)

    def get_absolute_url(self):
        return reverse('jobinfo_appCycle_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('jobinfo_appCycle_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('jobinfo_appCycle_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    class Meta:
        ordering = ['year__year', 'season__season_sequence']
        constraints = [
            UniqueConstraint(fields=['year', 'season'], name='unique_appCycle')
        ]


class Position(models.Model):
    position_id = models.AutoField(primary_key=True)
    position_number = models.CharField(max_length=20)
    position_name = models.CharField(max_length=255)

    def __str__(self):
        return '%s - %s' % (self.position_number, self.position_name)

    def get_absolute_url(self):
        return reverse('jobinfo_position_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('jobinfo_position_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('jobinfo_position_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    class Meta:
        ordering = ['position_number', 'position_name']
        constraints = [
            UniqueConstraint(fields=['position_number', 'position_name'], name='unique_position')
        ]


class JobRecruiter(models.Model):
    jobRecruiter_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    disambiguator = models.CharField(max_length=45, blank=True, default='')

    def __str__(self):
        result = ''
        if self.disambiguator == '':
            result = '%s, %s' % (self.last_name, self.first_name)
        else:
            result = '%s, %s (%s)' % (self.last_name, self.first_name, self.disambiguator)
        return result

    def get_absolute_url(self):
        return reverse('jobinfo_jobRecruiter_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )
    def get_update_url(self):
        return reverse('jobinfo_jobRecruiter_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('jobinfo_jobRecruiter_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    class Meta:
        ordering = ['last_name', 'first_name', 'disambiguator']
        constraints = [
            UniqueConstraint(fields=['last_name', 'first_name', 'disambiguator'], name='unique_jobRecruiter')
        ]


class JobSeeker(models.Model):
    jobSeeker_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    disambiguator = models.CharField(max_length=45, blank=True, default='')

    def __str__(self):
        result = ''
        if self.disambiguator == '':
            result = '%s, %s' % (self.last_name, self.first_name)
        else:
            result = '%s, %s (%s)' % (self.last_name, self.first_name, self.disambiguator)
        return result

    def get_absolute_url(self):
        return reverse('jobinfo_jobSeeker_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('jobinfo_jobSeeker_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('jobinfo_jobSeeker_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    class Meta:
        ordering = ['last_name', 'first_name', 'disambiguator']
        constraints = [
            UniqueConstraint(fields=['last_name', 'first_name', 'disambiguator'], name='unique_jobSeeker')
        ]


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    appCycle = models.ForeignKey(AppCycle, related_name='companies', on_delete=models.PROTECT)
    position = models.ForeignKey(Position, related_name='companies', on_delete=models.PROTECT)
    jobRecruiter = models.ForeignKey(JobRecruiter, related_name='companies', on_delete=models.PROTECT)

    def __str__(self):
        return '%s - %s (%s)' % (self.position.position_number, self.company_name, self.appCycle.__str__())

    def get_absolute_url(self):
        return reverse('jobinfo_company_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('jobinfo_company_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('jobinfo_company_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    class Meta:
        ordering = ['position', 'company_name', 'appCycle']
        constraints = [
            UniqueConstraint(fields=['appCycle', 'position', 'company_name'], name='unique_company')
        ]


class Application(models.Model):
    application_id = models.AutoField(primary_key=True)
    jobSeeker = models.ForeignKey(JobSeeker, related_name='applications', on_delete=models.PROTECT)
    company = models.ForeignKey(Company, related_name='applications', on_delete=models.PROTECT)

    def __str__(self):
        return '%s / %s' % (self.company, self.jobSeeker)

    def get_absolute_url(self):
        return reverse('jobinfo_application_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('jobinfo_application_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('jobinfo_application_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    class Meta:
        ordering = ['company', 'jobSeeker']
        constraints = [
            UniqueConstraint(fields=['company', 'jobSeeker'], name='unique_application')
        ]
