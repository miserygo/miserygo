from django.conf.urls import url

from web.views import (
    auth, rank
)
urlpatterns = [
    url(r'^login/', auth.login, name='login'),
    url(r'^register/', auth.register, name='register'),
    url(r'^rank/', rank.rank, name='rank'),
    url(r'^good/', rank.good, name='good'),
    url(r'^collect/', rank.collect, name='collect'),
    url(r'^comment/', rank.comment, name='comment'),
    # url(r'^test/', rank.test, name='test'),
]
