from django.utils.safestring import mark_safe


def parse_url_as_image_tag(url):
    if url:
        return mark_safe('<img src="%s" style="width: 50px; height:50px;" />' % url)
    return url
