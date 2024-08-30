def is_content_manager(request):
    return {
        'is_content_manager': request.user.groups.filter(name="Content Managers").exists() if request.user.is_authenticated else False
    }