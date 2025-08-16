# Campus Helper API

A robust backend service built with FastAPI to provide useful information for students in a centralized way. It acts as a digital assistant, exposing structured endpoints for accessing class timetables, bus timings, and canteen menus with secure authentication.

```
Demo Video
```
https://drive.google.com/file/d/1_TuXayMoql2s3THZMxqg11OYWFLw5-JX/view?usp=drive_link

<img width="1581" height="897" alt="image" src="https://github.com/user-attachments/assets/2f9a119b-bccc-471e-a317-8acce6cf339c" />

```
Frontend
```
Live: https://campus-helper-frontend.vercel.app/
Repo: https://github.com/godlykmathews/campus-helper-frontend



## API
https://campus-helper.onrender.com
  - NB: [render loads slow]


## 🚀 Features

- **Class Timetable Management**: View and manage class schedules by day with room assignments
- **Bus Schedule Management**: Access bus timings and routes for campus transportation
- **Canteen Menu Management**: Browse daily menu items with prices and categories
- **User Authentication**: JWT-based authentication with admin and student roles
- **Interactive API Documentation**: Auto-generated Swagger UI and ReDoc
- **Cloud Database**: Production-ready MySQL database hosted on Railway
- **CORS Support**: Ready for frontend integration
- **Data Validation**: Comprehensive input validation with Pydantic

## 🛠 Tech Stack

- **Backend**: FastAPI (Python 3.13)
- **Database**: Railway MySQL (Production) / SQLite (Development)
- **ORM**: SQLAlchemy 1.4
- **Authentication**: JWT tokens with bcrypt password hashing
- **Validation**: Pydantic v1.x
- **Server**: Uvicorn with hot reload
- **Database Driver**: PyMySQL for MySQL connectivity

## 📁 Project Structure

```
CampusHELPER/
├── app/
│   ├── core/
│   │   ├── database.py      # Database configuration & connection
│   │   ├── security.py      # JWT & password hashing
│   │   └── __init__.py
│   ├── models/
│   │   ├── models.py        # SQLAlchemy database models
│   │   └── __init__.py
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── timetable.py     # Class schedule endpoints
│   │   ├── bus.py           # Bus schedule endpoints
│   │   ├── canteen.py       # Canteen menu endpoints
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── user.py          # User Pydantic schemas
│   │   ├── timetable.py     # Timetable Pydantic schemas
│   │   ├── bus.py           # Bus schedule Pydantic schemas
│   │   ├── canteen.py       # Canteen menu Pydantic schemas
│   │   └── __init__.py
│   ├── main.py              # FastAPI application entry point
│   └── __init__.py
├── venv/                    # Python virtual environment
├── .env                     # Environment variables (Railway MySQL)
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
├── run.py                   # Application runner script
├── create_sample_data.py    # Database seeder with sample data
└── readme.md               # Project documentation
```

## ⚡ Quick Start

### 1. Navigate to Project Directory

```powershell
cd "c:\Users\godly\OneDrive\Desktop\CampusHELPER"
```

### 2. Activate Virtual Environment

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows Command Prompt
venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Environment Setup

Your `.env` file is already configured for Railway MySQL:

```env
# Railway MySQL Database
DATABASE_URL=mysql+pymysql://root:aWeICgmNkARSeLQSCMVHihNcwbvnHjQl@yamabiko.proxy.rlwy.net:19601/railway

# JWT Configuration
SECRET_KEY=A5e4ZhKfo_8-kkyT4lJlbUl0v6qargfuERpETizeENLrMREcHLEO18yINZtag6TnjWu1tT8z6VuBh0wr7FMTpg
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Initialize Database with Sample Data

```powershell
python create_sample_data.py
```

### 6. Start the Development Server

```powershell
# Option 1: Using the run script
python run.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Access the API

- **API Base URL**: http://localhost:8000
- **Interactive Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔐 Authentication

### Default Credentials

After running the sample data script:

- **Admin User**: 
  - Username: `admin`
  - Password: `admin123`
  - Permissions: Full CRUD access to all endpoints

- **Student User**: 
  - Username: `student`
  - Password: `student123`
  - Permissions: Read-only access to all endpoints

### Getting Access Token

```bash
curl -X POST "http://localhost:8000/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
```

## 📋 API Endpoints

### Authentication (`/auth`)
- `POST /auth/register` - Register new user
- `POST /auth/token` - Login and get JWT access token
- `GET /auth/me` - Get current user profile

