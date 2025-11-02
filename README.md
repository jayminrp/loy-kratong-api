# Loy Kratong API

API สำหรับลอยกระทงออนไลน์ (Loy Kratong Online API)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or if using a virtual environment:

```bash
# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```

**Note**: Replace with your actual PostgreSQL connection string.

For testing locally, you can use a local PostgreSQL database or a service like:
- [Supabase](https://supabase.com) (free PostgreSQL hosting)
- [Neon](https://neon.tech) (free PostgreSQL hosting)
- [ElephantSQL](https://www.elephantsql.com) (free PostgreSQL hosting)

### 3. Run the API Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or for production:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## Testing the API

### Option 1: FastAPI Interactive Docs (Recommended)

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints interactively in the browser.

### Option 2: Test with cURL

#### Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok"}
```

#### Get All Kratongs
```bash
curl http://localhost:8000/kratong
```

#### Create a Kratong
```bash
curl -X POST http://localhost:8000/kratong \
  -H "Content-Type: application/json" \
  -d '{
    "id": "1234567890",
    "ownerName": "Test User",
    "wishText": "ขอให้มีความสุข",
    "shapeImg": "/kratong1.png",
    "createdAt": 1699123456789
  }'
```

### Option 3: Test with Python

Create a test script `test_api.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

# Test health check
response = requests.get(f"{BASE_URL}/health")
print("Health check:", response.json())

# Test get all kratongs
response = requests.get(f"{BASE_URL}/kratong")
print("All kratongs:", response.json())

# Test create kratong
new_kratong = {
    "id": "1234567890",
    "ownerName": "Test User",
    "wishText": "ขอให้มีความสุข",
    "shapeImg": "/kratong1.png",
    "createdAt": 1699123456789
}
response = requests.post(f"{BASE_URL}/kratong", json=new_kratong)
print("Created kratong:", response.json())
```

Run it:
```bash
pip install requests
python test_api.py
```

## API Endpoints

### GET `/health`
Health check endpoint.

**Response:**
```json
{"status": "ok"}
```

### GET `/kratong`
Get all kratongs.

**Response:**
```json
{
  "kratongs": [
    {
      "id": "1234567890",
      "ownerName": "User Name",
      "wishText": "คำอวยพร",
      "shapeImg": "/kratong1.png",
      "createdAt": 1699123456789
    }
  ]
}
```

### POST `/kratong`
Create a new kratong.

**Request Body:**
```json
{
  "id": "string (unique ID, e.g., Date.now().toString())",
  "ownerName": "string",
  "wishText": "string",
  "shapeImg": "string (path to image)",
  "createdAt": 1234567890
}
```

**Response:**
```json
{
  "id": "1234567890",
  "ownerName": "User Name",
  "wishText": "คำอวยพร",
  "shapeImg": "/kratong1.png",
  "createdAt": 1699123456789
}
```

## CORS Configuration

The API is configured to allow requests from:
- `https://loy-kratong-tse.onrender.com` (production frontend)
- `http://localhost:5173` (local development)
- `http://localhost:3000` (alternative local port)

## Database Schema

The API uses PostgreSQL with the following table:

```sql
CREATE TABLE kratongs (
    id VARCHAR PRIMARY KEY,
    owner_name VARCHAR(100) NOT NULL,
    wish_text TEXT NOT NULL,
    shape_img VARCHAR(255) NOT NULL,
    created_at BIGINT NOT NULL,
    server_time TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

The table will be created automatically when the API starts if it doesn't exist.

## Deployment on Render

### Prerequisites

1. **Python Version**: The project uses Python 3.12. A `runtime.txt` file is included to specify this version.
   - If Render still uses Python 3.13, go to your Render dashboard → Settings → Environment → and manually set Python version to 3.12

2. **Environment Variables**:
   - `DATABASE_URL` - Your PostgreSQL connection string (automatically set if using Render's PostgreSQL service)

### Render Configuration

1. **Build Command** (optional, Render auto-detects):
   ```
   pip install -r requirements.txt
   ```

2. **Start Command**:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Python Version**: 
   - The `runtime.txt` file specifies `python-3.12`
   - If deployment fails with `psycopg2` errors, verify Python 3.12 is selected in Render dashboard

### Troubleshooting

**Issue**: `ImportError: undefined symbol: _PyInterpreterState_Get`
- **Solution**: This was fixed by switching from `psycopg2-binary` to `psycopg` (psycopg3), which supports Python 3.13.
  - The project now uses `psycopg[binary]==3.2.3` in `requirements.txt`
  - Database URL format uses `postgresql+psycopg://` for SQLAlchemy compatibility
  - Works with both Python 3.12 and Python 3.13

