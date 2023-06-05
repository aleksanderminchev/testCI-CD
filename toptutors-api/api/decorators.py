from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user
from apifairy import arguments, response
import sqlalchemy as sqla
from api.app import db
from api.schemas import StringPaginationSchema, PaginatedCollection, QueryCollection,StringQueryParams
import time


# Decorator to require admin role for accessing an endpoint
def admin_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return decorated_view


# Decorator to paginate responses for an endpoint
def paginated_response(schema, max_limit=2500, order_by=None,
                       order_direction='asc',
                       pagination_schema=StringPaginationSchema):
    def inner(f):
        @wraps(f)
        def paginate(*args, **kwargs):
            start_time = time.time()
            args = list(args)
            pagination = args.pop(-1)
            select_query = f(*args, **kwargs)
            if order_by is not None:
                o = order_by.desc() if order_direction == 'desc' else order_by
                select_query = select_query.order_by(o)

            count = db.session.scalar(sqla.select(
                sqla.func.count()).select_from(select_query))

            limit = pagination.get('limit', max_limit)
            offset = pagination.get('offset')
            after = pagination.get('after')
            if limit > max_limit:
                limit = max_limit
            if after is not None:
                if offset is not None or order_by is None:  # pragma: no cover
                    abort(400)
                if order_direction != 'desc':
                    order_condition = order_by > after
                    offset_condition = order_by <= after
                else:
                    order_condition = order_by < after
                    offset_condition = order_by >= after
                query = select_query.limit(limit).filter(order_condition)
                offset = db.session.scalar(sqla.select(
                    sqla.func.count()).select_from(select_query.filter(
                        offset_condition)))
            else:
                if offset is None:
                    offset = 0
                if offset < 0 or (count > 0 and offset >= count) or limit <= 0:
                    abort(400)

                query = select_query.limit(limit).offset(offset)

            data = db.session.scalars(query).all()
            end_time = time.time()
            time_elapsed = end_time - start_time
            print(f"Time complexity for input size n: {time_elapsed:.8f} seconds")
            data = [i.to_dict() for i in data]

            return {'data': data, 'pagination': {
                'offset': offset,
                'limit': limit,
                'count': len(data),
                'total': count,
            }}

        # wrap with APIFairy's arguments and response decorators
        return arguments(pagination_schema)(response(PaginatedCollection(
            schema, pagination_schema=pagination_schema))(paginate))
    db.session.remove()
    return inner


def query_params(schema,query_schema=StringQueryParams):
    """ Wrapper used to add query params to the route specified"""
    def inner(f):
        @wraps(f)
        def add_query_params(*args, **kwargs):
            print(*args)
            data=f(*args,**kwargs)
            return data
        return arguments(query_schema)(response(QueryCollection(
            schema,query_schema=query_schema))(add_query_params))
    db.session.remove()
    return inner