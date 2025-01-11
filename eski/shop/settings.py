
# Add 'dj_shop_cart' to INSTALLED_APPS in settings.py
INSTALLED_APPS.append('dj_shop_cart')

# Add context processor for cart
TEMPLATES[0]['OPTIONS']['context_processors'].append('dj_shop_cart.context_processors.cart')

# Add 'dj_shop_cart' to INSTALLED_APPS in settings.py
INSTALLED_APPS.append('dj_shop_cart')

# Add context processor for cart
TEMPLATES[0]['OPTIONS']['context_processors'].append('dj_shop_cart.context_processors.cart')
