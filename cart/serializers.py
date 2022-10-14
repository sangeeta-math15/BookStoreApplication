from rest_framework import serializers

from book.models import Book
from cart.models import Cart, CartItem


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['price', 'quantity', 'book']


class CartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField(read_only=True)

    def get_cart_items(self, obj):
        cart_obj = obj.cartitem_set.all()
        return ItemSerializer(cart_obj, many=True).data

    quantity = serializers.IntegerField(write_only=True)
    book = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Book.objects.all())

    class Meta:
        model = Cart
        fields = ['id', 'total_price', 'total_quantity', 'status', 'user_id', 'quantity', 'book', 'cart_items']
        read_only_fields = ['status', 'total_price', 'total_quantity']

    def create(self, validated_data):
        user = validated_data.get('user_id')
        book = validated_data.get('book')
        quantity = validated_data.get('quantity')
        cart, created = Cart.objects.get_or_create(user_id=user, status=False)
        books_price = book.price * quantity
        CartItem.objects.create(price=books_price, quantity=quantity, book_id=book.id,
                                user_id=user, cart=cart)
        cart.total_price = 0
        cart.total_quantity = 0
        cart_item_list = CartItem.objects.filter(cart_id=cart.id)
        for cart_item in cart_item_list:
            cart.total_price += cart_item.price
            cart.total_quantity += cart_item.quantity
            cart.save()
            print(cart_item.quantity)
        return cart
