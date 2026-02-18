# Social Media Content Generation Backend

A comprehensive backend system for generating social media content using AI, managing campaigns, and analyzing performance.

## Features

- **AI Content Generation**: Generate captions, hashtags, and post ideas using Gemini AI.
- **Campaign Management**: Create, update, and delete marketing campaigns.
- **Content Management**: Manage generated content with approval workflows.
- **User Management**: Authentication and role-based access control.
- **Analytics**: Track content performance and campaign metrics.

## Tech Stack

- **Backend**: Python 3.10+
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **AI Integration**: Google Gemini API
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: Pydantic

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 13 or higher
- Google Gemini API Key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Team1_Social_Media_Content-_Generation_backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory with the following variables:

   ```env
   DATABASE_URL=postgresql://user:password@host:port/dbname
   GEMINI_API_KEY=your_gemini_api_key
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Database Setup**
   Run the database migrations to create the necessary tables:
   ```bash
   alembic upgrade head
   ```

## Usage

### Run the Server

Start the development server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### API Documentation

Interactive API documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Project Structure

```
app/
├── api/                # API endpoints and routers
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   ├── campaigns.py
│   │   │   ├── content.py
│   │   │   ├── analytics.py
│   │   │   └── users.py
│   │   └── api.py
├── core/               # Core configuration and utilities
│   ├── config.py
│   ├── security.py
│   └── database.py
├── models/             # SQLAlchemy database models
├── schemas/            # Pydantic request/response schemas
├── services/           # Business logic and AI integrations
│   ├── gemini_service.py
│   ├── campaign_service.py
│   └── content_service.py
├── migrations/         # Alembic database migrations
├── tests/              # Unit and integration tests
└── main.py             # Application entry point
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/register`: Register a new user
- `POST /api/v1/auth/login`: Login and get access token
- `POST /api/v1/auth/logout`: Logout user
- `POST /api/v1/auth/refresh`: Refresh access token

### Campaigns

- `GET /api/v1/campaigns`: List all campaigns
- `POST /api/v1/campaigns`: Create a new campaign
- `GET /api/v1/campaigns/{id}`: Get campaign details
- `PUT /api/v1/campaigns/{id}`: Update campaign
- `DELETE /api/v1/campaigns/{id}`: Delete campaign

### Content

- `GET /api/v1/content`: List all content
- `POST /api/v1/content`: Create new content
- `GET /api/v1/content/{id}`: Get content details
- `PUT /api/v1/content/{id}`: Update content
- `DELETE /api/v1/content/{id}`: Delete content
- `POST /api/v1/content/generate`: Generate content using AI

### Analytics

- `GET /api/v1/analytics/campaigns`: Campaign analytics
- `GET /api/v1/analytics/content`: Content performance
- `GET /api/v1/analytics/trends`: Trend analysis

## AI Integration

The system uses Google Gemini API for AI-powered content generation. The `gemini_service.py` module handles:

- Generating post ideas
- Creating captions
- Suggesting hashtags
- Analyzing content tone and style

## Testing

Run the test suite using pytest:

```bash
pytest
```

## Deployment

To deploy this application to production:

1. Create a production database
2. Configure environment variables
3. Run database migrations
4. Start the server using a production-ready ASGI server (e.g., Gunicorn + Uvicorn)

Example deployment with Gunicorn:

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b [IP_ADDRESS]:8000
```

## Security

- All API endpoints are protected and require authentication
- JWT tokens are used for authentication
- Password hashing is implemented using bcrypt
- Role-based access control (admin, editor, viewer)

## License

This project is licensed under the MIT License.