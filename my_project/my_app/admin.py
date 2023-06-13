import logging
from copy import deepcopy

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import models as djangomodels
from django.utils.html import format_html

from my_project.my_app import models
from my_project.my_app.mappings import *




class PricingPlanForm(forms.ModelForm):
    company = forms.ModelChoiceField(
        queryset=models.Company.objects.all(),
        required=True
    )
    product_name = forms.ChoiceField(choices=PRODUCT_NAMES_DICT.items())
    fee = forms.IntegerField(required=True)
    status = forms.ChoiceField(choices=PRICING_PLAN_STATUSES)
    scope = forms.CharField(max_length=50, required=False)

    def save(self, commit=True):
        if not self.instance.scope:
            # if scope is not filled (vendor form) then prefill it
            product_name = self.cleaned_data.get('product_name').product_name
            if product_name in ['subscription_yavin', 'renting_yavin', 'subscription_other']:
                scope = '1000-01'
            elif product_name in ['commission_proxi', 'commission_vads', 'gateway_proxi', 'gateway_vads']:
                scope = 'all'
            else:
                scope = 'other'
            self.instance.scope = scope
        self.instance.save()

        return super(PricingPlanForm, self).save(commit=commit)

    class Meta:
        model = models.PricingPlan
        exclude = ['scope', 'status']


class PricingPlanAdmin(admin.ModelAdmin):
    form = PricingPlanForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(PricingPlanAdmin, self).get_fieldsets(request, obj)
        fieldsets[0][1]['fields'].remove('scope')
        fieldsets[0][1]['fields'].remove('status')
        if request.user.is_superuser:
            return fieldsets
        fieldsets[0][1]['fields'].remove('company')
        return fieldsets

    def get_list_display(self, request):
        if request.user.is_superuser:
            list_display = ['product_name', 'company', 'fee', 'scope', 'status']
        else:
            list_display = ['product_name', 'fee', 'scope', 'status']
        return list_display

    def save_model(self, request, obj, form, change):
        pass  # this is overridden in the Form

    def get_queryset(self, request):
        qs = super(PricingPlanAdmin, self).get_queryset(request)
        if not request.user.is_superuser and request.user.groups.filter(name='vendor').exists():
            return qs.filter(
                company__reseller=models.Vendor.objects.get(user_profiles=request.user.profile)
            )
        return qs

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(PricingPlanAdmin, self).get_form(request, obj, **kwargs)
        form = deepcopy(form)
        if request.user.groups.filter(name='vendor').exists():
            qs = models.VendorPricingPlan.objects.all()
            qs = qs.filter(vendor=models.Vendor.objects.get(user_profiles=request.user.profile))
            form.base_fields['product_name'] = forms.ModelChoiceField(
                queryset=qs,
                to_field_name='product_name',
                required=True
            )
            for field in ('scope', 'status'):
                form.base_fields[field].widget = forms.HiddenInput()
            form.base_fields['status'].initial = 'open'
        else:
            form.base_fields['product_name'] = forms.ChoiceField(choices=PRODUCT_NAMES)
        return form


class PricingPlanInline(admin.TabularInline):
    model = models.PricingPlan
    form = PricingPlanForm
    extra = 0
    exclude = ('rounding', 'min')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='open')


class CustomModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        """
        Get label from product name mappings
        """
        mapping_dict = dict((key, value) for key, value in PRODUCT_NAMES)
        return mapping_dict[obj.product_name]


class PricingPlanInlineForVendor(PricingPlanInline):

    class Media:
        js = ('js/admin_inline_change.js',)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset = deepcopy(formset)
        formset.form.base_fields['scope'].widget = forms.HiddenInput()
        formset.form.base_fields['status'].widget = forms.HiddenInput()
        formset.form.base_fields['status'].initial = 'open'
        qs = models.VendorPricingPlan.objects.all()
        qs = qs.filter(vendor=models.Vendor.objects.get(user_profiles=request.user.profile))
        formset.form.base_fields['product_name'] = CustomModelChoiceField(
            queryset=qs,
            to_field_name='product_name',
            required=True
        )
        return formset


class CompanyFormForVendor(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=djangomodels.User.objects.order_by('username'),
        widget=FilteredSelectMultiple(verbose_name='Users', is_stacked=False),
    )
    reseller = forms.ModelChoiceField(
        queryset=models.Vendor.objects.all(),
        required=False
    )
    brand_name = forms.CharField()


