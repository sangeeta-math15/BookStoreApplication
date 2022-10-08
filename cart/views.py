from django.forms import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from book.models import Book
from cart.models import Cart, CartItem
from user.models import User
from book.util import verifying_token


class AddToCart(APIView):

    @verifying_token
    def post(self, request):
        try:
            book = Book.objects.get(id=request.data.get("book"))

            user_obj = User.objects.get(id=request.data.get('user_id'))
            # user = User.objects.get(id=request.data("user"))
            # print(request.data.get("user_id"))
            carts_list = Cart.objects.filter(user=request.data.get("user_id"), status=0)

            if len(carts_list) > 0:

                cart = carts_list.first()
            else:
                cart = Cart.objects.create(user=user_obj)

            books_price = book.price * request.data.get("quantity")
            CartItem.objects.create(price=books_price, quantity=request.data.get("quantity"), book_id=book.id,
                                    user_id=user_obj.id, cart=cart)

            cart_obj = Cart.objects.get(id=cart.id)
            cart_obj.total_price = 0
            cart_obj.total_quantity = 0

            cart_item_list = CartItem.objects.filter(cart_id=cart.id)

            for cart_item in cart_item_list:
                cart_obj.total_price += cart_item.price
                cart_obj.total_quantity += cart_item.quantity
                cart_obj.save()

            return Response({"message": "item added to cart", "data": model_to_dict(cart_obj)},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def get(self, request):
        try:
            cart_obj = Cart.objects.filter(user=request.data.get("user_id"))
            return Response({"message": "Carts retrieved", "data": cart_obj.values()}, status=status.HTTP_200_OK)
        except Exception as e:

            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
