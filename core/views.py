from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import FileResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .forms import ContactForm, DownloadLeadForm
from .models import (
    Service, Project, TechStackItem, Collaboration, Partner, Testimonial,
    AboutSection, Expertise, TeamMember, SiteSettings,
)


def home(request):
    context = {
        'active_nav': 'home',
        'services': Service.objects.all(),
        'partners': Partner.objects.all(),
        'projects': Project.objects.filter(is_featured=True) or Project.objects.all()[:3],
        'tech_stack_items': TechStackItem.objects.all(),
        'collaborations': Collaboration.objects.all(),
        'testimonials': Testimonial.objects.all(),
    }
    return render(request, 'core/home.html', context)


def about_page(request):
    context = {
        'active_nav': 'about',
        'about': AboutSection.load(),
        'expertises': Expertise.objects.all(),
        'team_members': TeamMember.objects.all(),
    }
    return render(request, 'core/about.html', context)


def services_page(request):
    context = {
        'active_nav': 'services',
        'services': Service.objects.all(),
    }
    return render(request, 'core/services.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    related = Service.objects.exclude(pk=service.pk)[:3]
    context = {
        'active_nav': 'services',
        'service': service,
        'related_services': related,
        'download_form': DownloadLeadForm(),
    }
    return render(request, 'core/service_detail.html', context)


def _notify_admin_of_download(lead):
    """Same pattern as _notify_admin_of_inquiry, for outline PDF downloads."""
    recipient = getattr(settings, 'NOTIFY_EMAIL', None) or SiteSettings.load().contact_email
    if not recipient:
        return
    try:
        service_name = lead.service.title if lead.service else "Unknown Service"
        subject = f"Outline Downloaded — {service_name} — {lead.name}"
        body = (
            f"{lead.name} downloaded the course outline for {service_name}.\n\n"
            f"Name:  {lead.name}\n"
            f"Phone: {lead.phone}\n"
            f"Email: {lead.email}\n"
            f"When:  {lead.created_at}\n"
        )
        send_mail(
            subject=subject,
            message=body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            recipient_list=[recipient],
            fail_silently=True,
        )
    except Exception:
        pass  # never let a notification failure block the visitor's download


def service_download(request, slug):
    """
    Handles the Name/Phone/Email form on the Download modal (service
    detail page). Submits with the form's target pointed at a hidden
    iframe, so the main page never navigates — a successful POST just
    streams the PDF back as the iframe's "page", which the browser
    saves as a download.
    """
    service = get_object_or_404(Service, slug=slug)
    if not service.outline_pdf:
        raise Http404("No outline PDF has been uploaded for this service yet.")

    if request.method != 'POST':
        return redirect('core:service_detail', slug=service.slug)

    form = DownloadLeadForm(request.POST)
    if not form.is_valid():
        # Submitted from a hidden iframe, so there's no page to show
        # this on — keep it simple and just decline the download.
        return HttpResponseBadRequest("Please fill in your name, phone, and email correctly.")

    lead = form.save(commit=False)
    lead.service = service
    lead.save()
    _notify_admin_of_download(lead)

    return FileResponse(
        service.outline_pdf.open('rb'),
        as_attachment=True,
        filename=f"{service.slug}-outline.pdf",
    )


def projects_page(request):
    category = request.GET.get('category', 'all')
    projects = Project.objects.all()
    if category in dict(Project.CATEGORY_CHOICES):
        projects = projects.filter(category=category)

    context = {
        'active_nav': 'projects',
        'projects': projects,
        'category_choices': Project.CATEGORY_CHOICES,
        'active_category': category,
    }
    return render(request, 'core/projects.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related = Project.objects.filter(category=project.category).exclude(pk=project.pk)[:3]
    context = {
        'active_nav': 'projects',
        'project': project,
        'related_projects': related,
    }
    return render(request, 'core/project_detail.html', context)


def tech_stack_page(request):
    context = {
        'active_nav': 'tech-stack',
        'tech_stack_items': TechStackItem.objects.all(),
        'collaborations': Collaboration.objects.all(),
    }
    return render(request, 'core/tech_stack.html', context)


def testimonials_page(request):
    context = {
        'active_nav': 'testimonials',
        'testimonials': Testimonial.objects.all(),
    }
    return render(request, 'core/testimonials.html', context)


def _notify_admin_of_inquiry(inquiry):
    """
    Emails the Tecnsol inbox (SiteSettings.contact_email, or NOTIFY_EMAIL env
    override) with every field the visitor submitted, including which
    service/course they applied for. Never raises — a failed email should
    never block the visitor from seeing their "thank you" message.
    """
    recipient = getattr(settings, 'NOTIFY_EMAIL', None) or SiteSettings.load().contact_email
    if not recipient:
        return
    try:
        service_name = inquiry.service_needed.title if inquiry.service_needed else "General Inquiry / Not Sure Yet"
        subject = f"New Inquiry — {service_name} — {inquiry.name}"
        body = render_to_string('core/emails/new_inquiry.txt', {
            'inquiry': inquiry,
            'service_name': service_name,
        })
        send_mail(
            subject=subject,
            message=body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            recipient_list=[recipient],
            fail_silently=True,
        )
    except Exception:
        pass  # never let a notification failure block the visitor's submission


def contact_page(request):
    """
    Handles the dedicated Contact page, and also receives submissions of
    the contact form embedded in the homepage's contact section — the
    user is redirected back to wherever they submitted from.

    A "More Info" -> "Apply Now" click on a service detail page arrives
    here as /contact/?service=<slug>, which pre-selects that service in
    the dropdown below.
    """
    applied_service = None
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            _notify_admin_of_inquiry(inquiry)
            messages.success(
                request,
                "Inquiry Transmitted — Thank you! The Tecnsol team will reach out shortly."
            )
            redirect_target = request.POST.get('next') or 'core:contact'
            return redirect(redirect_target)
    else:
        initial = {}
        service_slug = request.GET.get('service')
        if service_slug:
            applied_service = Service.objects.filter(slug=service_slug).first()
            if applied_service:
                initial['service_needed'] = applied_service.pk
        form = ContactForm(initial=initial)

    context = {
        'active_nav': 'contact',
        'contact_form': form,
        'applied_service': applied_service,
    }
    return render(request, 'core/contact.html', context)