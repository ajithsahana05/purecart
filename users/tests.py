from django.test import TestCase

# Create your tests here.

# import stripe
# from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from .models import Orders_info, Order_items, Payments
# from products.models import Products  # Assuming you have a Products model

# stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


# class CreateOrderAndPayment(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         # Step 1: Get order details from the request
#         order_items_data = request.data.get('order_items', [])
#         total_amount = 0

#         order_items = []

#         # Step 2: Calculate total amount and create order items
#         for item in order_items_data:
#             product = Products.objects.get(id=item['product_id'])
#             quantity = item['quantity']
#             price = product.price  # Assuming 'price' is in your Product model
#             total_amount += price * quantity  # Calculate total amount

#             order_item = Order_items(
#                 product_id=product,
#                 quantity=quantity,
#                 price=price,
#             )
#             order_items.append(order_item)

#         # Step 3: Create an order in the Orders_info model
#         order = Orders_info.objects.create(
#             user_id=request.user,
#             total_amount=total_amount,
#             order_status="pending"
#         )

#         # Step 4: Save order items for the created order
#         for order_item in order_items:
#             order_item.order_id = order
#             order_item.save()

#         # Step 5: Create Stripe PaymentIntent
#         try:
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=total_amount * 100,  # Amount in cents
#                 currency='usd',
#                 metadata={'order_id': order.order_id},
#             )

#             # Step 6: Save the payment intent information in the Payments model
#             payment = Payments.objects.create(
#                 order_id=order,
#                 payment_method='Stripe',
#                 transaction_id=payment_intent.id,
#                 payment_status='pending'
#             )

#             return Response({
#                 'client_secret': payment_intent.client_secret,
#                 'order_id': order.order_id,
#             }, status=status.HTTP_200_OK)

#         except stripe.error.StripeError as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class ConfirmPayment(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         # Step 1: Get the payment confirmation details
#         payment_intent_id = request.data.get('payment_intent_id')
#         payment_method_id = request.data.get('payment_method_id')

#         # Step 2: Confirm the payment with Stripe
#         try:
#             # Confirm the payment intent with the payment method
#             payment_intent = stripe.PaymentIntent.confirm(
#                 payment_intent_id,
#                 payment_method=payment_method_id,
#             )

#             # Step 3: Check the payment status
#             if payment_intent.status == 'succeeded':
#                 # Update the payment status in the Payments model
#                 payment = Payments.objects.get(transaction_id=payment_intent.id)
#                 payment.payment_status = 'successful'
#                 payment.save()

#                 # Update the order status
#                 order = Orders_info.objects.get(order_id=payment.metadata['order_id'])
#                 order.order_status = 'paid'
#                 order.save()

#                 return Response({
#                     'status': 'Payment successful',
#                     'order_status': order.order_status,
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)

#         except stripe.error.StripeError as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
