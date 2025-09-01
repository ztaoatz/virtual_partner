from ..system.tools import jsonutil
from django.shortcuts import HttpResponse as response
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def findstudent(request):
    print("开始查询学生信息")
    student = {
        "sname": "冼琛",
        "sex": "man",
        "nation": "China"
    }
    result = jsonutil.parse(student)
    return response(result)
