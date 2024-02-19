from rest_framework import serializers
from main.models import Course, Lesson, Payment


class LessonSerializers(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializers(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField() # количество уроков
    lessons = LessonSerializers(source='lesson_set', read_only=True, many=True) # список уроков

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, instance):
        return instance.lesson_set.count()


class PaymentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('paid_course', 'summ', 'payment_method')
