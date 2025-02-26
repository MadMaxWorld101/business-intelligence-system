"""Shopify connector for fetching store data."""
import shopify
import pandas as pd
from config import SHOPIFY_API_KEY, SHOPIFY_API_SECRET, SHOPIFY_STORE_URL

def initialize_shopify():
    """Initialize Shopify API connection."""
    shop_url = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{SHOPIFY_STORE_URL}/admin"
    shopify.ShopifyResource.set_site(shop_url)
    return shopify

def get_products(limit=50):
    """Get products from Shopify store.
    
    Args:
        limit: Maximum number of products to fetch
        
    Returns:
        Pandas DataFrame with product data
    """
    shopify_api = initialize_shopify()
    
    products = shopify_api.Product.find(limit=limit)
    product_data = []
    
    for product in products:
        product_dict = {
            'id': product.id,
            'title': product.title,
            'vendor': product.vendor,
            'product_type': product.product_type,
            'created_at': product.created_at,
            'updated_at': product.updated_at,
            'published_at': product.published_at,
            'tags': product.tags
        }
        
        # Get variants
        variants = []
        for variant in product.variants:
            variants.append({
                'variant_id': variant.id,
                'price': variant.price,
                'sku': variant.sku,
                'inventory_quantity': variant.inventory_quantity
            })
        
        product_dict['variants'] = variants
        product_data.append(product_dict)
    
    return pd.DataFrame(product_data)

def get_orders(limit=50, status='any'):
    """Get orders from Shopify store.
    
    Args:
        limit: Maximum number of orders to fetch
        status: Order status filter
        
    Returns:
        Pandas DataFrame with order data
    """
    shopify_api = initialize_shopify()
    
    orders = shopify_api.Order.find(limit=limit, status=status)
    order_data = []
    
    for order in orders:
        order_dict = {
            'id': order.id,
            'name': order.name,
            'email': order.email,
            'created_at': order.created_at,
            'processed_at': order.processed_at,
            'total_price': order.total_price,
            'subtotal_price': order.subtotal_price,
            'total_tax': order.total_tax,
            'currency': order.currency,
            'financial_status': order.financial_status,
            'fulfillment_status': order.fulfillment_status
        }
        
        order_data.append(order_dict)
    
    return pd.DataFrame(order_data)