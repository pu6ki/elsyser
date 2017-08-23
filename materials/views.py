from rest_framework import viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_word_filter import FullWordSearchFilter

from students.models import Subject
from students.permissions import IsTeacher, IsTeacherAuthor

from .serializers import MaterialSerializer, MaterialReadSerializer
from .models import Material
from .filters import MaterialListFilterBackend


class MaterialsViewSet(viewsets.GenericViewSet):
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated, IsTeacher),
        'update': (IsAuthenticated, IsTeacher, IsTeacherAuthor),
        'destroy': (IsAuthenticated, IsTeacher, IsTeacherAuthor)
    }

    def get_serializer_class(self):
        return MaterialReadSerializer if self.request.method in ('GET',) else MaterialSerializer

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]


class MaterialsListViewSet(mixins.ListModelMixin, MaterialsViewSet):
    queryset = Material.objects.all()
    filter_backends = (MaterialListFilterBackend, FullWordSearchFilter)
    word_fields = ('title', 'section')


class NestedMaterialsViewSet(mixins.RetrieveModelMixin,
                             mixins.CreateModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             MaterialsListViewSet):
    def get_related_subject(self):
        return get_object_or_404(Subject, id=self.kwargs['subject_pk'])

    def get_queryset(self):
        subject = self.get_related_subject()

        return subject.materials

    def get_object(self):
        return get_object_or_404(self.get_queryset(), id=self.kwargs['pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['subject'] = self.get_related_subject()

        return context


    def retrieve(self, request, *args, **kwargs):
        material = self.get_object()

        serializer = self.get_serializer(material)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        material = self.get_object()
        self.check_object_permissions(request, material)

        serializer = self.get_serializer(material, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_200_OK, headers=headers)

    def destroy(self, request, *args, **kwargs):
        material = self.get_object()
        self.check_object_permissions(request, material)

        material.delete()

        return Response(None, status.HTTP_204_NO_CONTENT)
