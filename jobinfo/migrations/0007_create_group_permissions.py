from __future__ import unicode_literals
from itertools import chain

from django.db import migrations


def populate_permissions_lists(apps):
    permission_class = apps.get_model('auth', 'Permission')

    jobrecruiter_permissions = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                               content_type__model='jobrecruiter')

    jobseeker_permissions = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                            content_type__model='jobseeker')

    season_permissions = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                         content_type__model='season')

    year_permissions = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                       content_type__model='year')

    appcycle_permissions = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                           content_type__model='appcycle')

    position_permissions = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                           content_type__model='position')

    company_permissions = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                          content_type__model='company')

    application_permissions = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                              content_type__model='application')

    perm_view_jobrecruiter = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                             content_type__model='jobrecruiter',
                                                             codename='view_jobrecruiter')

    perm_view_jobseeker = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                          content_type__model='jobseeker',
                                                          codename='view_jobseeker')

    perm_view_season = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                       content_type__model='season',
                                                       codename='view_season')

    perm_view_year = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                     content_type__model='year',
                                                     codename='view_year')

    perm_view_appcycle = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                         content_type__model='appcycle',
                                                         codename='view_appcycle')

    perm_view_position = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                         content_type__model='position',
                                                         codename='view_position')

    perm_view_company = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                        content_type__model='company',
                                                        codename='view_company')

    perm_view_application = permission_class.objects.filter(content_type__app_label='jobinfo',
                                                            content_type__model='application',
                                                            codename='view_application')

    ji_user_permissions = chain(perm_view_jobrecruiter,
                                perm_view_season,
                                perm_view_year,
                                perm_view_jobseeker,
                                perm_view_appcycle,
                                perm_view_position,
                                perm_view_company,
                                perm_view_application)

    ji_schedulingExec_permissions = chain(jobrecruiter_permissions,
                                          season_permissions,
                                          year_permissions,
                                          appcycle_permissions,
                                          position_permissions,
                                          company_permissions,
                                          perm_view_jobseeker,
                                          perm_view_application)

    ji_applicationManager_permissions = chain(jobseeker_permissions,
                                              application_permissions,
                                              perm_view_jobrecruiter,
                                              perm_view_season,
                                              perm_view_year,
                                              perm_view_position,
                                              perm_view_appcycle,
                                              perm_view_company)

    my_groups_initialization_list = [
        {
            "name": "ji_user",
            "permissions_list": ji_user_permissions,
        },
        {
            "name": "ji_schedulingExec",
            "permissions_list": ji_schedulingExec_permissions,
        },
        {
            "name": "ji_applicationManager",
            "permissions_list": ji_applicationManager_permissions,
        },
    ]
    return my_groups_initialization_list


def add_group_permissions_data(apps, schema_editor):
    groups_initialization_list = populate_permissions_lists(apps)

    group_model_class = apps.get_model('auth', 'Group')
    for group in groups_initialization_list:
        if group['permissions_list'] is not None:
            group_object = group_model_class.objects.get(
                name=group['name']
            )
            group_object.permissions.set(group['permissions_list'])
            group_object.save()


def remove_group_permissions_data(apps, schema_editor):
    groups_initialization_list = populate_permissions_lists(apps)

    group_model_class = apps.get_model('auth', 'Group')
    for group in groups_initialization_list:
        if group['permissions_list'] is not None:
            group_object = group_model_class.objects.get(
                name=group['name']
            )
            list_of_permissions = group['permissions_list']
            for permission in list_of_permissions:
                group_object.permissions.remove(permission)
                group_object.save()


class Migration(migrations.Migration):
    dependencies = [
        ('jobinfo', '0006_create_groups'),
    ]

    operations = [
        migrations.RunPython(
            add_group_permissions_data,
            remove_group_permissions_data
        )
    ]

