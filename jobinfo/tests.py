from django.test import TestCase, Client
from jobinfo.models import Season, Year, AppCycle, Position, JobRecruiter, JobSeeker, Company, Application
from django.contrib.auth.models import User, Permission
from django.urls import reverse, resolve
from jobinfo.forms import (JobRecruiterForm, CompanyForm, PositionForm, AppCycleForm, JobSeekerForm, ApplicationForm)
from jobinfo.views import (
    JobRecruiterList, JobRecruiterDetail, JobRecruiterCreate, JobRecruiterUpdate, JobRecruiterDelete,
    CompanyList, CompanyDetail, CompanyCreate, CompanyUpdate, CompanyDelete,
    PositionList, PositionDetail, PositionCreate, PositionUpdate, PositionDelete,
    AppCycleList, AppCycleDetail, AppCycleCreate, AppCycleUpdate, AppCycleDelete,
    JobSeekerList, JobSeekerDetail, JobSeekerCreate, JobSeekerUpdate, JobSeekerDelete,
    ApplicationList, ApplicationDetail, ApplicationCreate, ApplicationUpdate, ApplicationDelete
)


class SeasonModelTest(TestCase):
    def test_create_season(self):
        season = Season.objects.create(season_sequence=1, season_name="Winter")
        self.assertEqual(season.season_sequence, 1)
        self.assertEqual(season.season_name, "Winter")


class YearModelTest(TestCase):
    def test_create_year(self):
        year = Year.objects.create(year=2023)
        self.assertEqual(year.year, 2023)


class AppCycleModelTest(TestCase):
    def setUp(self):
        self.year = Year.objects.create(year=2023)
        self.season = Season.objects.create(season_sequence=1, season_name="Winter")

    def test_create_app_cycle(self):
        app_cycle = AppCycle.objects.create(year=self.year, season=self.season)
        self.assertEqual(app_cycle.year, self.year)
        self.assertEqual(app_cycle.season, self.season)


class PositionModelTest(TestCase):
    def test_create_position(self):
        position = Position.objects.create(position_number="P001", position_name="Software Engineer")
        self.assertEqual(position.position_number, "P001")
        self.assertEqual(position.position_name, "Software Engineer")


class JobRecruiterModelTest(TestCase):
    def test_create_job_recruiter(self):
        job_recruiter = JobRecruiter.objects.create(first_name="John", last_name="Doe")
        self.assertEqual(job_recruiter.first_name, "John")
        self.assertEqual(job_recruiter.last_name, "Doe")


class JobSeekerModelTest(TestCase):
    def test_create_job_seeker(self):
        job_seeker = JobSeeker.objects.create(first_name="Jane", last_name="Doe")
        self.assertEqual(job_seeker.first_name, "Jane")
        self.assertEqual(job_seeker.last_name, "Doe")


class CompanyModelTest(TestCase):
    def setUp(self):
        self.year = Year.objects.create(year=2023)
        self.season = Season.objects.create(season_sequence=1, season_name="Winter")
        self.app_cycle = AppCycle.objects.create(year=self.year, season=self.season)
        self.position = Position.objects.create(position_number="P001", position_name="Software Engineer")
        self.job_recruiter = JobRecruiter.objects.create(first_name="John", last_name="Doe")

    def test_create_company(self):
        company = Company.objects.create(
            company_name="Example Corp",
            appCycle=self.app_cycle,
            position=self.position,
            jobRecruiter=self.job_recruiter
        )
        self.assertEqual(company.company_name, "Example Corp")
        self.assertEqual(company.appCycle, self.app_cycle)
        self.assertEqual(company.position, self.position)
        self.assertEqual(company.jobRecruiter, self.job_recruiter)


class ApplicationModelTest(TestCase):
    def setUp(self):
        self.year = Year.objects.create(year=2023)
        self.season = Season.objects.create(season_sequence=1, season_name="Winter")
        self.app_cycle = AppCycle.objects.create(year=self.year, season=self.season)
        self.position = Position.objects.create(position_number="P001", position_name="Software Engineer")
        self.job_recruiter = JobRecruiter.objects.create(first_name="John", last_name="Doe")
        self.job_seeker = JobSeeker.objects.create(first_name="Jane", last_name="Doe")
        self.company = Company.objects.create(
            company_name="Example Corp",
            appCycle=self.app_cycle,
            position=self.position,
            jobRecruiter=self.job_recruiter
        )

    def test_create_application(self):
        application = Application.objects.create(
            jobSeeker=self.job_seeker,
            company=self.company
        )
        self.assertEqual(application.jobSeeker, self.job_seeker)
        self.assertEqual(application.company, self.company)


class JobRecruiterListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='tester', password='{iSchoolUI}'
        )
        self.user.user_permissions.add(
            *Permission.objects.filter(content_type__app_label='jobinfo', codename__startswith='view_')
        )
        self.job_recruiter = JobRecruiter.objects.create(
            first_name="John",
            disambiguator="1"
        )
        self.url = reverse('jobinfo_jobRecruiter_list_urlpattern')

    def test_job_recruiter_list_view_requires_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/login/?next={self.url}')

    def test_job_recruiter_list_view_displays_job_recruiters(self):
        self.client.login(username='tester', password='{iSchoolUI}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.job_recruiter.first_name)
        self.assertContains(response, self.job_recruiter.disambiguator)

    class JobRecruiterFormTestCase(TestCase):
        def test_valid_data(self):
            form = JobRecruiterForm({
                'first_name': 'John',
                'last_name': 'Doe',
                'disambiguator': '1',
            })
            self.assertTrue(form.is_valid())

        def test_blank_data(self):
            form = JobRecruiterForm({})
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors, {
                'first_name': ['This field is required.'],
                'last_name': ['This field is required.'],
                'disambiguator': ['This field is required.'],
            })

        def test_duplicate_data(self):
            JobRecruiter.objects.create(
                first_name="John",
                last_name="Doe",
                disambiguator="1"
            )
            form = JobRecruiterForm({
                'first_name': 'John',
                'last_name': 'Doe',
                'disambiguator': '1',
            })
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors, {
                '__all__': ['Job Recruiter with this First Name, Last Name, and Disambiguator already exists.']
            })


class URLPatternsTestCase(TestCase):
    def test_url_patterns(self):
        urlpatterns_mapping = [
            ('jobinfo_jobRecruiter_list_urlpattern', JobRecruiterList, 'jobRecruiter/'),
            ('jobinfo_jobRecruiter_detail_urlpattern', JobRecruiterDetail, 'jobRecruiter/<int:pk>/'),
            ('jobinfo_jobRecruiter_create_urlpattern', JobRecruiterCreate, 'jobRecruiter/create/'),
            ('jobinfo_jobRecruiter_update_urlpattern', JobRecruiterUpdate, 'jobRecruiter/<int:pk>/update/'),
            ('jobinfo_jobRecruiter_delete_urlpattern', JobRecruiterDelete, 'jobRecruiter/<int:pk>/delete/'),
            ('jobinfo_company_list_urlpattern', CompanyList, 'company/'),
            ('jobinfo_company_detail_urlpattern', CompanyDetail, 'company/<int:pk>'),
            ('jobinfo_company_create_urlpattern', CompanyCreate, 'company/create/'),
            ('jobinfo_company_update_urlpattern', CompanyUpdate, 'company/<int:pk>/update/'),
            ('jobinfo_company_delete_urlpattern', CompanyDelete, 'company/<int:pk>/delete/'),
            ('jobinfo_position_list_urlpattern', PositionList, 'position/'),
            ('jobinfo_position_detail_urlpattern', PositionDetail, 'position/<int:pk>'),
            ('jobinfo_position_create_urlpattern', PositionCreate, 'position/create/'),
            ('jobinfo_position_update_urlpattern', PositionUpdate, 'position/<int:pk>/update/'),
            ('jobinfo_position_delete_urlpattern', PositionDelete, 'position/<int:pk>/delete/'),
            ('jobinfo_appCycle_list_urlpattern', AppCycleList, 'appCycle/'),
            ('jobinfo_appCycle_detail_urlpattern', AppCycleDetail, 'appCycle/<int:pk>'),
            ('jobinfo_appCycle_create_urlpattern', AppCycleCreate, 'appCycle/create/'),
            ('jobinfo_appCycle_update_urlpattern', AppCycleUpdate, 'appCycle/<int:pk>/update/'),
            ('jobinfo_appCycle_delete_urlpattern', AppCycleDelete, 'appCycle/<int:pk>/delete/'),
            ('jobinfo_jobSeeker_list_urlpattern', JobSeekerList, 'jobSeeker/'),
            ('jobinfo_jobSeeker_detail_urlpattern', JobSeekerDetail, 'jobSeeker/<int:pk>/'),
            ('jobinfo_jobSeeker_create_urlpattern', JobSeekerCreate, 'jobSeeker/create/'),
            ('jobinfo_jobSeeker_update_urlpattern', JobSeekerUpdate, 'jobSeeker/<int:pk>/update/'),
            ('jobinfo_jobSeeker_delete_urlpattern', JobSeekerDelete, 'jobSeeker/<int:pk>/delete/'),
            ('jobinfo_application_list_urlpattern', ApplicationList, 'application/'),
            ('jobinfo_application_detail_urlpattern', ApplicationDetail, 'application/<int:pk>/'),
            ('jobinfo_application_create_urlpattern', ApplicationCreate, 'application/create/'),
            ('jobinfo_application_update_urlpattern', ApplicationUpdate, 'application/<int:pk>/update/'),
            ('jobinfo_application_delete_urlpattern', ApplicationDelete, 'application/<int:pk>/delete/'),
        ]

        for urlpattern_name, view, urlpattern in urlpatterns_mapping:
            url = reverse(urlpattern_name, args=[1]) if '<int:pk>' in urlpattern else reverse(urlpattern_name)
            self.assertEqual(resolve(url).func.view_class, view)

