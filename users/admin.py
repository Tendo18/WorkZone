from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, AdminProfile, EmployerProfile, ApplicantProfile

# --- User Admin ---
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'role', 'is_verified', 'is_active', 'created_at']
    list_filter = ['role', 'is_verified', 'is_active', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'phone_number', 'address', 'profile_image')}),
        ('Role & Status', {'fields': ('role', 'is_verified', 'is_active')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'role'),
        }),
    )

# --- Admin Profile Admin ---
@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'employee_id', 'created_at']
    list_filter = ['department', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'employee_id']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User Information', {'fields': ('user',)}),
        ('Admin Details', {'fields': ('department', 'employee_id', 'permissions')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at']

# --- Employer Profile Admin ---
@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'industry', 'is_verified_employer', 'created_at']
    list_filter = ['industry', 'is_verified_employer', 'company_size', 'created_at']
    search_fields = ['user__email', 'company_name', 'industry']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User Information', {'fields': ('user',)}),
        ('Company Information', {'fields': ('company_name', 'company_description', 'company_website', 'company_logo')}),
        ('Company Details', {'fields': ('industry', 'company_size', 'founded_year')}),
        ('Verification', {'fields': ('is_verified_employer',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at']

    def get_company_logo_preview(self, obj):
        if obj.company_logo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.company_logo.url)
        return "No logo"
    get_company_logo_preview.short_description = 'Logo Preview'

# --- Applicant Profile Admin ---
@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'headline', 'experience_years', 'education_level', 'is_available_for_work', 'is_verified_applicant', 'created_at']
    list_filter = ['gender', 'education_level', 'is_available_for_work', 'is_verified_applicant', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'headline']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User Information', {'fields': ('user',)}),
        ('Personal Information', {'fields': ('date_of_birth', 'gender')}),
        ('Professional Information', {'fields': ('headline', 'summary', 'experience_years')}),
        ('Education', {'fields': ('education_level',)}),
        ('Skills & Preferences', {'fields': ('skills', 'preferred_job_types', 'preferred_locations', 'salary_expectation')}),
        ('Social Links', {'fields': ('linkedin_url', 'github_url', 'portfolio_url')}),
        ('Status', {'fields': ('is_available_for_work', 'is_verified_applicant')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at']

    def get_age(self, obj):
        if obj.date_of_birth:
            return obj.age
        return "Not specified"
    get_age.short_description = 'Age'

# --- Admin Site Configuration ---
admin.site.site_header = "WorkZone Administration"
admin.site.site_title = "WorkZone Admin Portal"
admin.site.index_title = "Welcome to WorkZone Administration"