from django.shortcuts import render,HttpResponse,redirect
from web import models
from web.myforms import RegisterForm
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = models.UserInfo.objects.filter(username=username, password=password).first()
        if user_obj:
            request.session['user_id'] = user_obj.id
            return redirect('rank')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})



def register(request):
    """

    :param request:
    :return: html
    """
    if request.method == 'GET':
        register_form_obj = RegisterForm()
        return render(request, 'register.html', {'register_form_obj': register_form_obj})
    else:
        register_form_obj = RegisterForm(request.POST)
        if register_form_obj.is_valid():
            register_form_obj.cleaned_data.pop('r_password')
            models.UserInfo.objects.create(**register_form_obj.cleaned_data)
            return redirect('login')
        else:
            return render(request, 'register.html', {'register_form_obj': register_form_obj})


