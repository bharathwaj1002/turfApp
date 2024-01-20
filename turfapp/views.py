from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')



def about(request):
    return render(request,'about-us.html')



def contacts(request):
    return render(request,'contacts.html')



def typography(request):
    return render(request,'typography.html')