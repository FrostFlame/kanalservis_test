"""Предсталения приложения web."""
from rest_framework.decorators import api_view
from rest_framework.response import Response

from web.models import Order
from web.serializers import OrderSerializer


@api_view(['GET'])
def main_page(request):
    """Главная страница со списком всех заказов."""
    if request.method == 'GET':
        data = Order.objects.all()

        serializer = OrderSerializer(
            data, context={'request': request}, many=True
        )

        return Response(
            {
                'data': serializer.data,
                'dol_sum': sum([order.price_dol for order in data]),
                'rub_sum': sum([order.price_rub for order in data])
            }
        )
