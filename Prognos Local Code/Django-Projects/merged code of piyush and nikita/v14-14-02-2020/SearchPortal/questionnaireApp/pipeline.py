from .models import Image


def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    print("inside pipeline method")
    url = None
    if backend.name == 'google-oauth2':
        url = response['picture']
    if url:
        user.avatar = url
        user.save()
        # profileObejct = Profile.objects.all()
        # print("profile : ", profileObejct[0].user)
        # print("user : ", user)
        try:
            objects = Image.objects.get(userName=response['name'])
            if objects:
                pass
                print("passed")
            else:
                Image(userName=response['name'], image=url).save()
                print("saved")
        except:
            Image(userName=response['name'], image=url).save()
            print("inside except objects saved")