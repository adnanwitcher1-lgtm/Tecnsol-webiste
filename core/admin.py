from django.contrib import admin
from django.utils.html import format_html

from .models import (
    SiteSettings, Service, Project, TechStackItem,
    Collaboration, Partner, Testimonial, ContactMessage, DownloadLead,
    AboutSection, Expertise, TeamMember,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Hero Section", {
            'fields': (
                'hero_badge_text', 'hero_heading_line1', 'hero_heading_highlight',
                'hero_heading_line2', 'hero_subtitle',
            )
        }),
        ("Hero Stats", {
            'fields': (
                'stat_projects_delivered', 'stat_satisfied_clients_pct',
                'stat_code_commits_k', 'stat_uptime_pct',
            )
        }),
        ("Contact Details", {
            'fields': ('contact_email', 'contact_phone', 'contact_location',
                       'contact_intro', 'map_embed_url')
        }),
        ("Social Links", {
            'fields': ('github_url', 'linkedin_url', 'twitter_url', 'discord_url',
                       'facebook_url', 'instagram_url', 'youtube_url')
        }),
    )

    def has_add_permission(self, request):
        # Only one SiteSettings row should ever exist.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumb', 'fee', 'duration', 'icon_class', 'tags', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'icon_class', 'image', 'order')
        }),
        ("Card & Detail Page Content", {
            'fields': ('description', 'detail_description', 'tags')
        }),
        ("Apply Now Details", {
            'fields': ('fee', 'duration'),
            'description': "Shown on this service's detail page (More Info), above the Apply Now button."
        }),
        ("Download Button (optional)", {
            'fields': ('outline_pdf',),
            'description': ("Upload a course outline PDF to show a Download button next to Apply Now. "
                             "Visitors fill Name/Phone/Email before it downloads — see Outline Download Leads below."),
        }),
    )

    @admin.display(description="Image")
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.image.url)
        return "—"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'tagline', 'thumb', 'is_featured', 'order', 'created_at')
    list_editable = ('is_featured', 'order')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description', 'tags', 'tagline')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', '-created_at')

    @admin.display(description="Preview")
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.image.url)
        return "—"


@admin.register(TechStackItem)
class TechStackItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_label', 'icon_class', 'icon_image_url', 'website_url', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'category_label')
    ordering = ('order',)


@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('name', 'thumb', 'quote_author', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'quote', 'quote_author')
    ordering = ('order',)
    fieldsets = (
        (None, {
            'fields': ('name', 'logo', 'order')
        }),
        ("Testimonial Slider (optional)", {
            'fields': ('quote', 'quote_author'),
            'description': "Fill these in to show a quote under this photo in the slider. Leave blank to show just the photo and Name."
        }),
        ("Link (optional)", {
            'fields': ('website_url',)
        }),
    )

    @admin.display(description="Photo")
    def thumb(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:36px;border-radius:6px;background:#111;padding:4px;" />',
                obj.logo.url)
        return "—"


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'thumb', 'website_url', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    ordering = ('order',)

    @admin.display(description="Logo")
    def thumb(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:32px;border-radius:6px;background:#111;padding:4px;" />',
                obj.logo.url)
        return "—"

    
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'thumb', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'role', 'review')
    ordering = ('order',)

    @admin.display(description="Avatar")
    def thumb(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="height:36px;width:36px;border-radius:50%;object-fit:cover;" />',
                obj.avatar.url)
        return "—"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service_needed', 'budget', 'is_read', 'created_at')
    list_editable = ('is_read',)
    list_filter = ('service_needed', 'budget', 'is_read')
    search_fields = ('name', 'email', 'message', 'service_needed__title')
    readonly_fields = ('name', 'email', 'service_needed', 'budget', 'message', 'created_at')
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False


@admin.register(DownloadLead)
class DownloadLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'service', 'created_at')
    list_filter = ('service',)
    search_fields = ('name', 'email', 'phone', 'service__title')
    readonly_fields = ('name', 'phone', 'email', 'service', 'created_at')
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Copy", {
            'fields': ('eyebrow_text', 'heading_line1', 'heading_highlight', 'description')
        }),
        ("Image & Stats", {
            'fields': ('image', 'years_experience', 'team_members_count')
        }),
    )

    def has_add_permission(self, request):
        return not AboutSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_class', 'proficiency_pct', 'order')
    list_editable = ('order', 'proficiency_pct')
    search_fields = ('title', 'description')
    ordering = ('order',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'thumb', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'role')
    ordering = ('order',)

    @admin.display(description="Photo")
    def thumb(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;border-radius:50%;object-fit:cover;" />',
                obj.photo.url)
        return "—"


admin.site.site_header = "Tecnsol Admin"
admin.site.site_title = "Tecnsol Admin Portal"
admin.site.index_title = "Manage Website Content"
