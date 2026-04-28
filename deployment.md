## Deployment Instructions

### Prerequisites
- Python 3.8+
- Redis (for Channels, optional for local dev with InMemoryChannelLayer)

### Steps
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables in `.env`:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com
   ```
4. Run migrations: `python manage.py migrate`
5. Collect static files: `python manage.py collectstatic`
6. Start the server:
   - For WSGI: `gunicorn freelancehub.wsgi:application`
   - For ASGI (WebSockets): `daphne freelancehub.asgi:application`

### Platforms
This project is configured for:
- **Render**: Use `Procfile` with `daphne`.
- **Railway**: Automatically detects `Procfile`.
- **PythonAnywhere**: Use WSGI (WebSockets may need extra setup).
