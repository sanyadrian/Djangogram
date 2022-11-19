import re
from djangogram.models import Tag

TAGS_REGEX = '#((\w|[\u00A1-\uFFFF])+)'


def extract_tags(post):
    # if post.description is "":
    #     return post.description
    # else:
    tags = re.findall(TAGS_REGEX, str(post.description), flags=0)
    current_tags = []
    for tag in tags:
        obj, _ = Tag.objects.get_or_create(name=tag[0])
        current_tags.append(obj)
    post.tags.set(current_tags)
    return tags

