"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import gamer
from levelupapi.models.event import Event
from levelupapi.models.game import Game
from levelupapi.models.gamer import Gamer
from rest_framework.decorators import action


class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized event
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle Get requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        # request.query_params is a dictionary of any query parameters that were in the url
        event_game = request.query_params.get('game', None)
        if event_game is not None:
            events = events.filter(game_id=event_game)
        gamer = Gamer.objects.get(user=request.auth.user)
        # Set the `joined` property on every event
        for event in events:
        # Check to see if the gamer is in the attendees list on the event
            event.joined = gamer in event.attendees.all()

               

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns --JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            game=game,
            organizer=gamer
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for an event
        Just like in the retrieve method, we grab the event we want from the database.
        Each of the next lines are setting the fields on event to the values coming from the client,
        like in the create method. After all the fields are set, the changes are saved to the database.

        Returns: 
            Response -- Empty body with 204 status code
            """

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]

        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


# Using the action decorator turns a method into a new route.
# In this case, the action will accept POST methods and because
# detail=True the url will include the pk. Since we need to know which
# event the user wants to sign up for we’ll need to have the pk. The route
# is named after the function. So to call this method the url would be
# http://localhost:8000/events/2/signup

# Just like in the create method, we get the gamer that’s logged in,
# then the event by it’s pk. The ManyToManyField , attendees, on the
# Event model takes care of most of the hard work. The add method on
# attendees creates the relationship between this event and gamer by
# adding the event_id and gamer_id to the join table. The response then
# sends back a 201 status code.


    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Gamer Left Event'}, status=status.HTTP_204_NO_CONTENT)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date',
                  'time', 'organizer', 'attendees', 'joined')
        depth = 2
