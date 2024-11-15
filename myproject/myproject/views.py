from django.http import HttpRequest,HttpResponse,JsonResponse


def home_page(request):
    print("welcome to my webpage");
    return JsonResponse({"message":"welcome to my webpage"},safe=False)