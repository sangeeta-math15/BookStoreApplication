from django.forms import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from book.models import Book
from cart.models import Cart, CartItem
from book.util import verifying_token
import logging

from cart.serializers import CartSerializer

logging.basicConfig(filename='book_store_app.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


class AddToCart(APIView):

    @verifying_token
    def post(self, request):
        """
        Adds the book to the cart
        """
        try:
            serializer = CartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "item added to cart", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def get(self, request):
        """
        Retrieves the cart data from the database
        """
        try:
            cart_obj = Cart.objects.filter(user_id=request.data.get("user_id"))
            serializer = CartSerializer(cart_obj, many=True)
            return Response({"message": "Carts retrieved", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def delete(self, request):
        """
        Delete the cart
        """
        try:
            cart = Cart.objects.get(user_id_id=request.data.get("user_id"), status=False)

            cart_item_list = CartItem.objects.filter(cart_id=cart.id)
            if len(cart_item_list) > 0:
                for cart_item in cart_item_list:
                    cart_item.delete()
                    return Response({"message": "Cart item deleted"})
            else:
                cart.delete()
                return Response({"message": "Cart deleted"})

        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CheckOut(APIView):
    @verifying_token
    def post(self, request):
        try:
            cart = Cart.objects.get(user_id_id=request.data.get('user_id'), status=False)
            cart.status = True
            cart.save()
            return Response({"message": "stored in the cart", "data": model_to_dict(cart)})
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
