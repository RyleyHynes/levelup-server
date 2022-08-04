"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game
from levelupapi.models.game_type import GameType
from levelupapi.models.gamer import Gamer


class GameView(ViewSet):
    """Level up game view"""

    def retrieve(self, request, pk):
        """Handle Get requests for single game

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle Get requests to all the game types
        Returns:
            Response -- JSON serialized list of games
            """
        games = Game.objects.all()
        # request.query_params is a dictionary of any query parameters that were in the url
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
            """
        # Getting the gamer that is logged in.The request will get the user object based on that token
        gamer = Gamer.objects.get(user=request.auth.user)
        # retrieve the GameType object from the database. Makes sure the game type the user is trying
        # to add the new game actually exists in the database.
        # data passed in from the client is held in the request.data dictionary
        game_type = GameType.objects.get(pk=request.data["game_type"])

        # To add the game to the database, we call the create ORM method and pass the fields as
        # parameters to the function
        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            number_of_players=request.data["number_of_players"],
            skill_level=request.data["skill_level"],
            gamer=gamer,
            game_type=game_type
        )
        # After the create has finished the game variable is now the new game instance,
        # including the new id. That object can be serialized and returned to the client now just
        # like in the retrieve method
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a game
        Just like in the retrieve method, we grab the Game object we want from the database. 
        Each of the next lines are setting the fields on game to the values coming from the client, 
        like in the create method. After all the fields are set, the changes are saved to the database.

        Returns:
            Response-- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["number_of_players"]
        game.skill_level = request.data["skill_level"]

        game_type = GameType.objects.get(pk=request.data["game_type"])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        fields = ('id', 'game_type', 'title', 'maker',
                  'gamer', 'number_of_players', 'skill_level')
        depth = 1
