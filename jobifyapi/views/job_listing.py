"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from jobifyapi.models import JobListing, JobType, JobifyUser
from rest_framework.decorators import action


class JobListingView(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        jobify_user = JobifyUser.objects.get(user=request.auth.user)

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `gameTypeId` in the body of the request.
        job_type = JobType.objects.get(pk=request.data["jobTypeId"])

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            # Create a new Python instance of the Game class
            # and set its properties from what was sent in the
            # body of the request from the client.
            job_listing = JobListing.objects.create(
                title=request.data["title"],
                description=request.data["description"],
                wage=request.data["wage"],
                company=jobify_user,
                job_type=job_type,
                url=request.data["jobListingURL"]
            )
            serializer = JobListingSerializer(job_listing, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            job_listing = JobListing.objects.get(pk=pk)
            serializer = JobListingSerializer(job_listing, context={'request': request})
            return Response(serializer.data)
        except JobListing.DoesNotExist as ex:
            return Response({'message': 'Job listing does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        # jobify_user = JobifyUser.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        job_listing = JobListing.objects.get(pk=pk)
        job_listing.title = request.data["title"]
        job_listing.description = request.data["description"]
        job_listing.wage = request.data["wage"]
        job_listing.company = request.data["company"]
        job_listing.job_type = request.data["jobType"]
        job_listing.interested = request.data["interested"]
        job_listing.url = request.data["url"]
        

        job_type = JobType.objects.get(pk=request.data["jobTypeId"])
        job_listing.job_type = job_type
        job_listing.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            job_listing = JobListing.objects.get(pk=pk)
            job_listing.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except JobListing.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database
        job_listings = JobListing.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        job_type = self.request.query_params.get('type', None)
        if job_type is not None:
            job_listings = job_listings.filter(job_type__id=job_type)

        serializer = JobListingSerializer(
            job_listings, many=True, context={'request': request})
        return Response(serializer.data)
    @action(methods=['post', 'delete'], detail=True)
    def signup(self, request, pk=None):
        """Managing users signing up for job listings"""
        # Django uses the `Authorization` header to determine
        # which user is making the request to sign up
        user = JobifyUser.objects.get(user=request.auth.user)

        try:
            # Handle the case if the client specifies a game
            # that doesn't exist
            job_listing = JobListing.objects.get(pk=pk)
        except JobListing.DoesNotExist:
            return Response(
                {'message': 'Job Listing does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # A gamer wants to sign up for an event
        if request.method == "POST":
            try:
                # Using the attendees field on the event makes it simple to add a gamer to the event
                # .add(gamer) will insert into the join table a new row the gamer_id and the event_id
                job_listing.interested.add(user)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})

        # User wants to leave a previously joined job_listing
        elif request.method == "DELETE":
            try:
                # The many to many relationship has a .remove method that removes the user from the attendees list
                # The method deletes the row in the join table that has the user_id and event_id
                job_listing.interested.remove(user)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return Response({'message': ex.args[0]})

class JobListingSerializer(serializers.ModelSerializer):
        """JSON serializer for games

        Arguments:
            serializer type
        """
        class Meta:
            model = JobListing
            fields = ('id', 'title', 'description', 'wage', 'company', 'job_type', 'interested', 'url')
            depth = 1

