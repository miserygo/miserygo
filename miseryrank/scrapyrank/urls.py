from django.conf.urls import url

from scrapyrank import views
urlpatterns = [
    url(r'^main/', views.main, name='main'),

]
