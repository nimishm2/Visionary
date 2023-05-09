from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from jobinfo.forms import JobRecruiterForm, CompanyForm, JobSeekerForm, PositionForm, AppCycleForm, ApplicationForm
from jobinfo.models import (
    JobRecruiter,
    Company, JobSeeker, Position, AppCycle, Application,
)
from jobinfo.utils import ObjectCreateMixin, PageLinksMixin


class JobRecruiterList(LoginRequiredMixin, PermissionRequiredMixin, View):
    page_kwarg = 'page'
    paginate_by = 25
    permission_required = 'jobinfo.view_jobrecruiter'
    template_name = 'jobinfo/jobRecruiter_list.html'

    def get(self, request):
        jobRecruiters = JobRecruiter.objects.all()
        paginator = Paginator(
            jobRecruiters,
            self.paginate_by
        )
        page_number = request.GET.get(
            self.page_kwarg
        )
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(
                paginator.num_pages)
        if page.has_previous():
            prev_url = "?{pkw}={n}".format(
                pkw=self.page_kwarg,
                n=page.previous_page_number())
        else:
            prev_url = None
        if page.has_next():
            next_url = "?{pkw}={n}".format(
                pkw=self.page_kwarg,
                n=page.next_page_number())
        else:
            next_url = None
        context = {
            'is_paginated':
                page.has_other_pages(),
            'next_page_url': next_url,
            'paginator': paginator,
            'previous_page_url': prev_url,
            'jobRecruiter_list': page,
        }
        return render(
            request, self.template_name, context)


class JobRecruiterDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'jobinfo.view_jobrecruiter'
    def get(self, request, pk):
        jobRecruiter = get_object_or_404(JobRecruiter, pk=pk)
        company_list = jobRecruiter.companies.all()
        return render(request,
                      'jobinfo/jobRecruiter_detail.html',
                      {'jobRecruiter': jobRecruiter, 'company_list': company_list}
                      )


class JobRecruiterUpdate(LoginRequiredMixin, PermissionRequiredMixin, View):
    form_class = JobRecruiterForm
    model = JobRecruiter
    template_name = 'jobinfo/jobRecruiter_form_update.html'
    permission_required = 'jobinfo.change_jobrecruiter'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        jobRecruiter = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=jobRecruiter),
            'jobRecruiter': jobRecruiter,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        jobRecruiter = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=jobRecruiter)
        if bound_form.is_valid():
            new_jobRecruiter = bound_form.save()
            return redirect(new_jobRecruiter)
        else:
            context = {
                'form': bound_form,
                'jobRecruiter': jobRecruiter,
            }
            return render(
                request,
                self.template_name,
                context)


