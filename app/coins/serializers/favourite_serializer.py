from rest_framework import serializers

from coins.models.favourite_model import FavouriteCoin


# Create your serializer(s) here.
class ViewFavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteCoin
        fields = ['username']
        extra_kwargs = {
            'username': {'required': True},
        }


class AddFavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteCoin
        fields = ['username', 'favourite']
        extra_kwargs = {
            'username': {'required': True},
            'favourite': {'required': True}
        }
