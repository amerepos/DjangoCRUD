from crud_framework.errors import Error, HttpStatus
from crud_framework.models import BaseTrackedModel
from crud_framework.schemas import CrudSchema


class UserAwareCrudSchema(CrudSchema):
    USER_FIELD = None

    def __init__(self, user, *args, **kwargs):
        if not self.USER_FIELD:
            raise Error(
                code=-1, status=HttpStatus.HTTP_405_METHOD_NOT_ALLOWED, field_name='USER_FIELD',
                message='USER_FIELD missing', description='USER_FIELD missing')

        self.user = user
        super(UserAwareCrudSchema, self).__init__(*args, **kwargs)
        print(f'USER: {self.user}')

        # if not isinstance(self.MODEL_CLASS, BaseTrackedModel): TODO
        #     raise Error(
        #         code=-1, status=HttpStatus.HTTP_405_METHOD_NOT_ALLOWED, field_name='MODEL_CLASS',
        #         message='Class must be of type BaseTrackedModel', description='Class must be of type BaseTrackedModel')

    def set_queryset(self, filters):
        filters[self.USER_FIELD] = self.user
        return super(UserAwareCrudSchema, self).set_queryset(filters)

    def post(self, **data):
        return super(UserAwareCrudSchema, self).post(creator=self.user, editor=self.user, **data)

    def put(self, **data):
        return super(UserAwareCrudSchema, self).put(editor=self.user, **data)

    def delete(self, **data):
        return super(UserAwareCrudSchema, self).delete(editor=self.user, **data)
