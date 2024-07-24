from rest_framework import serializers
from Order_App.models import Order

class OrderSerializers(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        model =Order 
        fields =[
            "Order_id",
            "user",
            "created_at",
            "products"
        ]