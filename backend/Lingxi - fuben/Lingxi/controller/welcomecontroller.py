from django.shortcuts import render


def welcome(request):
    print("进入welcome函数")
    result = {"sname": "冼琛"}
    return render(request, 'welcome.html', result)
