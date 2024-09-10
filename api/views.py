from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def convert_currency(request, currency1, currency2, amount):
    rates = {
        'USD': {'GBP': 0.8, 'EUR': 0.93},
        'GBP': {'USD': 1.26, 'EUR': 1.17},
        'EUR': {'USD': 1.07, 'GBP': 0.86}
    }
    try:
        amount = float(amount)
        if currency1 in rates and currency2 in rates[currency1]:
            conversion_rate = rates[currency1][currency2]
            converted_amount = amount * conversion_rate
            return Response({'amount': converted_amount}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Currency not supported'}, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)
