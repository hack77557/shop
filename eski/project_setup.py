import os

# Step 1: Organize Apps into an 'apps' folder
# Create an 'apps' directory and move each app inside it.
# Update the settings.py INSTALLED_APPS with the new paths, e.g., 'apps.myapp'.

# Step 2: Generate requirements.txt
# Assuming you are in the virtual environment:
os.system('pip freeze > requirements.txt')

# Step 3: Add Testing Structure
# Create a 'tests' directory or add tests.py in each app.

# Example of tests.py in one app
# File: apps/myapp/tests.py
from django.test import TestCase

class ExampleTest(TestCase):
    def test_example(self):
        self.assertEqual(1 + 1, 2)

# Step 4: Add Documentation
# Create a README.md file with basic instructions.
readme_content = """# Django Shop Project

## Project Setup

1. Navigate to the project directory:
```bash
cd shop
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Run the development server:
```bash
python manage.py runserver
```

## Running Tests

To execute tests, run:
```bash
python manage.py test
```

## Project Structure

- **apps/**: Contains all Django apps.
- **requirements.txt**: Lists all project dependencies.
- **README.md**: Documentation for the project.

"""

with open("README.md", "w") as readme_file:
    readme_file.write(readme_content)

# Step 5: Add Cart Functionality
# Install dj-shop-cart
os.system('pip install dj-shop-cart')

# Add cart functionality to settings.py
cart_settings = """
# Add 'dj_shop_cart' to INSTALLED_APPS in settings.py
INSTALLED_APPS.append('dj_shop_cart')

# Add context processor for cart
TEMPLATES[0]['OPTIONS']['context_processors'].append('dj_shop_cart.context_processors.cart')
"""

with open('shop/settings.py', 'a') as settings_file:
    settings_file.write(cart_settings)

# Ensure the 'apps/myapp' directory exists
os.makedirs('apps/myapp', exist_ok=True)

# Create or append to 'views.py' in 'apps/myapp'
cart_views = """from dj_shop_cart.cart import Cart
from django.shortcuts import get_object_or_404, redirect, render
from apps.myapp.models import Product

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
"""

views_path = 'apps/myapp/views.py'
with open(views_path, 'w') as views_file:  # Use 'w' to create the file if it doesn't exist
    views_file.write(cart_views)

# Create cart template
cart_template = """<h1>Shopping Cart</h1>
<ul>
    {% for item in cart %}
        <li>{{ item.product.name }} - {{ item.quantity }} x {{ item.product.get_price }}</li>
    {% endfor %}
</ul>
<p>Total: {{ cart.total }}</p>
"""

os.makedirs('apps/myapp/templates/cart', exist_ok=True)
with open('apps/myapp/templates/cart/detail.html', 'w') as template_file:
    template_file.write(cart_template)

print("Cart functionality added!")
