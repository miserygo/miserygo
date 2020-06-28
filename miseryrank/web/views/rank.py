from django.shortcuts import render,redirect,HttpResponse
from web.utils import sqlalchemy
import re
from django.db.models import Q
from django.conf import settings
from web.utils.sqlalchemy import session, Block, Hot, Collect, Comment
from web.utils.page import MyPagenation
def rank(request,block='all'):
    blocks = sqlalchemy.Block.getBlocks()
    block = request.GET.get('block')
    print('block', block)
    if block:
        blocks_c = session.query(Block).filter_by(name=block).first()
        hots = blocks_c.hots
    else:
        blocks_c = blocks
        hots = sqlalchemy.session.query(sqlalchemy.Hot).all()
    get_data = request.GET.copy()
    page_num = request.GET.get('page')
    kw = request.GET.get('kw')


    if kw:
        kw = kw.strip()
        hots = sqlalchemy.session.query(sqlalchemy.Hot).filter(sqlalchemy.Hot.title.like(f'%{kw}%')).all()
    base_url = request.path
    hot_count = len(hots)
    per_page_num = settings.PER_PAGE_NUM  # 每页显示多少条数据
    page_num_show = settings.PAGE_NUM_SHOW  # 显示的页码数

    page_obj = MyPagenation(page_num, hot_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_hmtl()
    hot_objs = hots[page_obj.start_data_num:page_obj.end_data_num]
    return render(request, 'rank.html',{'blocks': blocks, 'blocks_c':blocks_c,'hot_list': hot_objs, 'page_html': page_html})

def good(request):
    if request.method == 'GET':
        hots = session.query(Hot).filter(Hot.good > 0).order_by(Hot.good.desc()).all()
        return render(request, 'collect.html', {'list_hots': hots})
    if request.method == 'POST':
        nid = request.POST.get('id')
        hot_obj = session.query(Hot).filter_by(id=nid).one()
        good = int(hot_obj.good)
        good += 1
        session.query(Hot).filter_by(id=nid).update(
            {'good': good}
        )
        session.commit()
    return redirect('rank')

def collect(request):
    user_id = request.session.get('user_id')
    if request.method == 'GET':
        hots = session.query(Collect).filter_by(user_id=1).all()
        list_hots = []
        for hot in hots:
            list_hots.append(hot.hots)
        return render(request, 'collect.html',{'list_hots': list_hots})
    if request.method == 'POST':

        nid = request.POST.get('id')
        col = session.query(Collect.hot_id).filter_by(user_id=user_id).all()
        list = []
        for eve_co in col:
            list.append(eve_co[0])
        if int(nid) not in list:
            session.add_all([
                Collect(user_id=user_id, hot_id=nid),
            ])
            session.commit()
        return HttpResponse('ok')

def comment(request):
    content = request.POST.get('content')
    id = request.POST.get('id')
    id = re.findall(r'comment(\d+)go',id)[0]
    id = int(id)
    user_id = request.session.get('user_id')
    session.add_all([
        Comment(user=int(user_id), hot_id=id, content=content),
    ])
    session.commit()
    return HttpResponse('ok')



