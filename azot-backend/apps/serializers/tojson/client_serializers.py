from rest_framework import serializers
# import apps.serializers.tojson.client_cart_serializer import CartOutSerializer
# import apps.serializers.tojson.seller_serializers import PurchaseSerializer
import apps.serializers.tojson.client_cart_serializer
import apps.serializers.tojson.seller_serializers


class ClientOutSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
        }

    def to_internal_value(self, data):
        return {
            'id': data.get('id'),
            'email': data.get('email'),
        }





class ClientInfoOutSerializer(serializers.Serializer):
    name = serializers.CharField()
    surname = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'surname': instance.surname,
            'phone': instance.phone,
            'address': instance.address,
            'balance': instance.balance,
        }

    def to_internal_value(self, data):
        return {
            'name': data.get('name'),
            'surname': data.get('surname'),
            'phone': data.get('phone'),
            'address': data.get('address'),
            'balance': data.get('balance'),
        }

class ClientOutShortSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    client_info = ClientInfoOutSerializer()

    def to_representation(self, instance):
        return {
            'name': instance.client_info.name,
            'surname': instance.client_info.surname,
        }


class ClientOutWithInfoSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    client_info = ClientInfoOutSerializer()
    cart = apps.serializers.tojson.client_cart_serializer.CartOutSerializer()


    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
            'client_info': ClientInfoOutSerializer().to_representation(instance.client_info),
        }

    def to_internal_value(self, data):
        return {
            'id': data.get('id'),
            'email': data.get('email'),
            'client_info': ClientInfoOutSerializer().to_internal_value(data.get('client_info')),
            'cart': apps.serializers.tojson.client_cart_serializer.CartOutSerializer().to_internal_value(data.get('cart')),
        }