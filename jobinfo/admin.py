from django.contrib import admin

from .models import Year, AppCycle, Season, Company, Position, JobRecruiter, JobSeeker, Application

admin.site.register(Year)
admin.site.register(AppCycle)
admin.site.register(Season)
admin.site.register(Company)
admin.site.register(Position)
admin.site.register(JobRecruiter)
admin.site.register(JobSeeker)
admin.site.register(Application)
