from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from materials.serializers import MaterialSerializer, MaterialReadSerializer
from materials.models import Material
from students.models import Subject
from students.permissions import IsStudent, IsTeacher


class MaterialsViewSet(viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated, IsTeacher),
        'update': (IsAuthenticated, IsTeacher),
        'destroy': (IsAuthenticated, IsTeacher)
    }


    def get_serializer_class(self):
         return MaterialReadSerializer if self.request.method in ('GET',) else MaterialSerializer


    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]


class MaterialsListViewSet(mixins.ListModelMixin, MaterialsViewSet):
    def get_queryset(self):
        request = self.request
        all_materials = Material.objects.all()

        if IsTeacher().has_permission(request, self):
            return all_materials.filter(subject=request.user.teacher.subject)

        return all_materials.filter(class_number=request.user.student.clazz.number)


class NestedMaterialsViewSet(mixins.RetrieveModelMixin,
                             mixins.CreateModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             MaterialsListViewSet):

    def get_queryset(self):
        subject_id = self.kwargs['subject_pk']
        subject = get_object_or_404(Subject, id=subject_id)

        return super().get_queryset().filter(subject=subject)


    def retrieve(self, request, subject_pk=None, pk=None):
        subject = get_object_or_404(Subject, id=subject_pk)
        material = get_object_or_404(subject.material_set, id=pk)

        serializer = self.get_serializer(material)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request, subject_pk=None):
        subject = get_object_or_404(Subject, id=subject_pk)
        context = {'subject': subject, 'request': request}

        serializer = self.get_serializer_class()(
            context=context, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


    def update(self, request, subject_pk=None, pk=None):
        subject = get_object_or_404(Subject, id=subject_pk)
        material = get_object_or_404(subject.material_set, id=pk)

        if material.author != request.user.teacher:
            return Response(
                {'message': 'You can edit only your own materials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer_class()(
            material, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
            headers=headers
        )


    def destroy(self, request, subject_pk=None, pk=None):
        subject = get_object_or_404(Subject, id=subject_pk)
        material = get_object_or_404(subject.material_set, id=pk)

        if material.author != request.user.teacher:
            return Response(
                {'message': 'You can delete only your own materials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        material.delete()

        return Response(
            {'message': 'Material successfully deleted.'},
            status=status.HTTP_200_OK
        )
