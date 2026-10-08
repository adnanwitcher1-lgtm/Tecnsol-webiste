import re

from .models import SiteSettings


def _whatsapp_number(phone):
    """Digits-only international number for wa.me links.
    '+92 300 1234567' -> 923001234567, '0300-1234567' -> 923001234567."""
    digits = re.sub(r"\D", "", phone or "")
    if digits.startswith("00"):
        digits = digits[2:]
    elif digits.startswith("0"):
        digits = "92" + digits[1:]
    return digits


def site_settings(request):
    """Make SiteSettings available in every template as `site`."""
    site = SiteSettings.load()
    return {
        'site': site,
        'whatsapp_number': _whatsapp_number(site.contact_phone),
    }
