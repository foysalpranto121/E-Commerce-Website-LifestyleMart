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
        
        # Check if admin already exists
        existing_admin = User.query.filter_by(email='admin@lifestylemart.com').first()
        if existing_admin:
            print("✅ Database already initialized!")
            print(f"📊 Current data: {Category.query.count()} categories, {Product.query.count()} products, {User.query.count()} users")
            return
        
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
            Category(name='Men\'s Fashion', description='Trendy clothing and accessories for men'),
            Category(name='Women\'s Fashion', description='Stylish clothing and accessories for women'),
            Category(name='Shoes', description='Footwear collection for all occasions'),
            Category(name='Accessories', description='Fashion accessories to complete your look'),
            Category(name='Beauty & Personal Care', description='Beauty products and personal care items'),
            Category(name='Home & Living', description='Home decor and lifestyle products')
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        
        # Create sample products
        products = [
            {
                'name': 'Premium Cotton T-Shirt',
                'description': 'Premium quality 100% cotton t-shirt. Features a comfortable fit, breathable fabric, and durable stitching. Perfect for everyday wear and available in multiple colors. Machine washable and retains shape after multiple washes.',
                'category_id': 1,
                'price': 1200,
                'stock': 50,
                'brand': 'Fashion Hub',
                'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'is_featured': True
            },
            {
                'name': 'Classic Denim Jeans',
                'description': 'Comfortable and stylish denim jeans made from premium quality cotton denim. Features a classic straight fit, five-pocket styling, and durable construction. Perfect for casual outings and everyday wear.',
                'category_id': 1,
                'price': 2500,
                'stock': 30,
                'brand': 'Denim Co',
                'image': 'https://images.unsplash.com/photo-1542272604-787c3839105e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'is_featured': True
            },
            {
                'name': 'Elegant Summer Dress',
                'description': 'Light and breezy summer dress perfect for warm weather. Made from soft, breathable fabric with a flattering A-line silhouette. Features a beautiful floral print and comfortable fit. Ideal for beach outings, garden parties, and casual summer events.',
                'category_id': 2,
                'price': 1900,
                'stock': 25,
                'brand': 'Elegance',
                'image': 'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'is_featured': True
            },
            {
                'name': 'Red Running Shoes',
                'description': 'Professional running shoes with advanced cushioning technology. Features breathable mesh upper, responsive midsole, and durable rubber outsole for excellent traction. Perfect for daily runs, gym workouts, and athletic activities.',
                'category_id': 3,
                'price': 3500,
                'stock': 40,
                'brand': 'SportMax',
                'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'is_featured': True
            },
            {
                'name': 'Leather Handbag',
                'description': 'Genuine leather handbag with multiple compartments. Features premium quality leather, sturdy handles, and elegant design. Perfect for office, shopping, and everyday use. Includes inner pockets for organization.',
                'category_id': 4,
                'price': 4200,
                'stock': 20,
                'brand': 'Chic Style',
                'image': 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'is_featured': True
            },
            {
                'name': 'Fashion Watch',
                'description': 'Stylish analog watch with genuine leather strap. Features precise quartz movement, water-resistant case, and elegant dial design. Perfect accessory for both casual and formal occasions. Comes with gift box.',
                'category_id': 4,
                'price': 2800,
                'stock': 30,
                'brand': 'TimeStyle',
                'image': 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'is_featured': True
            },
            {
                'name': 'Men\'s Formal Shirt',
                'description': 'Classic formal shirt perfect for business meetings and formal occasions. Made from premium cotton blend with wrinkle-resistant finish. Features a sharp collar, button cuffs, and tailored fit. Available in multiple sizes.',
                'category_id': 1,
                'price': 1800,
                'stock': 35,
                'brand': 'Executive Wear',
                'image': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'is_featured': False
            },
            {
                'name': 'Designer Sunglasses',
                'description': 'Trendy designer sunglasses with UV400 protection. Features lightweight frame, polarized lenses, and comfortable nose pads. Perfect for outdoor activities and adding style to your look.',
                'category_id': 4,
                'price': 1500,
                'stock': 45,
                'brand': 'Vision Style',
                'image': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'is_featured': False
            },
            {
                'name': 'Casual Sneakers',
                'description': 'Comfortable casual sneakers for everyday wear. Features breathable canvas upper, cushioned insole, and flexible rubber sole. Perfect for walking, casual outings, and daily activities.',
                'category_id': 3,
                'price': 2000,
                'stock': 50,
                'brand': 'Urban Step',
                'image': 'https://images.unsplash.com/photo-1560769629-975f1d23c57d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'is_featured': False
            },
            {
                'name': 'Women\'s Blazer',
                'description': 'Professional women\'s blazer for office and formal occasions. Made from premium fabric with tailored fit. Features notched lapels, button closure, and functional pockets. Perfect for completing your professional look.',
                'category_id': 2,
                'price': 3500,
                'stock': 20,
                'brand': 'ProStyle',
                'image': 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'is_featured': False
            },
            {
                'name': 'Leather Wallet',
                'description': 'Genuine leather wallet with multiple card slots and compartments. Features premium quality leather, RFID blocking technology, and compact design. Perfect for everyday use and makes a great gift.',
                'category_id': 4,
                'price': 900,
                'stock': 60,
                'brand': 'Lux Accessories',
                'image': 'https://images.unsplash.com/photo-1627123424574-724758594e93?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'is_featured': False
            },
            {
                'name': 'Maxi Dress',
                'description': 'Elegant maxi dress with flowing silhouette. Made from soft, comfortable fabric with beautiful print. Features a flattering fit and versatile style perfect for parties, weddings, and special occasions.',
                'category_id': 2,
                'price': 3200,
                'stock': 15,
                'brand': 'Glamour',
                'image': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
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
