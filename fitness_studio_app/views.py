from django.http import HttpResponse

def home_page(request):
    print("Home page")
    return HttpResponse("Welcome to the Fitness Studio App for testing!")
