from crud_framework.schemas.base import BaseSchema


class ChoicesSchema(BaseSchema):
    CHOICES_CLASS = None

    def get(self):
        values = [v[0] for v in self.CHOICES_CLASS.get_choices()]
        return {
            'values': values,
            'count': len(values)
        }
