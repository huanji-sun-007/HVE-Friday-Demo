# FastAPI Baseline

A production-ready FastAPI application with best practices, clean architecture, and comprehensive testing.

## Features

- ✅ **Clean Architecture**: Modular structure with separation of concerns
- ✅ **Async by Default**: All endpoints use async/await for better performance
- ✅ **Type Safety**: Full type hints and Pydantic validation
- ✅ **Auto Documentation**: Interactive API docs with Swagger UI and ReDoc
- ✅ **Dependency Injection**: Proper DI pattern for services
- ✅ **Comprehensive Tests**: Unit and integration tests with pytest
- ✅ **CORS Support**: Pre-configured CORS middleware
- ✅ **Error Handling**: Consistent error responses
- ✅ **Input Validation**: Automatic request/response validation

## Project Structure

```
app/
├── main.py                 # Application entry point
├── api/
│   ├── routes/
│   │   ├── health.py      # Health check endpoints
│   │   └── items.py       # Item CRUD endpoints
│   └── dependencies.py     # Dependency injection
├── models/
│   └── schemas.py         # Pydantic models
├── services/
│   └── item_service.py    # Business logic
├── core/
│   └── config.py          # Configuration
└── tests/
    ├── conftest.py        # Test fixtures
    ├── test_api.py        # API integration tests
    ├── test_models.py     # Model validation tests
    └── test_services.py   # Service unit tests
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd HVE-Friday-Demo
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Server

Start the FastAPI development server with auto-reload:

```bash
uvicorn app.main:app --reload
```

Or using Python directly:

```bash
python -m app.main
```

The application will be available at:
- **API**: http://localhost:8000
- **Interactive Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Production Server

For production, use multiple workers:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Running Tests

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app --cov-report=html
```

Run specific test file:

```bash
pytest app/tests/test_api.py
```

Run specific test:

```bash
pytest app/tests/test_api.py::TestItemEndpoints::test_create_item
```

## API Endpoints

### Health Check

- **GET** `/health` - Check application health
- **GET** `/` - Root endpoint with basic info

### Items (CRUD)

- **POST** `/api/v1/items` - Create a new item
- **GET** `/api/v1/items/{item_id}` - Get item by ID
- **GET** `/api/v1/items` - List all items (with pagination and filtering)
- **PUT** `/api/v1/items/{item_id}` - Update an item
- **DELETE** `/api/v1/items/{item_id}` - Delete an item

### Query Parameters for Listing Items

- `skip`: Number of items to skip (default: 0)
- `limit`: Maximum items to return (default: 100, max: 100)
- `min_price`: Filter items with price >= min_price
- `max_price`: Filter items with price <= max_price

## Example Usage

### Create an Item

```bash
curl -X POST "http://localhost:8000/api/v1/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "quantity": 10
  }'
```

### Get All Items

```bash
curl "http://localhost:8000/api/v1/items"
```

### Get Item by ID

```bash
curl "http://localhost:8000/api/v1/items/1"
```

### Update an Item

```bash
curl -X PUT "http://localhost:8000/api/v1/items/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Laptop",
    "price": 899.99
  }'
```

### Delete an Item

```bash
curl -X DELETE "http://localhost:8000/api/v1/items/1"
```

## Configuration

Configuration is managed through `app/core/config.py` using Pydantic Settings.

You can override settings using environment variables or a `.env` file:

```env
PROJECT_NAME=My FastAPI App
VERSION=1.0.0
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=["http://localhost:3000"]
```

## Development

### Adding New Endpoints

1. Create a new router file in `app/api/routes/`
2. Define your endpoints using FastAPI decorators
3. Include the router in `app/main.py`

Example:

```python
# app/api/routes/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def list_users():
    return {"users": []}
```

```python
# app/main.py
from app.api.routes import users

app.include_router(users.router, prefix="/api/v1", tags=["Users"])
```

### Adding Business Logic

1. Create a service class in `app/services/`
2. Implement your business logic methods
3. Use dependency injection in routes

### Adding Models

1. Define Pydantic models in `app/models/schemas.py`
2. Use appropriate validation and constraints
3. Separate request and response models

## Testing Strategy

- **Unit Tests**: Test individual components (models, services)
- **Integration Tests**: Test API endpoints end-to-end
- **Fixtures**: Reusable test data and setup in `conftest.py`

## Best Practices Implemented

1. **Separation of Concerns**: Routes, business logic, and models are separated
2. **Dependency Injection**: Services are injected into routes
3. **Type Hints**: All functions have proper type annotations
4. **Async/Await**: Async handlers for better performance
5. **Error Handling**: Consistent HTTP exceptions
6. **Validation**: Automatic input/output validation with Pydantic
7. **Documentation**: Comprehensive docstrings and API documentation
8. **Testing**: Full test coverage with pytest
9. **Configuration Management**: Environment-based configuration
10. **CORS**: Pre-configured for frontend integration

## Next Steps

Consider adding:

- **Database Integration**: SQLAlchemy, Tortoise ORM, or MongoDB
- **Authentication**: JWT tokens, OAuth2, API keys
- **Authorization**: Role-based access control
- **Logging**: Structured logging with loguru or structlog
- **Monitoring**: Prometheus metrics, Sentry error tracking
- **Caching**: Redis for performance optimization
- **Background Tasks**: Celery for async job processing
- **Rate Limiting**: slowapi for API rate limiting
- **Docker**: Containerization for deployment

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.