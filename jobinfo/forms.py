from django import forms

from jobinfo.models import JobRecruiter, Company, Position, AppCycle, JobSeeker, Application


class JobRecruiterForm(forms.ModelForm):
    class Meta:
        model = JobRecruiter
        fields = '__all__'

    def clean_first_name(self):
        return self.cleaned_data['first_name'].strip()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].strip()

    def clean_disambiguator(self):
        if len(self.cleaned_data['disambiguator']) == 0:
            result = self.cleaned_data['disambiguator']
        else:
            result = self.cleaned_data['disambiguator'].strip()
        return result


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def clean_company_name(self):
        return self.cleaned_data['company_name'].strip()


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'

    def clean_position_number(self):
        return self.cleaned_data['position_number'].strip()

    def clean_position_name(self):
        return self.cleaned_data['position_name'].strip()


class AppCycleForm(forms.ModelForm):
    class Meta:
        model = AppCycle
        fields = '__all__'


class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = '__all__'

    def clean_first_name(self):
        return self.cleaned_data['first_name'].strip()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].strip()

    def clean_disambiguator(self):
        if len(self.cleaned_data['disambiguator']) == 0:
            result = self.cleaned_data['disambiguator']
        else:
            result = self.cleaned_data['disambiguator'].strip()
        return result


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'
