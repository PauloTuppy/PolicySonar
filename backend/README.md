# PolicySonar Backend

This is the Python backend for PolicySonar, using only Python standard library modules.

## Configuration

1. Copy `.env.example` to `.env`
2. Update the values in `.env` with your actual credentials

## Running the Server

```bash
python3 backend/main.py
```

The server will start on port 8000.

## API Endpoints

- `GET /api/policies` - Returns list of policies
