from web.utils import sqlalchemy
from web.utils.sqlalchemy import session, Collect, Block, Hot, Comment,createdatable
# sqlalchemy.Base.metadata.create_all(sqlalchemy.engine)
# co = session.query(Collect.hot_id).filter_by(user_id=1).all()
# print(co)
# block = 'ZhiHu'
# # blocks = session.query(Block).filter_by(name='ZhiHu').all()
# blocks_c = session.query(Block).filter_by(name=block).first()
# hots = blocks_c.hots
# # print(hots.count())
# hots = sqlalchemy.session.query(sqlalchemy.Hot).all()
# print(blocks_c,len(hots))

# hots = session.query(Collect).filter_by(user_id=1).all()
# hots = session.query(Block).filter_by(name='ZhiHu').first().hots
# blocks_c = session.query(Block).filter_by(name='Zhihu').all()
# hots = blocks_c.hots
# print(hots.title)
# print(hots.url)
# for hot in hots:
#     print(hot.hots.title)

# hots = session.query(Hot.good).filter(Hot.good>0).order_by(Hot.good.desc()).all()
# hots = session.query(Hot).first()
# list = list(hots.comments)
# print(type(list))
createdatable()