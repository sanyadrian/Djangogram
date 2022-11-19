from djangogram.models import Tag


def subject_renderer(request):
    tags = request.GET.get('tag')
    tag = Tag.objects.filter(name=tags)
    return {
        'tag': tag
    }