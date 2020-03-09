from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request, name=""):
    l = [{'a': 1, 'b': 2, 'c': 3}, {'a': 11, 'b': 22, 'c': 33}, {'a': 111, 'b': 222, 'c': 333}]

    if name == "":
        data = ['latiket', 'akash', 10, 20]
        name = "Dom"
        context = {"msg": "welcome ", "data": data, "name": name, 'l': l}
        return render(request, "urlDemo/home.html", context)
    else:
        data = [10, 20]
        context = {"msg": "welcome ", "data": data, "name": name, 'first': True, 'l': l}
        return render(request, "urlDemo/second.html", context)


def out(request, name, d):
    print("inside out")
    print("d1 = ", d)
    data = ['latiket', 'akash', 10, 20]
    context = {"msg": "welcome ", "data": data, "number": d, "name": name, 'first': False}
    return render(request, "urlDemo/second.html", context)

