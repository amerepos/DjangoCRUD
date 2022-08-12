from crud_framework.errors import Error, HttpStatus
from crud_framework.schemas import CrudSchema


class UserAwareCrudSchema(CrudSchema):
    USER_FIELD = None

    def __init__(self, initkwargs, *args, **kwargs):
        if not self.USER_FIELD:
            raise Error(
                code=-1, status=HttpStatus.HTTP_405_METHOD_NOT_ALLOWED, field_name='USER_FIELD',
                message='USER_FIELD missing', description='USER_FIELD missing')

        self.user = initkwargs.get('user', None)
        if not self.user:
            raise Error(code=-1, status=HttpStatus.HTTP_406_NOT_ACCEPTABLE, field_name='user',
                        message='user missing', description='user missing')

        super(UserAwareCrudSchema, self).__init__(initkwargs=initkwargs, *args, **kwargs)
        print(f'USER: {self.user}')

        # if not isinstance(self.MODEL_CLASS, BaseTrackedModel): TODO
        #     raise Error(
        #         code=-1, status=HttpStatus.HTTP_405_METHOD_NOT_ALLOWED, field_name='MODEL_CLASS',
        #         message='Class must be of type BaseTrackedModel', description='Class must be of type BaseTrackedModel')

    def get_queryset(self):
        self.filters[self.USER_FIELD] = self.user
        return super(UserAwareCrudSchema, self).get_queryset()

    def post(self, **data):  # TODO make sure user can create
        return super(UserAwareCrudSchema, self).post(editor=self.user, **data)

    def put(self, **data):  # TODO make sure user can edit
        return super(UserAwareCrudSchema, self).put(editor=self.user, **data)

    def delete(self, **data):  # TODO make sure user can delete
        return super(UserAwareCrudSchema, self).delete(editor=self.user, **data)


class PermissionMixin:
    VIEW_PERM = None
    ADD_PERM = None
    EDIT_PERM = None
    DELETE_PERM = None

    def __init__(self, *args, **kwargs):
        super(PermissionMixin, self).__init__(*args, **kwargs)
        self.app_label = self.MODEL_CLASS._meta.app_label

    def get(self, *args, **kwargs):
        if not self.VIEW_PERM:
            self.VIEW_PERM = f"{self.app_label}.view_{self.model_name}"

        if self.user.has_perm(self.VIEW_PERM):
            return super(PermissionMixin, self).get(*args, **kwargs)
        else:
            raise Error(status=HttpStatus.HTTP_403_FORBIDDEN, field_name='user', message='You can\'t view this item!')

    def post(self, *args, **kwargs):
        if not self.ADD_PERM:
            self.ADD_PERM = f"{self.app_label}.add_{self.model_name}"

        if self.user.has_perm(self.ADD_PERM):
            return super(PermissionMixin, self).post(*args, **kwargs)
        else:
            raise Error(status=HttpStatus.HTTP_403_FORBIDDEN, field_name='user', message='You can\'t create this item!')

    def put(self, *args, **kwargs):
        if not self.EDIT_PERM:
            self.EDIT_PERM = f"{self.app_label}.change_{self.model_name}"

        if self.user.has_perm(self.EDIT_PERM):
            return super(PermissionMixin, self).put(*args, **kwargs)
        else:
            raise Error(status=HttpStatus.HTTP_403_FORBIDDEN, field_name='user', message='You can\'t edit this item!')

    def delete(self, *args, **kwargs):
        if not self.DELETE_PERM:
            self.DELETE_PERM = f"{self.app_label}.delete_{self.model_name}"

        if self.user.has_perm(self.DELETE_PERM):
            return super(PermissionMixin, self).delete(*args, **kwargs)
        else:
            raise Error(status=HttpStatus.HTTP_403_FORBIDDEN, field_name='user', message='You can\'t delete this item!')
