"""
LIFESTYLE MART - Python eCommerce Platform
Main Flask application
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FloatField, SelectField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import secrets
from functools import wraps

# Configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ecommerce.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    role = db.Column(db.Enum('user', 'admin', 'seller'), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image = db.Column(db.String(255))
    brand = db.Column(db.String(100))
    is_featured = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum('active', 'inactive'), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True)

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum('pending', 'processing', 'shipped', 'delivered', 'cancelled'), default='pending')
    payment_method = db.Column(db.Enum('cod', 'bkash', 'nagad', 'card', 'gift_card'), default='cod')
    payment_status = db.Column(db.Enum('pending', 'paid', 'failed'), default='pending')
    shipping_address = db.Column(db.Text, nullable=False)
    billing_address = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    # New fields for enhanced features
    delivery_type = db.Column(db.Enum('standard', 'express'), default='standard')
    gift_card_code = db.Column(db.String(50))
    gift_card_amount = db.Column(db.Float, default=0)
    tracking_number = db.Column(db.String(100))
    courier_name = db.Column(db.String(100))
    estimated_delivery = db.Column(db.DateTime)
    actual_delivery = db.Column(db.DateTime)
    delivery_notes = db.Column(db.Text)
    order_review = db.Column(db.Text)
    order_rating = db.Column(db.Integer)  # 1-5 stars for overall order experience
    is_gift = db.Column(db.Boolean, default=False)
    gift_message = db.Column(db.Text)
    gift_wrap = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text)
    status = db.Column(db.Enum('approved', 'pending', 'rejected'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class SignupForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone Number')
    address = TextAreaField('Address')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description')
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    brand = StringField('Brand')
    image = StringField('Image URL')
    is_featured = BooleanField('Featured Product')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', 
                         choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')],
                         coerce=int, validators=[DataRequired()])
    review_text = TextAreaField('Your Review', validators=[DataRequired(), Length(min=10, max=500)])

class PaymentForm(FlaskForm):
    payment_method = SelectField('Payment Method',
                                choices=[('cod', 'Cash on Delivery'),
                                        ('bkash', 'bKash'),
                                        ('nagad', 'Nagad'),
                                        ('card', 'Credit/Debit Card'),
                                        ('gift_card', 'Gift Card')],
                                validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=11, max=11)])
    transaction_id = StringField('Transaction ID (for bKash/Nagad)')
    card_number = StringField('Card Number')
    card_expiry = StringField('Expiry Date (MM/YY)')
    card_cvv = StringField('CVV')
    gift_card_code = StringField('Gift Card Code')

class OrderTrackingForm(FlaskForm):
    tracking_number = StringField('Tracking Number', validators=[DataRequired()])
    courier_name = SelectField('Courier Service',
                               choices=[('pathao', 'Pathao'),
                                       ('redx', 'RedX'),
                                       ('steadfast', 'Steadfast'),
                                       ('ecourier', 'eCourier'),
                                       ('other', 'Other')],
                               validators=[DataRequired()])
    estimated_delivery = DateField('Estimated Delivery', format='%Y-%m-%d')
    delivery_notes = TextAreaField('Delivery Notes')

class OrderReviewForm(FlaskForm):
    order_rating = SelectField('Order Rating',
                               choices=[(5, '5 Stars - Excellent'),
                                       (4, '4 Stars - Very Good'),
                                       (3, '3 Stars - Good'),
                                       (2, '2 Stars - Fair'),
                                       (1, '1 Star - Poor')],
                               coerce=int, validators=[DataRequired()])
    order_review = TextAreaField('Order Review', validators=[DataRequired(), Length(min=10, max=500)])

class GiftCardForm(FlaskForm):
    gift_card_code = StringField('Gift Card Code', validators=[DataRequired(), Length(min=8, max=50)])
    gift_message = TextAreaField('Gift Message')
    gift_wrap = BooleanField('Gift Wrapping (+৳50)')

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper functions
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def generate_order_number():
    return f"LSM{datetime.now().strftime('%Y%m%d')}{secrets.randbelow(10000):04d}"

# Routes
@app.route('/')
def index():
    products = Product.query.filter_by(is_featured=True, status='active').limit(8).all()
    categories = Category.query.limit(6).all()
    return render_template('index.html', products=products, categories=categories)

@app.route('/shop')
def shop():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'name')
    
    query = Product.query.filter_by(status='active')
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(Product.name.contains(search) | Product.description.contains(search))
    
    if sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort == 'newest':
        query = query.order_by(Product.created_at.desc())
    else:
        query = query.order_by(Product.name.asc())
    
    products = query.paginate(page=page, per_page=12, error_out=False)
    categories = Category.query.all()
    
    return render_template('shop.html', products=products, categories=categories, 
                         category_id=category_id, search=search, sort=sort)

@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    if product.status != 'active':
        return redirect(url_for('shop'))
    
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.status == 'active'
    ).limit(4).all()
    
    reviews = Review.query.filter_by(product_id=id, status='approved').order_by(Review.created_at.desc()).all()
    
    return render_template('product.html', product=product, related_products=related_products, reviews=reviews)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', 'danger')
            return render_template('signup.html', form=form)
        
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    # Get user's orders
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).limit(10).all()
    return render_template('profile.html', orders=orders)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    
    if name:
        current_user.name = name
    if phone:
        current_user.phone = phone
    if address:
        current_user.address = address
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    products = []
    total = 0
    
    for product_id, quantity in cart_items.items():
        product = Product.query.get(int(product_id))
        if product and product.status == 'active':
            subtotal = product.price * quantity
            total += subtotal
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
    
    return render_template('cart.html', products=products, total=total)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    product = Product.query.get_or_404(product_id)
    if product.stock < quantity:
        return jsonify({'success': False, 'message': 'Not enough stock available'})
    
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    session['cart'] = cart
    
    return jsonify({
        'success': True, 
        'message': 'Product added to cart',
        'cart_count': sum(cart.values())
    })

@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 0))
    
    cart = session.get('cart', {})
    
    if quantity > 0:
        product = Product.query.get(product_id)
        if product and product.stock >= quantity:
            cart[product_id] = quantity
        else:
            return jsonify({'success': False, 'message': 'Not enough stock available'})
    else:
        cart.pop(product_id, None)
    
    session['cart'] = cart
    
    return jsonify({
        'success': True,
        'cart_count': sum(cart.values())
    })

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')
    cart = session.get('cart', {})
    cart.pop(product_id, None)
    session['cart'] = cart
    
    return jsonify({
        'success': True,
        'cart_count': sum(cart.values())
    })

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('shop'))
    
    form = PaymentForm()
    
    if request.method == 'POST':
        form = PaymentForm(request.form)
        if form.validate_on_submit():
            # Process order
            order_number = generate_order_number()
            total_amount = 0
            order_items = []
            
            for product_id, quantity in cart.items():
                product = Product.query.get(product_id)
                if product and product.stock >= quantity:
                    subtotal = product.price * quantity
                    total_amount += subtotal
                    order_items.append({
                        'product_id': product_id,
                        'quantity': quantity,
                        'price': product.price,
                        'total': subtotal
                    })
                    # Update stock
                    product.stock -= quantity
            
            if not order_items:
                flash('No valid products in cart', 'danger')
                return redirect(url_for('cart'))
            
            # Create order with enhanced features
            delivery_type = request.form.get('delivery_type', 'standard')
            is_gift = request.form.get('is_gift') == 'on'
            gift_wrap = request.form.get('gift_wrap') == 'on'
            
            # Calculate gift card discount
            gift_card_amount = 0
            if form.payment_method.data == 'gift_card' and form.gift_card_code.data:
                # Simple gift card validation (in real app, this would check against database)
                gift_card_amount = min(500, total_amount * 0.1)  # 10% discount up to ৳500
            
            # Calculate delivery cost
            delivery_cost = 0
            if delivery_type == 'express':
                delivery_cost = 100  # Express delivery fee
            elif is_gift and gift_wrap:
                delivery_cost += 50   # Gift wrapping fee
            
            final_total = total_amount - gift_card_amount + delivery_cost
            
            order = Order(
                user_id=current_user.id,
                order_number=order_number,
                total_amount=final_total,
                shipping_address=request.form.get('shipping_address'),
                billing_address=request.form.get('billing_address') or request.form.get('shipping_address'),
                payment_method=form.payment_method.data,
                payment_status='paid' if form.payment_method.data != 'cod' else 'pending',
                notes=request.form.get('notes'),
                delivery_type=delivery_type,
                gift_card_code=form.gift_card_code.data,
                gift_card_amount=gift_card_amount,
                is_gift=is_gift,
                gift_message=request.form.get('gift_message'),
                gift_wrap=gift_wrap,
                estimated_delivery=datetime.utcnow + (timedelta(days=1) if delivery_type == 'express' else timedelta(days=3))
            )
            db.session.add(order)
            db.session.flush()
            
            # Add order items
            for item in order_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    price=item['price'],
                    total=item['total']
                )
                db.session.add(order_item)
            
            db.session.commit()
            
            # Clear cart
            session['cart'] = {}
            
            flash(f'Order {order_number} placed successfully!', 'success')
            return redirect(url_for('order_confirmation', id=order.id))
    
    # Calculate total for display
    total = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            total += product.price * quantity
    
    return render_template('checkout.html', form=form, total=total, cart_items=len(cart))

@app.route('/add_review/<int:product_id>', methods=['POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    form = ReviewForm(request.form)
    
    if form.validate_on_submit():
        # Check if user already reviewed this product
        existing_review = Review.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        if existing_review:
            flash('You have already reviewed this product', 'warning')
            return redirect(url_for('product_detail', id=product_id))
        
        review = Review(
            product_id=product_id,
            user_id=current_user.id,
            rating=form.rating.data,
            review_text=form.review_text.data,
            status='approved'  # Auto-approve for demo
        )
        db.session.add(review)
        db.session.commit()
        
        flash('Review submitted successfully!', 'success')
    
    return redirect(url_for('product_detail', id=product_id))

@app.route('/order_confirmation/<int:id>')
@login_required
def order_confirmation(id):
    order = Order.query.get_or_404(id)
    if order.user_id != current_user.id:
        return redirect(url_for('index'))
    
    return render_template('order_confirmation.html', order=order)

# Admin routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_products=total_products,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders)

@app.route('/admin/products')
@admin_required
def admin_products():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Product.query
    if search:
        query = query.filter(Product.name.contains(search))
    
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/products.html', products=products, search=search)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            category_id=form.category_id.data,
            price=form.price.data,
            stock=form.stock.data,
            brand=form.brand.data,
            image=form.image.data,
            is_featured=form.is_featured.data
        )
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/product_form.html', form=form, title='Add Product')

@app.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.category_id = form.category_id.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.brand = form.brand.data
        product.image = form.image.data
        product.is_featured = form.is_featured.data
        
        db.session.commit()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/product_form.html', form=form, product=product, title='Edit Product')

@app.route('/admin/products/delete/<int:id>')
@admin_required
def admin_delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@admin_required
def admin_orders():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Order.query
    if status:
        query = query.filter(Order.status == status)
    
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/orders.html', orders=orders, status=status)

@app.route('/admin/orders/<int:id>')
@admin_required
def admin_order_detail(id):
    order = Order.query.get_or_404(id)
    return render_template('admin/order_detail.html', order=order)

@app.route('/admin/orders/update_status/<int:id>', methods=['POST'])
@admin_required
def admin_update_order_status(id):
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        
        # Set actual delivery time if delivered
        if new_status == 'delivered':
            order.actual_delivery = datetime.utcnow()
        
        db.session.commit()
        
        flash('Order status updated successfully!', 'success')
    else:
        flash('Invalid status!', 'danger')
    
    return redirect(url_for('admin_order_detail', id=id))

@app.route('/admin/orders/<int:id>/tracking', methods=['GET', 'POST'])
@admin_required
def admin_order_tracking(id):
    order = Order.query.get_or_404(id)
    form = OrderTrackingForm(obj=order)
    
    if form.validate_on_submit():
        order.tracking_number = form.tracking_number.data
        order.courier_name = form.courier_name.data
        order.estimated_delivery = form.estimated_delivery.data
        order.delivery_notes = form.delivery_notes.data
        
        db.session.commit()
        flash('Tracking information updated successfully!', 'success')
        return redirect(url_for('admin_order_detail', id=id))
    
    return render_template('admin/order_tracking.html', order=order, form=form)

@app.route('/admin/orders/<int:id>/review', methods=['GET', 'POST'])
@admin_required
def admin_order_review(id):
    order = Order.query.get_or_404(id)
    form = OrderReviewForm(obj=order)
    
    if form.validate_on_submit():
        order.order_rating = form.order_rating.data
        order.order_review = form.order_review.data
        
        db.session.commit()
        flash('Order review added successfully!', 'success')
        return redirect(url_for('admin_order_detail', id=id))
    
    return render_template('admin/order_review.html', order=order, form=form)

@app.route('/track-order')
def track_order():
    tracking_number = request.args.get('tracking_number')
    order = None
    
    if tracking_number:
        order = Order.query.filter_by(tracking_number=tracking_number).first()
    
    return render_template('track_order.html', order=order, tracking_number=tracking_number)

@app.route('/admin/users')
@admin_required
def admin_users():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    if search:
        query = query.filter(User.name.contains(search) | User.email.contains(search))
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/users.html', users=users, search=search)

@app.route('/admin/users/<int:id>')
@admin_required
def admin_user_detail(id):
    user = User.query.get_or_404(id)
    return render_template('admin/user_detail.html', user=user)

@app.route('/admin/users/<int:id>/toggle_role', methods=['POST'])
@admin_required
def admin_toggle_user_role(id):
    user = User.query.get_or_404(id)
    
    # Prevent changing own role
    if user.id == current_user.id:
        flash('You cannot change your own role!', 'danger')
        return redirect(url_for('admin_users'))
    
    new_role = request.form.get('role')
    if new_role in ['admin', 'user', 'seller']:
        user.role = new_role
        db.session.commit()
        
        flash(f'User role changed to {new_role} successfully!', 'success')
    else:
        flash('Invalid role!', 'danger')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/categories')
@admin_required
def admin_categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/categories/add', methods=['GET', 'POST'])
@admin_required
def admin_add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if name:
            category = Category(name=name, description=description)
            db.session.add(category)
            db.session.commit()
            
            flash('Category added successfully!', 'success')
            return redirect(url_for('admin_categories'))
        else:
            flash('Category name is required!', 'danger')
    
    return render_template('admin/category_form.html', title='Add Category')

@app.route('/admin/categories/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_category(id):
    category = Category.query.get_or_404(id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if name:
            category.name = name
            category.description = description
            db.session.commit()
            
            flash('Category updated successfully!', 'success')
            return redirect(url_for('admin_categories'))
        else:
            flash('Category name is required!', 'danger')
    
    return render_template('admin/category_form.html', category=category, title='Edit Category')

@app.route('/admin/categories/delete/<int:id>')
@admin_required
def admin_delete_category(id):
    category = Category.query.get_or_404(id)
    
    # Check if category has products
    if category.products:
        flash('Cannot delete category with products!', 'danger')
        return redirect(url_for('admin_categories'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/reviews')
@admin_required
def admin_reviews():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Review.query
    if status:
        query = query.filter(Review.status == status)
    
    reviews = query.order_by(Review.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/reviews.html', reviews=reviews, status=status)

@app.route('/admin/reviews/approve/<int:id>')
@admin_required
def admin_approve_review(id):
    review = Review.query.get_or_404(id)
    review.status = 'approved'
    db.session.commit()
    
    flash('Review approved successfully!', 'success')
    return redirect(url_for('admin_reviews'))

@app.route('/admin/reviews/reject/<int:id>')
@admin_required
def admin_reject_review(id):
    review = Review.query.get_or_404(id)
    review.status = 'rejected'
    db.session.commit()
    
    flash('Review rejected successfully!', 'success')
    return redirect(url_for('admin_reviews'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Create database tables
created = False

@app.before_request
def create_tables():
    global created
    if not created:
        db.create_all()
        created = True

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