### Timetable (`/timetable`)
- `GET /timetable/{day}` - Get class schedule for specific day
- `GET /timetable/` - Get all timetable entries
- `POST /timetable/` - Create new timetable entry *(admin only)*
- `PUT /timetable/{id}` - Update existing timetable entry *(admin only)*
- `DELETE /timetable/{id}` - Delete timetable entry *(admin only)*

### Bus Schedule (`/bus`)
- `GET /bus/{route}` - Get bus timings for specific route
- `GET /bus/` - Get all bus schedules
- `GET /bus/routes/list` - Get available routes
- `POST /bus/` - Create new bus schedule *(admin only)*
- `PUT /bus/{id}` - Update bus schedule *(admin only)*
- `DELETE /bus/{id}` - Delete bus schedule *(admin only)*

### Canteen Menu (`/canteen`)
- `GET /canteen/{day}` - Get menu for specific day
- `GET /canteen/` - Get all menu items
- `GET /canteen/categories/list` - Get available categories
- `POST /canteen/` - Create new menu item *(admin only)*
- `PUT /canteen/{id}` - Update menu item *(admin only)*
- `DELETE /canteen/{id}` - Delete menu item *(admin only)*

## 💡 Usage Examples

### 1. Login and Get Token

```bash
curl -X POST "http://localhost:8000/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
```

### 2. Get Monday's Class Schedule

```bash
curl -X GET "http://localhost:8000/timetable/monday"
```

### 3. Add New Class (Admin Required)

```bash
curl -X POST "http://localhost:8000/timetable/" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "day": "Monday",
       "time": "14:00-15:00",
       "subject": "Data Structures",
       "room": "Lab 2"
     }'
```

### 4. Get Available Bus Routes

```bash
curl -X GET "http://localhost:8000/bus/routes/list"
```

### 5. Get Monday's Canteen Menu

```bash
curl -X GET "http://localhost:8000/canteen/monday"
```

### 6. Filter Menu by Category

```bash
curl -X GET "http://localhost:8000/canteen/monday?category=lunch"
```

## 🗄️ Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `hashed_password`
- `is_admin` (Boolean)
- `is_active` (Boolean)
- `created_at` (Timestamp)

### Timetables Table
- `id` (Primary Key)
- `day` (Monday-Sunday)
- `time` (HH:MM-HH:MM format)
- `subject` (Class/Course name)
- `room` (Room number/location)
- `created_at` (Timestamp)

### Bus Schedules Table
- `id` (Primary Key)
- `route` (Route description)
- `time` (Departure time)
- `bus_no` (Bus identifier)
- `created_at` (Timestamp)

### Canteen Menus Table
- `id` (Primary Key)
- `day` (Monday-Sunday)
- `item` (Food item name)
- `price` (Price in currency)
- `category` (breakfast/lunch/dinner/snacks)
- `created_at` (Timestamp)

## 🚀 Deployment Options

### Railway Deployment (Current Setup)

Your project is already configured for Railway with:
- Railway MySQL database connection
- Production environment variables
- Secure JWT secret key

To deploy:
1. Push to GitHub repository
2. Connect Railway to your GitHub repo
3. Railway will auto-deploy using your existing configuration

### Manual Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Set production environment variables
export DATABASE_URL="your_production_database_url"
export SECRET_KEY="your_production_secret_key"

# Run with production settings
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 Development

### Running Tests

```powershell
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests (when test files are added)
pytest
```

### Database Management

```powershell
# Reset database with fresh sample data
python create_sample_data.py

# Access Railway MySQL database directly
# Use the connection string from your .env file
```

### Code Quality

```powershell
# Format code with black
pip install black
black app/

# Lint with flake8
pip install flake8
flake8 app/
```

## 🔮 Future Enhancements

- [ ] Search functionality across all endpoints
- [ ] Real-time notifications for schedule changes
- [ ] Mobile app integration with push notifications
- [ ] Analytics dashboard for admin users
- [ ] Redis caching for improved performance
- [ ] Rate limiting and API throttling
- [ ] Email notifications for important updates
- [ ] Bulk data import via CSV/Excel files
- [ ] Multi-language support
- [ ] Advanced filtering and sorting options
- [ ] API versioning
- [ ] Automated testing suite
- [ ] Monitoring and logging integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the [API documentation](http://localhost:8000/docs) for endpoint details
- Review the sample data in `create_sample_data.py` for data format examples

---

**Campus Helper API** - Making campus life easier, one endpoint at a time! 🎓
