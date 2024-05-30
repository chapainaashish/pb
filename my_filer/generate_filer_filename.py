import os
from datetime import date

from django.utils.encoding import force_str
from django.utils.text import get_valid_filename as get_valid_filename_django
from django.template.defaultfilters import slugify as slugify_django

from unidecode import unidecode


def slugify(string):
    return slugify_django(unidecode(force_str(string)))


def get_valid_filename(s):
    """
    like the regular get_valid_filename, but also slugifies away
    umlauts and stuff.
    """
    s = get_valid_filename_django(s)
    filename, ext = os.path.splitext(s)
    filename = slugify(filename)
    ext = slugify(ext)
    if ext:
        return "%s.%s" % (filename, ext)
    else:
        return "%s" % (filename,)


def custom_filename(instance, filename):
    now = date.today()
    return os.path.join(str(now.year), str(now.month).zfill(2), get_valid_filename(filename))
