"""
Database setup script for LIFESTYLE MART Python eCommerce Platform
"""

from app import app, db, User, Category, Product, Order, OrderItem, Review
from werkzeug.security import generate_password_hash
import random

def create_sample_data():
    """Create sample data for the eCommerce platform"""
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create admin user
        admin = User(
            name='Admin User',
            email='admin@lifestylemart.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        
        # Create sample categories
        categories = [
            Category(name='Men\'s Clothing', description='Fashion for men'),
            Category(name='Women\'s Clothing', description='Fashion for women'),
            Category(name='Shoes', description='Footwear collection'),
            Category(name='Accessories', description='Fashion accessories')
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        
        # Create sample products
        products = [
            {
                'name': 'Classic White Shirt',
                'description': 'Premium quality cotton shirt perfect for any occasion',
                'category_id': 1,
                'price': 1299.99,
                'stock': 50,
                'brand': 'Fashion Hub',
                'is_featured': True
            },
            {
                'name': 'Denim Jeans',
                'description': 'Comfortable and stylish denim jeans',
                'category_id': 1,
                'price': 2499.99,
                'stock': 30,
                'brand': 'Denim Co',
                'is_featured': True
            },
            {
                'name': 'Summer Dress',
                'description': 'Light and breezy summer dress',
                'category_id': 2,
                'price': 1899.99,
                'stock': 25,
                'brand': 'Elegance',
                'is_featured': True
            },
            {
                'name': 'Running Shoes',
                'description': 'Professional running shoes with advanced cushioning',
                'category_id': 3,
                'price': 3499.99,
                'stock': 40,
                'brand': 'SportMax',
                'is_featured': True
            },
            {
                'name': 'Leather Wallet',
                'description': 'Genuine leather wallet with multiple compartments',
                'category_id': 4,
                'price': 899.99,
                'stock': 60,
                'brand': 'Lux Accessories',
                'is_featured': False
            },
            {
                'name': 'Business Suit',
                'description': 'Professional business suit for formal occasions',
                'category_id': 1,
                'price': 8999.99,
                'stock': 15,
                'brand': 'Executive Wear',
                'is_featured': True
            },
            {
                'name': 'Handbag',
                'description': 'Stylish handbag with premium materials',
                'category_id': 4,
                'price': 2799.99,
                'stock': 20,
                'brand': 'Chic Style',
                'is_featured': False
            },
            {
                'name': 'Sneakers',
                'description': 'Casual sneakers for everyday comfort',
                'category_id': 3,
                'price': 1999.99,
                'stock': 45,
                'brand': 'Urban Step',
                'is_featured': False
            }
        ]
        
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        
        # Create sample users
        users = [
            {
                'name': 'John Doe',
                'email': 'john@example.com',
                'password_hash': generate_password_hash('password123'),
                'phone': '01712345678',
                'address': '123 Main St, Dhaka'
            },
            {
                'name': 'Jane Smith',
                'email': 'jane@example.com',
                'password_hash': generate_password_hash('password123'),
                'phone': '01887654321',
                'address': '456 Park Ave, Dhaka'
            }
        ]
        
        for user_data in users:
            user = User(**user_data)
            db.session.add(user)
        
        db.session.commit()
        
        # Create sample reviews
        products_for_reviews = Product.query.limit(5).all()
        users_for_reviews = User.query.limit(3).all()
        
        for product in products_for_reviews:
            for user in users_for_reviews:
                if random.random() > 0.5:  # 50% chance of review
                    review = Review(
                        product_id=product.id,
                        user_id=user.id,
                        rating=random.randint(3, 5),
                        review_text=f"Great product! I really love this {product.name}.",
                        status='approved'
                    )
                    db.session.add(review)
        
        db.session.commit()
        
        print("✅ Sample data created successfully!")
        print(f"📊 Created {Category.query.count()} categories")
        print(f"🛍️ Created {Product.query.count()} products")
        print(f"👥 Created {User.query.count()} users")
        print(f"⭐ Created {Review.query.count()} reviews")
        print("\n🔐 Admin login credentials:")
        print("   Email: admin@lifestylemart.com")
        print("   Password: admin123")

if __name__ == '__main__':
    create_sample_data()