class CompanyForm(CompanyFormForVendor):
    hidden_field = forms.ChoiceField(choices=PLATFORMS, required=True)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand_name']
    inlines = []

    def get_inline_instances(self, request, obj=None):
        _inlines = super(CompanyAdmin, self).get_inline_instances(request, obj=None)
        if request.user.groups.filter(name='vendor').exists():
            _inlines.append(PricingPlanInlineForVendor(self.model, self.admin_site))
        else:
            _inlines.append(PricingPlanInline(self.model, self.admin_site))
        return _inlines

    def get_fieldsets(self, request, obj=None):
        out_fieldsets = (("Company Details", {"fields": ['users', 'brand_name']}),)
        if request.user.groups.filter(name='vendor').exists():
            return out_fieldsets
        out_fieldsets[0][1]['fields'].append('hidden_field')
        out_fieldsets[0][1]['fields'].append('reseller')
        return out_fieldsets

    def get_form(self, request, obj=None, **kwargs):
        if request.user.groups.filter(name='vendor').exists():
            self.form = CompanyFormForVendor
        else:
            self.form = CompanyForm
        form = super(CompanyAdmin, self).get_form(request, obj, **kwargs)
        if hasattr(request.user, 'profile') \
                and hasattr(request.user.profile, 'vendor') \
                and request.user.profile.vendor is not None:
            qs = djangomodels.User.objects.all()
            qs = qs.filter(  # user.company is owned by vendor
                companyusers__company__in=models.Company.objects.filter(
                    reseller=models.Vendor.objects.get(user_profiles=request.user.profile)
                )
            ) | qs.filter(  # user.userprofile is owned by vendor
                profile__vendor=models.Vendor.objects.get(user_profiles=request.user.profile)
            )
            form.base_fields['users'].queryset = qs
            form.base_fields['reseller'].initial = request.user.profile.vendor

        return form

    def get_queryset(self, request):
        qs = super(CompanyAdmin, self).get_queryset(request)
        if not request.user.is_superuser and request.user.groups.filter(name='vendor').exists():
            return qs.filter(
                reseller=models.Vendor.objects.get(user_profiles=request.user.profile)
            )
        return qs


class VendorPricingPlanAdminForm(forms.ModelForm):
    economic_model = forms.ChoiceField(choices=VENDOR_ECONOMIC_MODELS)
    product_name = forms.ChoiceField(choices=PRODUCT_NAMES)


class VendorPricingPlanInline(admin.TabularInline):
    model = models.VendorPricingPlan
    form = VendorPricingPlanAdminForm
    extra = 0


class VendorForm(forms.ModelForm):
    type = forms.ChoiceField(choices=VENDOR_TYPES)
    economic_model = forms.ChoiceField(choices=VENDOR_ECONOMIC_MODELS)
    invoice_company = forms.ModelChoiceField(
        queryset=models.Company.objects.all(),
        required=False
    )


class VendorAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'economic_model', 'id')
    form = VendorForm
    inlines = [VendorPricingPlanInline, ]


class CompanyUsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'user_email',)

    def company_name(self, obj):
        return obj.company.id

    def user_email(self, obj):
        return obj.user.id

    def get_queryset(self, request):
        qs = super(CompanyUsersAdmin, self).get_queryset(request)
        if not request.user.is_superuser and request.user.groups.filter(name='vendor').exists():
            return qs.filter(
                company__in=models.Company.objects.filter(
                    reseller=models.Vendor.objects.get(user_profiles=request.user.profile)
                )
            )
        return qs


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    user = forms.ModelChoiceField(
        queryset=djangomodels.User.objects.all(),
        required=False
    )
    company = forms.ModelChoiceField(
        queryset=models.Company.objects.all(),
        required=False
    )
    vendor = forms.ModelChoiceField(
        queryset=models.Vendor.objects.all(),
        required=False
    )

    def save(self, commit=True):
        email = self.cleaned_data.get('email', "").lower()

        if self.instance.id:
            # in edit mode
            profile = self.instance
        else:
            # in add mode
            password = "blabla"
            user = djangomodels.User.objects.create_user(email, email, password)
            profile = models.UserProfile.objects.create(user=user)
        profile.vendor = self.cleaned_data['vendor']
        profile.save()
        return super(UserProfileForm, self).save(commit=commit)

    class Meta:
        model = models.UserProfile
        fields = "__all__"


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', ]
    form = UserProfileForm

    def save_model(self, request, obj, form, change):
        pass  # this is overridden in the Form

    def username(self, obj):
        return obj.user.username if obj.user else None

    def get_fieldsets(self, request, obj=None):
        print('X'*99)
        print(obj)
        logging.warning('z'*99)
        logging.warning(obj)
        if obj:
            # obj is not None, so this is a change page
            email_or_user_field = 'user'
        else:
            email_or_user_field = 'email'
        out_fieldsets = [
                ("User", {"fields": [email_or_user_field, 'first_name', 'vendor']}),
            ]
        if not request.user.is_superuser and request.user.groups.filter(name='vendor').exists():
            return out_fieldsets
        else:
            out_fieldsets[0][1]["fields"].append('hidden_fields')
            return out_fieldsets

    def get_form(self, request, obj=None, **kwargs):
        print('Z'*99)
        print(obj)
        form = super(UserProfileAdmin, self).get_form(request, obj, **kwargs)
        form = deepcopy(form)
        if hasattr(request.user, 'profile'):
            if hasattr(request.user.profile, 'vendor'):
                form.base_fields['vendor'].initial = request.user.profile.vendor
        return form

    def get_queryset(self, request):
        print('A'*99)
        qs = super(UserProfileAdmin, self).get_queryset(request)
        if not request.user.is_superuser and request.user.groups.filter(name='vendor').exists():
            qs = qs.filter(user__in=djangomodels.User.objects.filter( # userprofile.company is owned by vendor
                companyusers__company__in=models.Company.objects.filter(
                    reseller=models.Vendor.objects.get(user_profiles=request.user.profile)
                )
            )) | qs.filter( # userprofile is owned by vendor
                vendor=models.Vendor.objects.get(user_profiles=request.user.profile)
            )
        return qs


admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.CompanyUsers, CompanyUsersAdmin)
admin.site.register(models.Vendor, VendorAdmin)
admin.site.register(models.PricingPlan, PricingPlanAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
