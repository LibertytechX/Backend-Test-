from rest_framework import serializers
from products_App.models import Products, Category


class ProductSerializers(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        model =Products
        fields ='__all__'

    
class CartegorySerializers(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        model =Category
        fields =[
            "title"
        ] 




