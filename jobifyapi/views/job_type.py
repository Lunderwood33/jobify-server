from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from jobifyapi.models import JobType

class JobTypeView(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            job_type = JobType.objects.get(pk=pk)
            serializer = JobTypeSerializer(job_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        job_types = JobType.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = JobTypeSerializer(
            job_types, many=True, context={'request': request})
        return Response(serializer.data)

class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields =  '__all__' # ('id', 'label')