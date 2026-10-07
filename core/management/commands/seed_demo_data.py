"""
Seeds the database with the same demo content that used to be hardcoded
in the original single-file HTML page, so the site looks complete the
moment you run it. Everything it creates can be edited, replaced or
deleted from the Django admin panel afterwards.

Usage:
    python manage.py seed_demo_data
"""
import io
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import (
    SiteSettings, Service, Project, TechStackItem, Collaboration, Testimonial,
    AboutSection, Expertise, TeamMember,
)

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def make_placeholder_image(text, size=(800, 500), bg=(17, 17, 24), fg=(255, 42, 95)):
    """Generates a simple placeholder PNG (as bytes) with centered text."""
    if not PIL_AVAILABLE:
        return None
    img = Image.new('RGB', size, color=bg)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default(size=36)
    except TypeError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rectangle(
        [(20, 20), (size[0] - 20, size[1] - 20)], outline=fg, width=3)
    draw.text(((size[0] - w) / 2, (size[1] - h) / 2), text, fill=fg, font=font)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


class Command(BaseCommand):
    help = "Seed the database with demo Services, Projects, Tech Stack, Collaborations and Testimonials."

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', action='store_true',
            help="Delete existing demo-seedable content before re-seeding.")

    @transaction.atomic
    def handle(self, *args, **options):
        if options['flush']:
            Service.objects.all().delete()
            Project.objects.all().delete()
            TechStackItem.objects.all().delete()
            Collaboration.objects.all().delete()
            Testimonial.objects.all().delete()
            Expertise.objects.all().delete()
            TeamMember.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared existing demo content."))

        SiteSettings.load()

        # ---- Services ----
        services = [
            dict(icon_class="fa-solid fa-code", title="Custom Frontend Engineering",
                 description="Ultra-responsive, pixel-perfect user interfaces built with React, Next.js, and modern CSS frameworks tailored for optimal conversion and lightning speed.",
                 tags="ReactJS, TailwindCSS, TypeScript", fee="$499", duration="3 Weeks"),
            dict(icon_class="fa-solid fa-cubes-stacked", title="Full-Stack Architecture",
                 description="Scalable microservices, RESTful & GraphQL APIs, database architecture with Node.js, Python/Django, and cloud deployment pipelines.",
                 tags="NodeJS, Python, PostgreSQL", fee="$999", duration="6 Weeks"),
            dict(icon_class="fa-solid fa-wand-magic-sparkles", title="Interactive UI/UX & Motion",
                 description="Immersive 3D interactive canvases, micro-animations with Three.js/GSAP, dark-mode designs, and modern user experience journeys.",
                 tags="Three.js, GSAP, Figma", fee="$699", duration="4 Weeks"),
            dict(icon_class="fa-solid fa-gauge-high", title="Speed & SEO Optimization",
                 description="Deep Lighthouse audit fixes, asset compression, code splitting, edge caching, and semantic structured data for search engine rankings.",
                 tags="Core Web Vitals, SEO", fee="$299", duration="2 Weeks"),
            dict(icon_class="fa-solid fa-cart-shopping", title="E-Commerce Platforms",
                 description="Custom high-conversion storefronts, seamless payment gateway integrations (Stripe, PayPal), headless commerce, and cart management.",
                 tags="Shopify, Stripe API", fee="$1,299", duration="8 Weeks"),
            dict(icon_class="fa-solid fa-shield-halved", title="Maintenance & Security",
                 description="Continuous vulnerability patching, 24/7 uptime monitoring, automated CI/CD deployment automation, and dedicated system support.",
                 tags="DevOps, CI/CD", fee="$199/mo", duration="Ongoing"),
        ]
        for i, data in enumerate(services):
            Service.objects.update_or_create(title=data['title'], defaults={**data, 'order': i})
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(services)} services."))

        # ---- Projects ----
        projects = [
            dict(title="Aetheris - AI Analytics Suite", category=Project.CATEGORY_WEB,
                 tagline="FinTech SaaS",
                 description="Next-generation real-time financial tracking platform featuring WebGL data visualizations, instant automated reports, and dark UI system architecture.",
                 tags="React, Tailwind, ChartJS", is_featured=True),
            dict(title="Vortex Cyber Guard", category=Project.CATEGORY_WEB,
                 tagline="Cyber Security",
                 description="High-security web application with live threat monitoring, encrypted data streams, custom alert systems, and automated firewall configs.",
                 tags="Vue.js, Django, WebSockets", is_featured=True),
            dict(title="Orbit Commerce Engine", category=Project.CATEGORY_WEB,
                 tagline="E-Commerce",
                 description="Headless commerce platform with custom checkout flows, Stripe integration, and a Django-powered inventory/admin backend.",
                 tags="Django, React, Stripe API", is_featured=True),
            dict(title="Nebula Brand Identity", category=Project.CATEGORY_GRAPHICS,
                 tagline="Brand Design",
                 description="Full brand identity system including logo suite, color palette, typography guide, and social media templates for a tech startup.",
                 tags="Illustrator, Branding", is_featured=False),
            dict(title="Pulse App Icon Set", category=Project.CATEGORY_GRAPHICS,
                 tagline="UI Illustration",
                 description="A cohesive set of app icons and onboarding illustrations designed for a fintech mobile application launch.",
                 tags="Figma, Illustration", is_featured=False),
            dict(title="Horizon Pitch Deck", category=Project.CATEGORY_GRAPHICS,
                 tagline="Marketing Design",
                 description="Investor pitch deck design with custom data visualizations, iconography, and a dark, premium visual language.",
                 tags="Photoshop, Figma", is_featured=False),
        ]
        for i, data in enumerate(projects):
            obj, _ = Project.objects.update_or_create(
                title=data['title'], defaults={**data, 'order': i})
            if not obj.image:
                img_bytes = make_placeholder_image(data['title'])
                if img_bytes:
                    obj.image.save(f"{obj.slug}.png", ContentFile(img_bytes), save=True)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(projects)} projects."))

        # ---- Tech Stack ----
        tech_items = [
            dict(name="React.js", icon_class="fa-brands fa-react", icon_color="text-cyan-400", category_label="Frontend",
                 website_url="https://react.dev"),
            dict(name="JavaScript ES6+", icon_class="fa-brands fa-js", icon_color="text-yellow-400", category_label="Core Engine",
                 website_url="https://developer.mozilla.org/en-US/docs/Web/JavaScript"),
            dict(name="Python", icon_class="fa-brands fa-python", icon_color="text-blue-400", category_label="Backend & AI",
                 website_url="https://www.python.org"),
            dict(name="Django", icon_class="fa-solid fa-fire", icon_color="text-green-600", category_label="Backend Framework",
                 website_url="https://www.djangoproject.com"),
            dict(name="HTML5 / Web APIs", icon_class="fa-brands fa-html5", icon_color="text-orange-500", category_label="Semantics",
                 website_url="https://developer.mozilla.org/en-US/docs/Web/HTML"),
            dict(name="Tailwind CSS", icon_class="fa-brands fa-css3-alt", icon_color="text-blue-500", category_label="Styling",
                 website_url="https://tailwindcss.com"),
            dict(name="Node.js", icon_class="fa-brands fa-node-js", icon_color="text-green-500", category_label="Runtime",
                 website_url="https://nodejs.org"),
            dict(name="PostgreSQL", icon_class="fa-solid fa-database", icon_color="text-indigo-400", category_label="Database",
                 website_url="https://www.postgresql.org"),
            dict(name="Git / GitHub", icon_class="fa-brands fa-git-alt", icon_color="text-orange-600", category_label="Version Control",
                 website_url="https://github.com"),
            dict(name="Docker", icon_class="fa-brands fa-docker", icon_color="text-sky-400", category_label="Containers",
                 website_url="https://www.docker.com"),
            dict(name="Three.js", icon_class="fa-solid fa-cube", icon_color="text-maroon-glow", category_label="3D WebGL",
                 website_url="https://threejs.org"),
            dict(name="REST & GraphQL", icon_class="fa-solid fa-server", icon_color="text-purple-400", category_label="API Services",
                 website_url="https://graphql.org"),
            dict(name="Figma", icon_class="fa-brands fa-figma", icon_color="text-pink-400", category_label="UI/UX Prototypes",
                 website_url="https://www.figma.com"),
            dict(name="Adobe XD", icon_class="fa-brands fa-adobe", icon_color="text-[#FF61F6]", category_label="UI/UX Prototypes",
                 website_url="https://www.adobe.com/products/xd.html",
                 icon_image_url="https://cdn.simpleicons.org/adobexd/FF61F6"),
            dict(name="Adobe Illustrator", icon_class="fa-brands fa-adobe", icon_color="text-[#FF9A00]", category_label="Vector Graphics",
                 website_url="https://www.adobe.com/products/illustrator.html",
                 icon_image_url="https://cdn.simpleicons.org/adobeillustrator/FF9A00"),
            dict(name="Adobe Photoshop", icon_class="fa-brands fa-adobe", icon_color="text-[#31A8FF]", category_label="Image Editing",
                 website_url="https://www.adobe.com/products/photoshop.html",
                 icon_image_url="https://cdn.simpleicons.org/adobephotoshop/31A8FF"),
            dict(name="Premiere Pro", icon_class="fa-brands fa-adobe", icon_color="text-[#9999FF]", category_label="Video Editing",
                 website_url="https://www.adobe.com/products/premiere.html",
                 icon_image_url="https://cdn.simpleicons.org/adobepremierepro/9999FF"),
            dict(name="Adobe After Effects", icon_class="fa-brands fa-adobe", icon_color="text-[#CF96FF]", category_label="Motion Graphics",
                 website_url="https://www.adobe.com/products/aftereffects.html",
                 icon_image_url="https://cdn.simpleicons.org/adobeaftereffects/CF96FF"),
        ]
        for i, data in enumerate(tech_items):
            TechStackItem.objects.update_or_create(name=data['name'], defaults={**data, 'order': i})
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(tech_items)} tech stack items."))

        # ---- Collaborations (Institute Photos / Quotes slider) ----
        collaborations = [
            dict(name="Main Campus", quote="Stepping onto this campus, you can feel the energy of students building real projects, not just studying theory.", quote_author="Dr. Ahmed, Director"),
            dict(name="Computer Lab", quote="Our labs run the same tools used in the industry, so students graduate already comfortable with real developer workflows.", quote_author="Hina Malik, Lab Coordinator"),
            dict(name="Design Studio", quote="Watching a student's first Figma mockup turn into a live, working website is still the best part of my day.", quote_author="Umar Farooq, UI/UX Mentor"),
            dict(name="Auditorium", quote="Every batch closes with a demo day right here — parents and hiring partners watching students present their own products.", quote_author="Sana Tariq, Program Head"),
            dict(name="Student Workspace", quote="The collaborative workspace means juniors and seniors are constantly learning from each other, not just from us.", quote_author="Bilal Chaudhry, Senior Instructor"),
            dict(name="Library", quote="A quiet corner to read, plan a sprint, or just think — every serious institute needs one of these.", quote_author="Ayesha Noor, Librarian"),
        ]
        for i, data in enumerate(collaborations):
            obj, created = Collaboration.objects.update_or_create(
                name=data['name'],
                defaults={'order': i, 'quote': data['quote'], 'quote_author': data['quote_author']})
            if not obj.logo:
                img_bytes = make_placeholder_image(data['name'], size=(900, 650))
                if img_bytes:
                    obj.logo.save(f"{data['name'].lower().replace(' ', '-')}.png", ContentFile(img_bytes), save=True)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(collaborations)} institute photos."))

        # ---- Testimonials ----
        testimonials = [
            dict(name="Sarah Jenkins", role="CTO, Nexus Technologies", rating=5,
                 review="Tecnsol rebuilt our core web platform from the ground up. The performance boost was instant, Lighthouse scores jumped to 99 and user retention spiked by 40%."),
            dict(name="Marcus Vance", role="Founder, CyberScale", rating=5,
                 review="The modern dark aesthetic and micro-animations Tecnsol implemented gave our SaaS product a premium high-end enterprise feel. Exceptional engineering standards."),
            dict(name="Elena Rostova", role="Head of Product, HyperION", rating=5,
                 review="Communication was effortless and deadlines were met ahead of schedule. Tecnsol feels like having a senior team of world-class frontend architects on retainer."),
        ]
        for i, data in enumerate(testimonials):
            obj, _ = Testimonial.objects.update_or_create(
                name=data['name'], defaults={**data, 'order': i})
            if not obj.avatar:
                img_bytes = make_placeholder_image(data['name'].split()[0], size=(300, 300))
                if img_bytes:
                    obj.avatar.save(f"{data['name'].lower().replace(' ', '-')}.png", ContentFile(img_bytes), save=True)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(testimonials)} testimonials."))

        # ---- About Us ----
        about = AboutSection.load()
        if not about.image:
            img_bytes = make_placeholder_image("Tecnsol Team", size=(900, 700))
            if img_bytes:
                about.image.save("about-team.png", ContentFile(img_bytes), save=True)
        self.stdout.write(self.style.SUCCESS("Seeded About Section."))

        expertise_items = [
            dict(icon_class="fa-solid fa-code", title="Frontend Engineering",
                 description="Pixel-perfect, high-performance interfaces.", proficiency_pct=96),
            dict(icon_class="fa-solid fa-server", title="Backend & APIs",
                 description="Scalable Django & Node architectures.", proficiency_pct=92),
            dict(icon_class="fa-solid fa-palette", title="UI/UX Design",
                 description="Research-driven, conversion-focused design.", proficiency_pct=90),
            dict(icon_class="fa-solid fa-cloud", title="Cloud & DevOps",
                 description="CI/CD, containerization, zero-downtime deploys.", proficiency_pct=88),
        ]
        for i, data in enumerate(expertise_items):
            Expertise.objects.update_or_create(title=data['title'], defaults={**data, 'order': i})
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(expertise_items)} expertise items."))

        team_members = [
            dict(name="Imran Sheikh", role="Founder & Lead Engineer",
                 bio="Full-stack architect leading every build."),
            dict(name="Ayesha Khan", role="UI/UX Design Lead",
                 bio="Crafts the interfaces clients fall in love with."),
            dict(name="Bilal Ahmed", role="Backend Engineer",
                 bio="Keeps Django, APIs and databases rock solid."),
            dict(name="Hania Malik", role="Motion & Graphics Designer",
                 bio="Brings brand and video work to life."),
        ]
        for i, data in enumerate(team_members):
            obj, _ = TeamMember.objects.update_or_create(name=data['name'], defaults={**data, 'order': i})
            if not obj.photo:
                img_bytes = make_placeholder_image(data['name'].split()[0], size=(450, 600))
                if img_bytes:
                    obj.photo.save(f"{data['name'].lower().replace(' ', '-')}.png", ContentFile(img_bytes), save=True)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(team_members)} team members."))

        self.stdout.write(self.style.SUCCESS(
            "\nDone! Run the server and visit /admin/ to replace this placeholder "
            "content with your real projects, logos and photos."))
