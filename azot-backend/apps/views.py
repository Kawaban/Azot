import uuid

from rest_framework import status
from rest_framework.exceptions import ValidationError, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.serializers.tojson.client_serializers import ClientOutSerializer, ClientOutWithInfoSerializer
from apps.serializers.tojson.seller_serializers import ProductOutSerializer
from apps.serializers.fromjson.product_serializers import ProductInSerializer
from apps.serializers.fromjson.client_serializers import ClientInSerializer, ClientInfoInSerializer
from apps.serializers.tojson.seller_serializers import SellerOutSerializer, SellerOutWithInfoSerializer
from apps.serializers.fromjson.seller_serializers import SellerInSerializer, SellerInfoInSerializer
from apps.serializers.fromjson.client_cart_serializer import ClientCartSerializer



from apps.models import Client, Seller, Product, Purchase, Cart

from apps.exceptions import PurchaseError



class ClientRegisterView(APIView):
    def post(self, request):
        client = ClientInSerializer(data=request.data)
        client.is_valid(raise_exception=True)
        instance = client.create(client.validated_data)
        return Response({'content': ClientOutSerializer(instance).data}, status=status.HTTP_200_OK)


class ClientLoginView(APIView):
    def post(self, request):
        client = ClientInSerializer(data=request.data)
        client.is_valid(raise_exception=True)
        instance = Client.objects.get(email=client.validated_data['email'])
        if instance.password == client.validated_data['password']:
            return Response({'content': ClientOutWithInfoSerializer(instance).data}, status=status.HTTP_200_OK)
        else:
            raise NotAuthenticated()

class SellerRegisterView(APIView):
    def post(self, request):
        seller = SellerInSerializer(data=request.data)
        seller.is_valid(raise_exception=True)
        instance = seller.create(seller.validated_data)
        return Response({'content': SellerOutSerializer(instance).data}, status=status.HTTP_200_OK)


class SellerLoginView(APIView):
    def post(self, request):
        seller = SellerInSerializer(data=request.data)
        seller.is_valid(raise_exception=True)
        instance = Seller.objects.get(email=seller.validated_data['email'])
        if instance.password == seller.validated_data['password']:
            return Response({'content': SellerOutWithInfoSerializer(instance).data}, status=status.HTTP_200_OK)
        else:
            raise NotAuthenticated()


class SellerAddProductView(APIView):
    def post(self, request, seller_id):
        seller = Seller.objects.get(id=seller_id)
        product = ProductInSerializer(data=request.data)
        product.is_valid(raise_exception=True)
        product.create(product.validated_data, seller)
        return Response({'content': 'success'}, status=status.HTTP_200_OK)

class GetProductsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        return Response({'content': ProductOutSerializer(products, many=True).data}, status=status.HTTP_200_OK)


class ClientCartView(APIView):
    def put(self, request, client_id):
        client = Client.objects.get(id=client_id)
        cart = ClientCartSerializer(data=request.data)
        cart.is_valid(raise_exception=True)
        cart.update(client.cart, cart.validated_data)
        return Response({'content': 'success'}, status=status.HTTP_200_OK)

    def post(self, request, client_id):
        client = Client.objects.get(id=client_id)
        cart = client.cart
        for order in cart.order_set.all():
            if client.client_info.balance < order.product.price * order.quantity:
                raise PurchaseError()
            if order.product.items_available < order.quantity:
                raise PurchaseError()

            client.client_info.balance -= order.product.price * order.quantity
            client.client_info.save()

            order.product.items_available -= order.quantity
            order.product.save()

            Purchase.objects.create(id=uuid.uuid4(), seller=order.product.owner, product=order.product, quantity=order.quantity, cost=order.product.price * order.quantity)

        cart.orders = None
        cart.save()
        return Response({'content': 'success'}, status=status.HTTP_200_OK)



class ClientChangeInfoView(APIView):
    def put(self, request, client_id):
        client = Client.objects.get(id=client_id)
        client_info = ClientInfoInSerializer(data=request.data)
        client_info.is_valid(raise_exception=True)
        client.client_info = client_info.update(client.client_info, client_info.validated_data)
        return Response({'content': 'success'}, status=status.HTTP_200_OK)

class SellerChangeInfoView(APIView):
    def put(self, request, seller_id):
        seller = Seller.objects.get(id=seller_id)
        seller_info = SellerInfoInSerializer(data=request.data)
        seller_info.is_valid(raise_exception=True)
        seller.seller_info = seller_info.update(seller.seller_info, seller_info.validated_data)
        return Response({'content': 'success'}, status=status.HTTP_200_OK)

    def get(self, request, seller_id):
        seller = Seller.objects.get(id=seller_id)
        return Response({'content': SellerOutWithInfoSerializer(seller).data}, status=status.HTTP_200_OK)


class ClientAddBalanceView(APIView):
    def post(self, request, client_id):
        client = Client.objects.get(id=client_id)
        if request.data['balance'] < 0:
            raise ValidationError()
        client.client_info.balance += request.data['balance']
        client.client_info.save()
        return Response({'content': 'success'}, status=status.HTTP_200_OK)



