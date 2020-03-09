from django.shortcuts import render
import datetime

# Create your views here.


def news(request):
    dt = datetime.datetime.now()
    h = int(dt.strftime("%H"))
    msg = "Good "
    if h >= 5 <= 12:
        msg += "morning"
    elif h <= 16:
        msg += "afternoon"
    elif h <= 20:
        msg += "evening"
    else:
        msg += "night"

    msg += " viewer"
    mydict = {'msg': msg, 'time': dt}

    return render(request, "testapp/index.html", context=mydict)


def moviesnews(request):
    news1 = "WAR collected over 350 cr."
    news2 = "HOUSEFULL 4 released on 25th Oct 2019"
    news3 = "Dabbang 3 trailer is boring"
    news4 = "Commando 3 has a better trailer than Dabang 3"
    mydict = {'news1': news1, 'news2': news2, 'news3': news3, 'news4': news4}
    return render(request, "testapp/movies.html", context=mydict)


def pnews(request):
    news1 = "BJP-Shiv Sena alliance won an absolute majority in the Maharashtra assembly polls."
    news2 = "As per the Election Commission, BJP secured 105 seats, Shiv Sena (56), Congress (44) and the Nationalist Congress Party (54)."
    news3 = "While Bahujan Vikas Aaghadi won 3 seats, the All India Majlis-E-Ittehadul Muslimeen, Prahar Janshakti Party and Samajwadi Party won 2 seats each."
    news4 = "As many as 13 independents were declared victorious across the state."
    mydict = {'news1': news1, 'news2': news2, 'news3': news3, 'news4': news4}
    return render(request, "testapp/politics.html", context=mydict)


def snews(request):
    news1 = "Vijay Hazare Trophy 2019 Final, Karnataka vs Tamil Nadu Highlights: Karnataka win by 60 runs, VJD method"
    news2 = "Jasprit Bumrah, Smriti Mandhana win Wisden India Almanack ‘Cricketer of the Year’ award"
    news3 = "New Zealand captain Kane Williamson to miss England T20 series"
    news4 = "National selectors on Dhoni, to Dhoni: We’re moving on"
    mydict = {'news1': news1, 'news2': news2, 'news3': news3, 'news4': news4}
    return render(request, "testapp/movies.html", context=mydict)


