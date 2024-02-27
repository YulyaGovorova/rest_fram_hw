from rest_framework.serializers import ValidationError


class VideoValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = value.get(self.field)
        if tmp_value and 'youtube.com' not in tmp_value:
            raise ValidationError('Загружать только на Ютуб')