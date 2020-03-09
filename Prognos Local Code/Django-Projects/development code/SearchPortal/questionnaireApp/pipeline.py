from .models import Image


def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    url = None
    if backend.name == 'google-oauth2':
        url = response['picture']
    if url:
        user.avatar = url
        user.save()
        try:
            objects = Image.objects.get(userName=response['name'])
            if objects:
                pass
            else:
                Image(userName=response['name'], image=url).save()
        except:
            Image(userName=response['name'], image=url).save()
