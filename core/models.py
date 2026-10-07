from django.db import models
from django.utils.text import slugify


class SiteSettings(models.Model):
    """
    Singleton-style model holding editable hero copy, stats and contact
    details so the whole landing page stays editable from the admin panel.
    """
    hero_badge_text = models.CharField(
        max_length=120, default="Architecting Next-Gen Web Solutions")
    hero_heading_line1 = models.CharField(max_length=150, default="We Engineer")
    hero_heading_highlight = models.CharField(max_length=150, default="Digital Brilliance")
    hero_heading_line2 = models.CharField(max_length=150, default="With Code")
    hero_subtitle = models.TextField(
        default=("Tecnsol empowers brands with hyper-scalable web architectures, "
                  "bespoke frontend design engineering, and modern digital "
                  "ecosystems optimized for unmatched speed and performance."))

    stat_projects_delivered = models.PositiveIntegerField(default=180)
    stat_satisfied_clients_pct = models.DecimalField(max_digits=5, decimal_places=1, default=99)
    stat_code_commits_k = models.PositiveIntegerField(default=240)
    stat_uptime_pct = models.DecimalField(max_digits=5, decimal_places=1, default=99.9)

    contact_email = models.EmailField(default="contact@tecnsol.io")
    contact_phone = models.CharField(max_length=50, default="+1 (800) 832-6765")
    contact_location = models.CharField(max_length=150, default="Silicon Valley & Global Remote")
    contact_intro = models.TextField(
        default=("Ready to elevate your web presence or launch a high-performance "
                  "web application? Fill out the project inquiry form, and our "
                  "tech lead will respond within 12 hours."))

    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    discord_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    map_embed_url = models.URLField(
        blank=True,
        help_text=("Optional. Paste a Google Maps embed URL (Maps → Share → "
                    "Embed a map → copy the src=\"...\" link) to pin an exact "
                    "location on the Contact page. Leave blank to auto-generate "
                    "a map from the Location field above."))

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        # Force this to always be a single row (pk=1).
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # prevent accidental deletion of the singleton row

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def map_src(self):
        """Returns a usable Google Maps embed src, falling back to a plain
        location search if no explicit embed URL was set in the admin."""
        if self.map_embed_url:
            return self.map_embed_url
        from urllib.parse import quote
        query = quote(self.contact_location or "Tecnsol")
        return f"https://www.google.com/maps?q={query}&output=embed"


class Service(models.Model):
    icon_class = models.CharField(
        max_length=60, default="fa-solid fa-code",
        help_text="Font Awesome icon class, e.g. fa-solid fa-code")
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField()
    tags = models.CharField(
        max_length=255, blank=True,
        help_text="Comma separated, e.g. ReactJS, TailwindCSS, TypeScript")
    image = models.ImageField(
        upload_to='services/', blank=True, null=True,
        help_text=("Optional. Shown as the banner image on this service's detail "
                    "page. Leave blank to show an animated icon placeholder instead."))
    fee = models.CharField(
        max_length=60, blank=True,
        help_text="Shown on the service detail page, e.g. $499, $299/mo, Free Consultation")
    duration = models.CharField(
        max_length=60, blank=True,
        help_text="Shown on the service detail page, e.g. 4 Weeks, 2 Months, Ongoing")
    detail_description = models.TextField(
        blank=True,
        help_text=("Optional. Longer write-up shown only on the service's detail page. "
                    "Leave blank to reuse the short description above."))
    outline_pdf = models.FileField(
        upload_to='service_outlines/', blank=True, null=True,
        help_text=("Optional. Upload a course outline PDF here to show a Download button "
                    "on this service's page. Visitors fill Name/Phone/Email before it downloads. "
                    "Leave blank to hide the Download button."))
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Service.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def full_description(self):
        return self.detail_description or self.description


class Project(models.Model):
    CATEGORY_WEB = 'web_development'
    CATEGORY_GRAPHICS = 'graphics'
    CATEGORY_CHOICES = [
        (CATEGORY_WEB, 'Web Development'),
        (CATEGORY_GRAPHICS, 'Graphics Design'),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default=CATEGORY_WEB)
    tagline = models.CharField(
        max_length=120, blank=True,
        help_text="Small badge label shown on the image, e.g. FinTech SaaS")
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    tags = models.CharField(
        max_length=255, blank=True,
        help_text="Comma separated, e.g. React, Tailwind, ChartJS")
    live_url = models.URLField(blank=True)
    is_featured = models.BooleanField(
        default=False, help_text="Show this project in the homepage carousel")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]


