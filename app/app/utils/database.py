# -*- coding: utf-8 -*-
"""
    sxw 2016-7-7

    一些数据库帮助类或方法
    例如 CRUD mixin
"""
import datetime
from contextlib import contextmanager

from flask import current_app
from sqlalchemy.orm import class_mapper, sessionmaker

from app.configs.code import ResponseCode, ResponseLevel
from app.my_extensions import db


class CRUDMixin(object):
    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

    def create(self, commit=False, **kwargs):
        """
        sxw 2016-7-7

        根据parser解析的dict form字段，自动填充相应字段

        :param commit:  是否提交，默认为False
        :param kwargs: 创建模型关联的字典值
        :return self or False: 若commit为False， 则返回false;反之且提交成功，则返回self
        """
        kwargs.pop("page", None)
        kwargs.pop("per_page", None)
        kwargs.pop("q_names", None)
        kwargs.pop("q_values", None)
        kwargs.pop("q_type", None)
        kwargs.pop("o_names", None)
        kwargs.pop("o_values", None)
        for attr, value in kwargs.iteritems():
            # Flask-RESTful make everything None by default: /
            if value is not None and hasattr(self, attr):
                setattr(self, attr, value)
        return self.save(commit=commit)

    def update(self, commit=False, **kwargs):
        """
        sxw 2016-7-7

        更新已有实体的一些提交字段（排除id）

        :param commit: 是否提交，默认提交
        :param kwargs:  参数值
        :return self or False: 若commit为False， 则返回false;反之且提交成功，则返回self
        """
        kwargs.pop("id", None)
        for attr, value in kwargs.iteritems():
            # Flask-RESTful make everything None by default: /
            if value is not None and hasattr(self, attr):
                setattr(self, attr, value)
        return commit and self.save(commit=commit) or self

    def save(self, commit=False):
        """
        sxw 2016-7-7

        保存对象到数据库中，持久化对象

        :param commit: 是否提交，默认提交
        :return self or False: 若commit为False， 则返回false;反之且提交成功，则返回self
        """
        db.session.add(self)
        db.session.flush()
        commit and db.session.commit()
        return self

    def delete(self, commit=False):
        """
        sxw 2016-7-7

        删除对象，从数据库中删除记录

        :param commit: 是否提交，默认提交
        :return self or False: 若commit为False， 则返回false;反之且提交成功，则返回self
        """
        db.session.delete(self)
        commit and db.session.commit()
        return self

    @classmethod
    def page(cls, args):
        """
        通用分页查询模块，使用组合sql查询

        :param args: 传递的request参数解析
        :return: 查询出来的条目
        """
        q_names = args['q_names']
        q_values = args['q_values']
        page_query = cls.query
        q_type = args['q_type']

        # 校验查询参数键与值是否匹配
        if q_names is None and q_values is None:
            page_query = page_query
        elif q_names and q_values and len(q_names) == 1 and len(q_values) == 1 and q_type is None:
            query = ''.join(['cls.', q_names[0], '.like(u"%', q_values[0], '%")'])
            page_query = page_query.filter(eval(query))
        elif q_names and q_values and len(q_names) == 2 and len(q_values) == 2 and (q_type == "or" or q_type == "and"):
            query1 = ''.join(['cls.', q_names[0], '.like(u"%', q_values[0], '%")'])
            query2 = ''.join(['cls.', q_names[1], '.like(u"%', q_values[1], '%")'])
            if q_type == "or":
                page_query = page_query.filter(db.or_(eval(query1), eval(query2)))
            else:
                page_query = page_query.filter(db.and_(eval(query1), eval(query2)))
        else:
            from app.utils.response import res
            return res(ResponseCode.VALIDATE_FAIL, u"查询参数错误，请重试!", ResponseLevel.DANGER)

        o_names = args['o_names']
        o_values = args['o_values']
        # 校验排序参数键与值是否匹配
        if o_names is None and o_values is None:
            pass
        elif len(o_names) == 1 and len(o_values) == 1:
            page_query = page_query.order_by(" %s %s " % (o_names[0], o_values[0]))
        elif len(o_names) == 2 and len(o_values) == 2:
            page_query = page_query.order_by(" %s %s, %s %s " % (o_names[0], o_values[0], o_names[1], o_values[1]))
        else:
            from app.utils.response import res
            return res(ResponseCode.VALIDATE_FAIL, u"排序参数错误，请重试!", ResponseLevel.DANGER)

        # 获取总数
        total_count = page_query.count()
        # 分页参数
        data = page_query.paginate(args['page'], args['per_page'], False).items
        from app.utils.response import res_page
        return res_page(args, data=data, total_count=total_count)


def model_to_dict(obj, visited_children=None, back_relationships=None):
    """
        sxw 2016-06-23

        实现模型自动to_dict功能
        引用自：http://stackoverflow.com/questions/23554119/convert-sqlalchemy-orm-result-to-dict
    """
    if visited_children is None:
        visited_children = set()
    if back_relationships is None:
        back_relationships = set()
    serialized_data = {}
    for c in obj.__table__.columns:
        name = c.name
        if hasattr(obj, name):
            value = getattr(obj, c.name)
        else:
            # 针对python中关键字冲突，添加后下划线以避免冲突情况，例如class => class_
            name = "%s_" % name
            value = getattr(obj, name)

        if isinstance(value, (datetime.date, datetime.time)):
            serialized_data[name] = datetime.datetime.strftime(value, '%Y-%m-%d %H:%M:%S' if isinstance(value, (
                datetime.time, datetime.datetime)) else '%Y-%m-%d')
        elif isinstance(value, set):
            serialized_data[name] = list(value)
        else:
            serialized_data[name] = value

    relationships = class_mapper(obj.__class__).relationships
    visitable_relationships = [(name, rel) for name, rel in relationships.items() if name not in back_relationships]
    for name, relation in visitable_relationships:
        if relation.backref:
            back_relationships.add(relation.backref)
        relationship_children = getattr(obj, name)
        if relationship_children is not None:
            if relation.uselist:
                children = []
                for child in [c for c in relationship_children if c not in visited_children]:
                    visited_children.add(child)
                    children.append(model_to_dict(child, visited_children, back_relationships))
                serialized_data[name] = children
            else:
                serialized_data[name] = model_to_dict(relationship_children, visited_children, back_relationships)
    return serialized_data


@contextmanager
def new_session():
    """
    sxw 2016-12-7

    上下文管理器生成session，为事务生成专用的会话
    """
    # 初始化事务会话类
    session = sessionmaker(bind=db.engine)
    s = session()
    current_app.logger.info("New transaction and session {} begin!".format(s))
    try:
        yield s
    except Exception as e:
        s.rollback()
        current_app.logger.error("Transaction and session {} {}!".format(s, e))
    current_app.logger.info("Transaction and session {} finished!".format(s))
