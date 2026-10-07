# Tecnsol — Django Website

Full Django rebuild of the Tecnsol single-page site. Same design (dark theme,
maroon/neon accents, glass cards, animations) — now backed by Python/Django,
with every section editable from the admin panel and each navbar item opening
its own page.

## What changed vs the original single HTML file

- **Backend:** Python + Django (SQLite by default, easy to swap for Postgres).
- **Separate pages per navbar item:** Home, Services, Projects, Tech Stack,
  Reviews, Contact are now real Django pages/URLs (not just `#anchors`).
  Home is still the one full scrolling page with every section, like before.
- **"Portfolio" → "Projects"**, with a `category` field so every project is
  tagged **Web Development** or **Graphics Design**, and the Projects page
  has filter tabs for each.
- **New "Collaborations" section** (companies Tecnsol works with) on the
  Tech Stack page and on the homepage — logos are uploaded from the admin.
- **Everything is admin-managed:** hero copy & stats, services, projects
  (with images), tech stack items, collaborations (with logos), testimonials
  (with avatars), and every contact form submission is saved and viewable
  in the admin.

## Project layout

```
tecnsol/
├── manage.py
├── requirements.txt
├── tecnsol/            # project settings, root urls
└── core/               # the app: models, admin, views, templates
    ├── models.py       # SiteSettings, Service, Project, TechStackItem,
    │                   # Collaboration, Testimonial, ContactMessage
    ├── admin.py        # admin panel configuration
    ├── views.py         # one view per page
    ├── urls.py
    ├── forms.py         # contact form
    ├── templates/core/  # base.html + one template per page + partials/
    └── management/commands/seed_demo_data.py  # optional demo content
```

## Setup (run these on your own machine)

```bash
# 1. Create & activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create the database tables
python manage.py makemigrations core
python manage.py migrate

# 4. Create your admin login
python manage.py createsuperuser

# 5. (Optional but recommended) fill the site with demo content
#    so it doesn't look empty on first run — replace it later from /admin/
python manage.py seed_demo_data

# 6. Run the dev server

```

Then open:
- **Website:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin/

## Managing content from the admin panel

Everything below is edited or uploaded from **/admin/** — no code changes needed:

| Section on the site        | Model in admin      |
|-----------------------------|----------------------|
| Hero text, stats, contact info, map | Site Settings (map: paste a Google Maps embed URL, or leave blank to auto-generate one from the Location field) |
| About Us copy + image        | About Section        |
| About Us expertise/skill bars | Expertise            |
| About Us team grid            | Team Members         |
| Services grid                | Services (title, description, tags, icon, **Fee**, **Duration**, optional longer Detail Description shown on that service's own page) |
| Projects (Web Dev / Graphics) | Projects (has a Category dropdown + image upload) |
| Tech Stack cards (incl. Adobe apps) | Tech Stack Items (optional Website URL makes the card clickable) |
| Collaborations logos          | Collaborations      |
| Reviews / Testimonials        | Testimonials        |
| Contact form submissions      | Contact Messages (read-only, view what visitors sent) |

Note: the Contact section (form + info + map) now lives only on the dedicated
**Contact page** (`/contact/`, linked from the navbar) — the homepage no
longer embeds it.

To add a new project: **Admin → Projects → Add Project**, pick a category
(Web Development or Graphics Design), upload an image, add tags — it shows
up instantly on the Projects page under the right tab, and on the homepage
if you tick "is featured".

## "More Info" → service detail page → "Apply Now" → email

Every service card now has a **More Info** button that opens a dedicated
page for that service (`/services/<its-slug>/`), showing its full
description, **Fee**, and **Duration** — all editable from
**Admin → Services**. That page's **Apply Now** button sends the visitor to
the Contact page with that service pre-selected in the dropdown. When they
submit the form:

1. The submission is saved to **Admin → Contact Messages** as always
   (name, email, the exact service applied for, budget, message).
2. An email is sent to your inbox with all of that data — see below to
   turn this on.

This works for **any** service you add later from the admin panel — no
code changes needed; a new service automatically gets its own detail page
and shows up in the Apply Now dropdown.

### Turning on real email notifications

By default the site just prints the email to your terminal (nothing is
actually sent) so it runs with zero setup. To receive a real email every
time someone submits the Contact form or applies for a service:

1. Use a Gmail account (or any SMTP provider). For Gmail, turn on
   2-Step Verification, then create an **App Password**:
   Google Account → Security → 2-Step Verification → App passwords.
2. Set these environment variables before running the server (Windows
   PowerShell shown; use `export` instead of `$env:` on macOS/Linux):

   ```powershell
   $env:DJANGO_EMAIL_HOST_USER = "youraddress@gmail.com"
   $env:DJANGO_EMAIL_HOST_PASSWORD = "your-16-char-app-password"
   $env:DJANGO_NOTIFY_EMAIL = "whereyouwantinquiries@gmail.com"   # optional
   python manage.py runserver
   ```

   Leaving `DJANGO_NOTIFY_EMAIL` unset sends inquiries to the **Contact
   Email** field in Admin → Site Settings instead.
3. That's it — no code changes. Submit the Contact form once to test it.

For a permanent local setup, put those three lines in a `.env` file and
load it with a package like `python-dotenv`, or set them as system
environment variables — just make sure `DJANGO_EMAIL_HOST_PASSWORD` is
never committed to git (it's a secret).

## Notes

- Uploaded images are stored in `/media/` and served automatically while
  `DEBUG=True`. For production, serve `/media/` and `/static/` via your web
  server (nginx, whitenoise, S3, etc.) and set `DEBUG=False` +
  `DJANGO_ALLOWED_HOSTS` in your environment.
- The contact form saves every submission to the database (`Contact Messages`
  in the admin) **and** emails your inbox once you set the environment
  variables described above — see "Turning on real email notifications".
- `seed_demo_data` generates simple placeholder images with Pillow so the
  site isn't empty — delete/replace them from the admin whenever you're
  ready with real photos and logos.

---

### Quick start (خلاصہ):
`pip install -r requirements.txt` → `python manage.py makemigrations core` →
`python manage.py migrate` → `python manage.py createsuperuser` →
`python manage.py seed_demo_data` (dummy data ke liye) →
`python manage.py runserver`. Phir `/admin/` per ja kar apni real projects,
graphics, aur collaboration logos upload kar dein — sab kuch backend se
manage hota hai, koi code change nahi karna parega.
