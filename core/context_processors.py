from .models import SiteSettings


def site_settings(request):
    """Make SiteSettings available in every template as `site`."""
    return {'site': SiteSettings.load()}
