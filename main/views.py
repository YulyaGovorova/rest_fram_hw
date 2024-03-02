import stripe
import os
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from main.models import Course, Lesson, Payment, Subscription
from main.pagination import CourseLessonPaginator
from main.permissions import Moderator, UserOwner, UserPerm
from main.serializers import CourseSerializers, LessonSerializers, PaymentSerializers, PaymentCreateSerializer, \
    SubscriptionSerializer

from main.tasks import check_update_course

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()
    pagination_class = CourseLessonPaginator

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, Moderator]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, Moderator | UserOwner]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, Moderator | UserOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, UserOwner]
        return [permission() for permission in self.permission_classes]

    # def perform_create(self, serializer):
    #     new_course = serializer.save()
    #     new_course.user = self.request.user
    #     new_course.save()

    def perform_update(self, serializer):
        course_update = serializer.save()
        if course_update:
            check_update_course.delay(course_update.course_id)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializers
    # permission_classes = [IsAuthenticated, Moderator]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CourseLessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, Moderator | UserOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, Moderator | UserOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, UserOwner]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializers
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("payment_date",)
    permission_classes = [IsAuthenticated]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializers
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializers
    stripe.api_key = os.getenv('STRIPE_API_KEY')
    serializer_class = PaymentCreateSerializer
    queryset = Payment.objects.all()

    def create(self, request, *args, **kwargs):
        stripe.api_key = os.getenv("STRIPE_API_KEY")
        course_id = request.data.get("course")

        user = self.request.user
        data = {"user": user.id, "course": course_id, "is_confirmed": True}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response = stripe.PaymentIntent.create(
            amount=2000,
            currency="usd",
            automatic_payment_methods={"enabled": True, "allow_redirects": "never"},
        )

        stripe.PaymentIntent.confirm(
            response.id,
            payment_method="pm_card_visa",
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SubscriptionCreateAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, Moderator | UserOwner]

    def create(self, request, *args, **kwargs):
        course_pk = self.kwargs.get('course_pk')

        serializer = self.get_serializer(data={'user': request.user.pk, 'course': course_pk})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'Вы подписаны на курс.'}, status=status.HTTP_201_CREATED)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, UserPerm]