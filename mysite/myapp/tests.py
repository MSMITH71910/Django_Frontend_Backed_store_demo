from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, Order, OrderItem

class ECommerceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00,
            description='Test Description',
            stock=10,
            active=True
        )

    def test_cart_functionality(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('add_to_cart', args=[self.product.slug]))
        self.assertEqual(response.status_code, 302)
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.total_price, 10.00)

    def test_order_placement(self):
        self.client.login(username='testuser', password='password123')
        # Add to cart first
        self.client.get(reverse('add_to_cart', args=[self.product.slug]))
        
        # Checkout
        response = self.client.post(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        
        orders = Order.objects.filter(user=self.user)
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders[0].total_amount, 10.00)
        
        # Cart should be empty
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)

    def test_tracking_and_return(self):
        self.client.login(username='testuser', password='password123')
        # Create an order
        initial_stock = self.product.stock
        order = Order.objects.create(user=self.user, total_amount=10.00)
        item = OrderItem.objects.create(order=order, product=self.product, quantity=1, price=10.00)
        
        # Test tracking
        response = self.client.get(reverse('track_package', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Status:')
        
        # Test return/replace page
        response = self.client.get(reverse('return_replace', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reason for return:')
        
        # Test return action
        response = self.client.post(reverse('return_replace', args=[order.id]), {
            'item_id': item.id,
            'action': 'return',
            'reason': 'Bought by mistake'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify stock incremented
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock + 1)
        
        # Verify item deleted
        self.assertFalse(OrderItem.objects.filter(id=item.id).exists())
        
        # Verify order status updated since it was the only item
        order.refresh_from_db()
        self.assertEqual(order.status, 'Returned')

    def test_set_location(self):
        response = self.client.post(reverse('set_location'), {
            'country': 'Canada',
            'state': 'Ontario'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['location']['country'], 'Canada')
        self.assertEqual(self.client.session['location']['state'], 'Ontario')