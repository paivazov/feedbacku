from typing import Optional, Union

from django.contrib.sites.models import Site
from django.urls import reverse


def get_url_path(
    reverse_name: str, args: Optional[Union[list, tuple]] = None
) -> str:
    """Returns full path including domain and url from reverse_name
    Args:
        reverse_name: "name" of url that defined in urls.py
        args: constructs path (e.g. args=("expl",) dom.com/url_path/expl/)

    Returns:
        URI path
    """
    domain = Site.objects.get_current().domain
    url = reverse(reverse_name, args=args)
    return domain + url
