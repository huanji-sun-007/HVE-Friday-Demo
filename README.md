# HVE-Friday-Demo

## FastAPI Baseline Server

A production-ready FastAPI baseline server demonstrating modern best practices, clean architecture, and comprehensive API design.

## Features

- ✅ **FastAPI Framework**: Modern, fast, and production-ready
- ✅ **Async/Await**: Asynchronous endpoints for high performance
- ✅ **Pydantic Models**: Strong type validation for requests and responses
- ✅ **Modular Architecture**: Clean separation of concerns (routes, services, models)
- ✅ **Dependency Injection**: Proper DI pattern using FastAPI's `Depends()`
- ✅ **Comprehensive Documentation**: Auto-generated OpenAPI/Swagger docs
- ✅ **CORS Support**: Configurable Cross-Origin Resource Sharing
- ✅ **Security Utilities**: JWT token handling and password hashing
- ✅ **Error Handling**: Consistent HTTP exception handling
- ✅ **Testing Suite**: Complete test coverage with pytest

## Project Structure

```
app/
├── main.py                 # Application entry point
├── api/
│   ├── routes/
│   │   ├── health.py      # Health check endpoint
│   │   └── items.py       # CRUD endpoints for items
│   └── dependencies.py    # Dependency injection
├── models/
│   └── schemas.py         # Pydantic models
├── services/
│   └── item_service.py    # Business logic layer
├── core/
│   ├── config.py          # Configuration settings
│   └── security.py        # Security utilities
└── tests/
    └── test_main.py       # Test suite
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/huanji-sun-007/HVE-Friday-Demo.git
   cd HVE-Friday-Demo
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

### Development Mode (with auto-reload)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or run directly with Python:

```bash
python -m app.main
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The server will start at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### System Endpoints

- `GET /` - Redirects to API documentation
- `GET /api/v1/health` - Health check endpoint

### Item CRUD Endpoints

- `POST /api/v1/items` - Create a new item
- `GET /api/v1/items` - List all items (with pagination)
- `GET /api/v1/items/{item_id}` - Get a specific item
- `PUT /api/v1/items/{item_id}` - Update an item
- `DELETE /api/v1/items/{item_id}` - Delete an item

## Example Usage

### Create an Item

```bash
curl -X POST "http://localhost:8000/api/v1/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Example Item",
    "description": "This is an example",
    "price": 29.99,
    "tax": 2.99
  }'
```

### Get All Items

```bash
curl -X GET "http://localhost:8000/api/v1/items"
```

### Get a Specific Item

```bash
curl -X GET "http://localhost:8000/api/v1/items/1"
```

## Testing

Run the test suite:

```bash
pytest app/tests/ -v
```

Run with coverage:

```bash
pytest app/tests/ --cov=app --cov-report=html
```

## Configuration

Configuration can be customized via environment variables or a `.env` file:

```env
# Application
APP_NAME="FastAPI Baseline Server"
APP_VERSION="1.0.0"
DEBUG=false

# API
API_PREFIX="/api/v1"

# Security
SECRET_KEY="your-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["*"]
```

## Security Features

- JWT token generation and validation
- Password hashing with bcrypt
- Configurable token expiration
- CORS protection
- Input validation with Pydantic

## Best Practices Demonstrated

1. **Type Hints**: Full type annotation throughout
2. **Async/Await**: Asynchronous endpoint handlers
3. **Dependency Injection**: Clean service layer injection
4. **Error Handling**: Explicit HTTP exceptions
5. **Documentation**: Comprehensive docstrings and OpenAPI descriptions
6. **Validation**: Pydantic models with constraints
7. **Testing**: Complete test coverage
8. **Separation of Concerns**: Clear architectural layers

## License

MIT License