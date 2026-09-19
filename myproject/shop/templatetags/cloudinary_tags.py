from django import template
from cloudinary.utils import cloudinary_url
from cloudinary import CloudinaryResource

register = template.Library()

@register.filter
def cloudinary_img(public_id, width=300):
    """
    Given a Cloudinary public_id or CloudinaryResource, returns a Cloudinary image URL.
    """
    try:
        # If it's a CloudinaryResource, extract public_id
        if isinstance(public_id, CloudinaryResource):
            public_id = public_id.public_id

        url, _ = cloudinary_url(
            public_id,
            width=width,
            crop="scale",
            secure=True
        )
        return url
    except Exception:
        return ""