class JobRecruiterDelete(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'jobinfo.delete_jobrecruiter'
    def get(self, request, pk):
        jobRecruiter = self.get_object(pk)
        companies = jobRecruiter.companies.all()
        if companies.count() > 0:
            return render(
                request,
                'jobinfo/jobRecruiter_refuse_delete.html',
                {'jobRecruiter': jobRecruiter,
                 'companies': companies,
                 }
            )
        else:
            return render(
                request,
                'jobinfo/jobRecruiter_confirm_delete.html',
                {'jobRecruiter': jobRecruiter}
            )

    def get_object(self, pk):
        return get_object_or_404(
            JobRecruiter,
            pk=pk)

    def post(self, request, pk):
        jobRecruiter = self.get_object(pk)
        jobRecruiter.delete()
        return redirect('jobinfo_jobRecruiter_list_urlpattern')


class JobRecruiterCreate(LoginRequiredMixin, PermissionRequiredMixin, ObjectCreateMixin, View):
    form_class = JobRecruiterForm
    template_name = 'jobinfo/jobRecruiter_form.html'
    permission_required = 'jobinfo.add_jobrecruiter'


class CompanyList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Company
    permission_required = 'jobinfo.view_company'


class CompanyDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Company
    permission_required = 'jobinfo.view_company'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        company = self.get_object()
        appCycle = company.appCycle
        position = company.position
        jobRecruiter = company.jobRecruiter
        application_list = company.applications.all()
        context['appCycle'] = appCycle
        context['position'] = position
        context['jobRecruiter'] = jobRecruiter
        context['application_list'] = application_list
        return context


class CompanyCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = CompanyForm
    model = Company
    permission_required = 'jobinfo.add_company'


class CompanyUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = CompanyForm
    model = Company
    template_name = 'jobinfo/company_form_update.html'
    permission_required = 'jobinfo.change_company'


class CompanyDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Company
    success_url = reverse_lazy('jobinfo_company_list_urlpattern')
    permission_required = 'jobinfo.delete_company'


class JobSeekerList(LoginRequiredMixin, PermissionRequiredMixin, View):
    page_kwarg = 'page'
    paginate_by = 25
    template_name = 'jobinfo/jobSeeker_list.html'
    permission_required = 'jobinfo.view_jobseeker'

    def get(self, request):
        jobSeekers = JobSeeker.objects.all()
        paginator = Paginator(
            jobSeekers,
            self.paginate_by
        )
        page_number = request.GET.get(
            self.page_kwarg
        )
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(
                paginator.num_pages)
        if page.has_previous():
            prev_url = "?{pkw}={n}".format(
                pkw=self.page_kwarg,
                n=page.previous_page_number())
        else:
            prev_url = None
        if page.has_next():
            next_url = "?{pkw}={n}".format(
                pkw=self.page_kwarg,
                n=page.next_page_number())
        else:
            next_url = None
        context = {
            'is_paginated':
                page.has_other_pages(),
            'next_page_url': next_url,
            'paginator': paginator,
            'previous_page_url': prev_url,
            'jobSeeker_list': page,
        }
        return render(
            request, self.template_name, context)


class JobSeekerDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'jobinfo.view_jobseeker'
    def get(self, request, pk):
        jobSeeker = get_object_or_404(JobSeeker, pk=pk)
        application_list = jobSeeker.applications.all()
        return render(request,
                      'jobinfo/jobSeeker_detail.html',
                      {'jobSeeker': jobSeeker, 'application_list': application_list}
                      )


class JobSeekerCreate(LoginRequiredMixin, PermissionRequiredMixin, ObjectCreateMixin, View):
    form_class = JobSeekerForm
    template_name = 'jobinfo/jobSeeker_form.html'
    permission_required = 'jobinfo.add_jobseeker'


class JobSeekerUpdate(LoginRequiredMixin, PermissionRequiredMixin, View):
    form_class = JobSeekerForm
    model = JobSeeker
    template_name = 'jobinfo/jobSeeker_form_update.html'
    permission_required = 'jobinfo.change_jobseeker'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        jobSeeker = self.get_object(pk)
        context = {
            'form': self.form_class(instance=jobSeeker),
            'jobSeeker': jobSeeker,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        jobSeeker = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=jobSeeker)
        if bound_form.is_valid():
            new_jobSeeker = bound_form.save()
            return redirect(new_jobSeeker)
        else:
            context = {
                'form': bound_form,
                'jobSeeker': jobSeeker,
            }
            return render(
                request,
                self.template_name,
                context)


class JobSeekerDelete(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'jobinfo.delete_jobseeker'
    def get(self, request, pk):
        jobSeeker = self.get_object(pk)
        applications = jobSeeker.applications.all()
        if applications.count() > 0:
            return render(
                request,
                'jobinfo/jobSeeker_refuse_delete.html',
                {'jobSeeker': jobSeeker,
                 'applications': applications,
                 }
            )
        else:
            return render(
                request,
                'jobinfo/jobSeeker_confirm_delete.html',
                {'jobSeeker': jobSeeker}
            )

    def get_object(self, pk):
        return get_object_or_404(
            JobSeeker,
            pk=pk)

    def post(self, request, pk):
        jobSeeker = self.get_object(pk)
        jobSeeker.delete()
        return redirect('jobinfo_jobSeeker_list_urlpattern')


class PositionList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Position
    permission_required = 'jobinfo.view_position'


class PositionDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Position
    permission_required = 'jobinfo.view_position'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        position = self.get_object()
        company_list = position.companies.all()
        context['company_list'] = company_list
        return context


class PositionCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PositionForm
    model = Position
    permission_required = 'jobinfo.add_position'


class PositionUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PositionForm
    model = Position
    template_name = 'jobinfo/position_form_update.html'
    permission_required = 'jobinfo.change_position'


class PositionDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Position
    success_url = reverse_lazy('jobinfo_position_list_urlpattern')
    permission_required = 'jobinfo.delete_position'


class AppCycleList(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'jobinfo.view_appcycle'
    def get(self, request):
        return render(request,
                      'jobinfo/appCycle_list.html',
                      {'appCycle_list': AppCycle.objects.all()}
                      )


class AppCycleDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'jobinfo.view_appcycle'
    def get(self, request, pk):
        appCycle = get_object_or_404(AppCycle, pk=pk)
        company_list = appCycle.companies.all()
        return render(request, 'jobinfo/appCycle_detail.html', {'appCycle': appCycle, 'company_list': company_list})


class AppCycleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = AppCycleForm
    model = AppCycle
    template_name = 'jobinfo/appCycle_form_update.html'
    permission_required = 'jobinfo.change_appcycle'


class AppCycleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = AppCycle
    success_url = reverse_lazy('jobinfo_appCycle_list_urlpattern')
    permission_required = 'jobinfo.delete_appcycle'


class AppCycleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = AppCycleForm
    model = AppCycle
    permission_required = 'jobinfo.add_appcycle'


class ApplicationList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Application
    permission_required = 'jobinfo.view_application'


class ApplicationDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Application
    permission_required = 'jobinfo.view_application'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        application = self.get_object()
        jobSeeker = application.jobSeeker
        company = application.company
        context['jobSeeker'] = jobSeeker
        context['company'] = company
        return context


class ApplicationCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = ApplicationForm
    model = Application
    permission_required = 'jobinfo.add_application'


class ApplicationUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = ApplicationForm
    model = Application
    template_name = 'jobinfo/application_form_update.html'
    permission_required = 'jobinfo.change_application'


class ApplicationDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Application
    success_url = reverse_lazy('jobinfo_application_list_urlpattern')
    permission_required = 'jobinfo.delete_application'