class TechStackItem(models.Model):
    name = models.CharField(max_length=80)
    icon_class = models.CharField(
        max_length=60, help_text="Font Awesome icon class, e.g. fa-brands fa-react")
    icon_color = models.CharField(
        max_length=40, default="text-maroon-glow",
        help_text="Tailwind text color utility class, e.g. text-cyan-400")
    category_label = models.CharField(
        max_length=60, help_text="Small label under the name, e.g. Frontend, Database")
    website_url = models.URLField(
        blank=True,
        help_text="Optional. If set, clicking this tech card opens this link in a new tab.")
    icon_image_url = models.URLField(
        blank=True,
        help_text=("Optional. Direct image/SVG URL for the logo — use this when Font "
                    "Awesome has no icon for the tool (e.g. Adobe apps). Overrides the "
                    "Font Awesome icon class above when set."))
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Tech Stack Item"

    def __str__(self):
        return self.name


class Collaboration(models.Model):
    """
    Institute photos shown in the animated gallery/testimonial slider
    (e.g. campus, labs, classrooms, partner institutes) — each can carry
    an optional short quote so the same item powers both the image
    slider and the quote underneath it.
    """
    name = models.CharField(
        max_length=120,
        help_text="e.g. Main Campus, Computer Lab, Punjab Institute of Technology")
    logo = models.ImageField(
        upload_to='collaborations/',
        help_text="The institute/campus photo shown in the slider.")
    quote = models.TextField(
        blank=True, default='',
        help_text="Optional short testimonial/quote shown under this photo in the slider.")
    quote_author = models.CharField(
        max_length=120, blank=True, default='',
        help_text="Optional. Who said the quote, e.g. 'Dr. Ahmed, Director'. Leave blank to just show the Name above as the caption.")
    website_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Institute Photo / Quote"
        verbose_name_plural = "Institute Photos / Quotes"

    def __str__(self):
        return self.name


class Partner(models.Model):
    """
    Company/brand logos shown in the "Trusted By" marquee section above
    the Projects section on the homepage — separate from the Institute
    Photos/Quotes slider above.
    """
    name = models.CharField(max_length=120)
    logo = models.ImageField(
        upload_to='partners/',
        help_text="The partner/brand logo — works best as a transparent PNG.")
    website_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Partner Logo"
        verbose_name_plural = "Partner Logos"

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=150, help_text="e.g. CTO, Nexus Technologies")
    avatar = models.ImageField(upload_to='testimonials/')
    review = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

    def star_range(self):
        return range(self.rating)


class ContactMessage(models.Model):
    BUDGET_CHOICES = [
        ('2500-5000', '$2,500 - $5,000'),
        ('5000-10000', '$5,000 - $10,000'),
        ('10000+', '$10,000+'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    service_needed = models.ForeignKey(
        Service, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='applications',
        help_text=("Which service/course this inquiry is about. Auto-filled when "
                    "someone clicks \"Apply Now\" on a service's detail page."))
    budget = models.CharField(max_length=30, choices=BUDGET_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"

    def __str__(self):
        return f"{self.name} <{self.email}>"


class DownloadLead(models.Model):
    """
    Captured every time a visitor fills the Name/Phone/Email form to
    download a service's course outline PDF (the "Download" button on
    the service detail page).
    """
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='downloads',
        help_text="Which service/course outline this person downloaded.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Outline Download Lead"

    def __str__(self):
        return f"{self.name} <{self.email}>"


class AboutSection(models.Model):
    """
    Singleton-style model powering the homepage "About Us" section:
    eyebrow/heading copy, the section image, and a short intro paragraph.
    Expertise items and team members below are managed as separate lists.
    """
    eyebrow_text = models.CharField(max_length=120, default="Who We Are")
    heading_line1 = models.CharField(max_length=150, default="Engineering Minds Behind")
    heading_highlight = models.CharField(max_length=150, default="Tecnsol")
    description = models.TextField(
        default=("We're a tight-knit collective of engineers, designers and "
                  "strategists obsessed with building fast, beautiful, "
                  "future-proof digital products. Every pixel and every "
                  "line of code is written with intent."))
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    years_experience = models.PositiveIntegerField(default=8)
    team_members_count = models.PositiveIntegerField(default=12)

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return "About Section"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Expertise(models.Model):
    """A single expertise/skill highlighted in the About Us section."""
    icon_class = models.CharField(
        max_length=60, default="fa-solid fa-code",
        help_text="Font Awesome icon class, e.g. fa-solid fa-code")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    proficiency_pct = models.PositiveSmallIntegerField(
        default=90, help_text="0-100, drives the animated skill bar")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name_plural = "Expertise"

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    """A team member shown in the About Us section."""
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, help_text="e.g. Lead Frontend Engineer")
    photo = models.ImageField(upload_to='team/')
    bio = models.CharField(max_length=200, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True, help_text="Personal website / portfolio link")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name