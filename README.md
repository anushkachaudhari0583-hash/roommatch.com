# Roommatch Backend API

A Flask-based backend API for the Roommatch roommate matching platform.

## 🚀 Features

- **User Authentication**: JWT-based authentication with registration and login
- **Profile Management**: Complete user profiles with lifestyle preferences
- **AI Matching Algorithm**: Compatibility scoring based on multiple factors
- **Match Management**: Generate, view, and respond to roommate matches
- **Waitlist System**: Join waitlist for early access
- **RESTful API**: Clean, well-documented API endpoints

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "D:\Roommatch Web Page"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   # Copy the example environment file
   copy env_example.txt .env
   
   # Edit .env with your configuration
   # At minimum, change the SECRET_KEY and JWT_SECRET_KEY
   ```

## 🏃‍♂️ Running the Application

1. **Start the Flask development server**
   ```bash
   python app.py
   ```

2. **The API will be available at**
   ```
   http://localhost:5000
   ```

3. **Test the API**
   ```bash
   python test_api.py
   ```

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user

### Profile Management
- `GET /api/profile` - Get user profile
- `POST /api/profile` - Create/update user profile

### Matching
- `GET /api/matches` - Get user's matches
- `POST /api/matches/generate` - Generate new matches
- `POST /api/matches/<id>/respond` - Respond to a match

### General
- `GET /api/health` - Health check
- `POST /api/waitlist` - Join waitlist

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `your-secret-key-change-in-production` |
| `DATABASE_URL` | Database connection string | `sqlite:///roommatch.db` |
| `JWT_SECRET_KEY` | JWT signing key | `jwt-secret-string` |
| `FLASK_ENV` | Flask environment | `development` |

### Database

The application uses SQLAlchemy with SQLite by default. For production, consider using PostgreSQL:

```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://username:password@localhost/roommatch_db
```

## 🧪 Testing

Run the test script to verify all endpoints:

```bash
python test_api.py
```

This will test:
- Health check
- User registration
- User login
- Profile creation
- Match generation
- Waitlist signup

## 🔒 Security Features

- **Password Hashing**: Uses Werkzeug's secure password hashing
- **JWT Authentication**: Secure token-based authentication
- **CORS Protection**: Configurable cross-origin resource sharing
- **Input Validation**: Validates all incoming data
- **SQL Injection Protection**: Uses SQLAlchemy ORM

## 📊 Matching Algorithm

The compatibility scoring considers:

1. **Budget Compatibility (30%)**: Overlapping budget ranges
2. **Lifestyle Factors (40%)**: Cleanliness, social level, noise tolerance
3. **Pet Preferences (10%)**: Pet compatibility
4. **Smoking Preferences (10%)**: Smoking compatibility
5. **Location Preferences (10%)**: Same location preference

## 🚀 Deployment

### Using Gunicorn (Production)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔗 Frontend Integration

The backend is designed to work with the existing HTML/CSS/JS frontend. Update your frontend JavaScript to make API calls:

```javascript
// Example: Register a user
const registerUser = async (userData) => {
    const response = await fetch('http://localhost:5000/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
    });
    return response.json();
};
```

## 📝 API Documentation

### Request/Response Examples

#### Register User
```json
POST /api/auth/register
{
    "email": "user@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890"
}
```

#### Create Profile
```json
POST /api/profile
{
    "age": 25,
    "gender": "Non-binary",
    "occupation": "Software Developer",
    "budget_min": 800,
    "budget_max": 1200,
    "location_preference": "Downtown",
    "cleanliness_level": 4,
    "social_level": 3,
    "noise_tolerance": 3,
    "pet_preference": "yes",
    "smoking_preference": "no",
    "bio": "Looking for a compatible roommate!"
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process using port 5000
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```

2. **Database errors**
   ```bash
   # Delete database file and restart
   rm roommatch.db
   python app.py
   ```

3. **Import errors**
   ```bash
   # Make sure virtual environment is activated
   pip install -r requirements.txt
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support, email hello@roommatch.com or create an issue in the repository.
