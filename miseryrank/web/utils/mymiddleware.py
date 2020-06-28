from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect,render
from django.urls import reverse
from web import models

class UserAuth(MiddlewareMixin):
    def process_request(self,request):
        white_list = [reverse('login'), reverse('register')]
        if request.path in white_list:
            return
        user_id = request.session.get('user_id')
        if user_id:
            user_obj = models.UserInfo.objects.get(id=user_id)
            request.user_obj = user_obj
            return
        else:
            return redirect('login')