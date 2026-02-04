# LIFESTYLE MART - Python eCommerce Platform

A modern, full-featured eCommerce platform built with Python Flask, HTML, CSS, and JavaScript. This platform focuses on clothing, shoes, and accessories, collaborating with Bangladeshi local brands.

## 🚀 Features

### Frontend Features
- **Modern UI/UX**: Clean, responsive design with Bootstrap 5
- **Product Catalog**: Advanced filtering, sorting, and search
- **Shopping Cart**: JavaScript-based cart management
- **User Authentication**: Secure login, registration, password recovery
- **Order Management**: Complete order tracking and history
- **Product Reviews**: User rating and review system
- **Responsive Design**: Mobile-first approach

### Backend Features (Python Flask)
- **RESTful API**: Clean API endpoints for all operations
- **Database ORM**: SQLAlchemy for database operations
- **User Management**: Role-based access control (admin, user)
- **Order Processing**: Complete order workflow
- **Admin Panel**: Dashboard with statistics
- **Security**: Password hashing, CSRF protection, input validation

### Technical Features
- **Python Backend**: Flask framework with SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: MySQL/MariaDB with SQLAlchemy ORM
- **Authentication**: Flask-Login for session management
- **Forms**: Flask-WTF for form validation
- **Security**: Bcrypt, CSRF tokens, input sanitization

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Flask 2.3.3** - Web framework
- **SQLAlchemy 2.0.21** - Database ORM
- **Flask-Login 0.6.3** - User authentication
- **Flask-WTF 1.1.1** - Form handling
- **Werkzeug 2.3.7** - Security utilities
- **PyMySQL 1.1.0** - MySQL connector
- **bcrypt 4.0.1** - Password hashing

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling with Bootstrap 5
- **JavaScript** - Interactive functionality
- **Bootstrap 5** - UI framework
- **Font Awesome** - Icons

### Database
- **MySQL 5.7+** or **MariaDB 10.2+**

## 📋 Requirements

- Python 3.8 or higher
- MySQL or MariaDB
- Pip package manager

## 🚀 Installation

### 1. Clone/Download the Project
```bash
git clone <repository-url>
cd lifestyle-mart-python
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
1. Create a new database named `ecommerce_db`
2. Update database credentials in `app.py`:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/ecommerce_db'
```

### 5. Initialize Database
```bash
python database_setup.py
```

### 6. Run the Application
```bash
python app.py
```

### 7. Access the Application
- **Website**: `http://localhost:5000`
- **Admin Panel**: `http://localhost:5000/admin`

## 👤 Default Accounts

### Admin Account
- **Email**: `admin@lifestylemart.com`
- **Password**: `admin123`

### Test User Accounts
- **Email**: `john@example.com`
- **Password**: `password123`

- **Email**: `jane@example.com`
- **Password**: `password123`

## 📁 Project Structure

```
lifestyle-mart-python/
├── app.py                  # Main Flask application
├── database_setup.py       # Database initialization script
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── shop.html          # Product listing
│   ├── product.html       # Product details
│   ├── cart.html          # Shopping cart
│   ├── checkout.html      # Checkout process
│   ├── login.html         # User login
│   └── signup.html        # User registration
├── static/                # Static files
│   ├── css/
│   │   └── style.css      # Custom styles
│   └── js/
│       └── main.js         # JavaScript functionality
└── README.md              # This file
```

## 🔧 Configuration

### Database Settings
Update the database URI in `app.py`:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/ecommerce_db'
```

### Environment Variables
Create a `.env` file for sensitive data:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://user:pass@localhost/ecommerce_db
```

## 🎨 Customization

### Colors and Theme
Edit the CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #FF6B35;
    --secondary-color: #2C3E50;
    --accent-color: #E67E22;
}
```

### Adding New Products
Use the admin panel or add directly to the database setup script.

### Custom Pages
Create new HTML templates in the `templates/` folder and add routes in `app.py`.

## 🔒 Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **CSRF Protection**: Flask-WTF provides CSRF tokens
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection
- **Session Security**: Flask-Login handles secure sessions
- **XSS Protection**: Jinja2 auto-escaping prevents XSS attacks

## 📊 Admin Features

The admin panel provides:
- **Dashboard**: Sales statistics and overview
- **User Management**: View and manage customer accounts
- **Product Management**: Add, edit, delete products
- **Order Management**: View orders and update status
- **Category Management**: Organize product categories

## 🛒 eCommerce Features

### Shopping Cart
- JavaScript-based cart management
- Add/remove items
- Update quantities
- Stock validation

### Checkout Process
- Multi-step checkout
- Address management
- Payment method selection
- Order confirmation

### Order Management
- Order tracking
- Status updates
- Order history
- Email notifications (placeholder)

## 📱 Responsive Design

The platform is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- All modern browsers

## 🚀 Performance Optimization

- **Database Indexing**: Optimized queries with proper indexes
- **Static Assets**: Efficient CSS and JavaScript
- **Session Management**: Efficient session handling
- **Caching**: Template caching for better performance

## 🔧 Development Notes

### Code Standards
- Clean, commented Python code
- PEP 8 compliance
- MVC-style architecture
- Error handling and logging

### Database Design
- Normalized database structure
- Foreign key constraints
- Proper indexing
- Data validation

### Security Best Practices
- Input validation
- Output escaping
- Secure password handling
- Session management

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check database credentials in `app.py`
   - Ensure MySQL/MariaDB is running
   - Verify database exists

2. **Import Errors**
   - Activate virtual environment
   - Install all dependencies: `pip install -r requirements.txt`

3. **Port Already in Use**
   - Change port in `app.py`: `app.run(port=5001)`

4. **Template Not Found**
   - Ensure templates folder is in correct location
   - Check template names and paths

## 📞 Support

For support and questions:
- Email: info@lifestylemart.com
- Phone: +880 1234-567890

## 📄 License

This project is for educational and portfolio purposes. Feel free to use and modify according to your needs.

## 🔄 Updates

Version 1.0.0 - Initial Release
- Complete eCommerce platform
- Python Flask backend
- Modern HTML/CSS/JS frontend
- Admin panel
- User authentication
- Shopping cart
- Order management

---

**LIFESTYLE MART** - Your Fashion Destination 🛍️
