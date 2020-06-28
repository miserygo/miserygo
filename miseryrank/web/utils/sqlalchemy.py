from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, sessionmaker
engine = create_engine("mysql+pymysql://root:123@127.0.0.1:3306/testrank?charset=utf8", echo=True, max_overflow=5)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# 实例化
session = Session()

class Userinfo(Base):
    __tablename__ = 'web_userinfo'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(Integer)
    email = Column(String(50))
    telephone = Column(Integer)
    # is_active = Column(default=True)
    comments = relationship("Comment", backref='userinfo')

class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True)
    user = Column(Integer,ForeignKey(Userinfo.id))
    content = Column(Text(), nullable=True)
    hot_id = Column(Integer, ForeignKey('hot.id'))



class Collect(Base):
    __tablename__='collect'
    __table_args__ = {'keep_existing': True}
    nid = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('userinfo.id'))
    hot_id = Column(Integer, ForeignKey('hot.id'))
    users = relationship("Userinfo", backref='hot_to_user')
    hots = relationship("Hot", backref='hot_to_user')

class Block(Base):
    __tablename__='block'
    __table_args__ = {'keep_existing':True}
    id=Column(Integer, primary_key=True)
    name=Column(String(128))
    hots=relationship('Hot',
                         backref='block',
                         cascade='all,delete-orphan')

    @classmethod
    def addBlock(cls,name):
        try:
            block=Block(name=name)
            session.add(block)
            session.commit()
            return 0
        except:
            print('rolllback')
            session.rollback()
            return 1

    @classmethod
    def getBlocks(cls):
        # return session.query(Block).all()
        return session.query(Block)



class Hot(Base):
    __tablename__='hot'
    __table_args__ = {'keep_existing':True}
    id = Column(Integer, primary_key=True)
    title=Column(Text())
    content=Column(Text(),nullable=True)
    url=Column(Text())
    good = Column(Integer,default=0)
    block_id=Column(Integer,ForeignKey('block.id'))
    comments = relationship('Comment',
                        backref='hot',
                        cascade='all,delete-orphan')
    
    @classmethod
    def addHot(cls,block,title,content,url):
        try:
            b=session.query(Block).filter_by(name=block).first().id
            hot=Hot(title=title,content=content,url=url,block_id=b)
            session.add(hot)
            session.commit()
            return 0
        except:
            print('rolllback')
            session.rollback()
            return 1
def createdatable():
    Base.metadata.create_all(engine)
if __name__ == '__main__':
    # Base.metadata.create_all()
    createdatable()