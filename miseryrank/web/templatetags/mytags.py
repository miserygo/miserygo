from django import template
from web.utils.page import MyPagenation
from web.utils.sqlalchemy import session,Block,Hot
from sqlalchemy.sql import func
from django.conf import settings
from django.shortcuts import redirect
register = template.Library()
from django.urls import reverse
from django.http.request import QueryDict

@register.simple_tag()
def page_html(request, block):
    count = 0
    get_data = request.GET.copy()
    page_num = request.GET.get('page')
    base_url = request.path
    per_page_num = settings.PER_PAGE_NUM  # 每页显示多少条数据
    page_num_show = settings.PAGE_NUM_SHOW  # 显示的页码数
    count_list = session.query(Hot.block_id, func.count('*')).group_by(Hot.block_id).all()
    for i in count_list:
        if i[0] == block.id:
            count = i[1]
    page_obj = MyPagenation(page_num, count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_hmtl()
    return page_html
@register.simple_tag
def resole_url(request,url_name,block):
    # 编辑保存之后跳转回的路径
    next_url = request.get_full_path()
    reverse_url = reverse(url_name)
    q = QueryDict(mutable=True)
    q['block'] = block
    next_url = q.urlencode()
    full_url = reverse_url + '?' + next_url
    # print(full_url)
    return full_url

@register.filter
def index(comments,num):
    li = []
    for i in comments:
        li.append(i)
    return li[num]


if __name__ == '__main__':
    obj = session.query(Hot.block_id, func.count('*')).group_by(Hot.block_id).all()

    print(obj,type(obj))
