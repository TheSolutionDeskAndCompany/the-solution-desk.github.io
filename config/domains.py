"""
Domain configuration for the application.
"""

# Base URL for the application
BASE_URL = "https://thesolutiondesk.ca"

# Allowed hosts (for security)
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "thesolutiondesk.ca",
    "www.thesolutiondesk.ca",
    "thesolutiondesk.onrender.com"  # Keep the Render URL for internal routing
]

# CORS settings (if you have a separate frontend)
CORS_ALLOWED_ORIGINS = [
    "https://thesolutiondesk.ca",
    "https://www.thesolutiondesk.ca"
]

# CSRF trusted origins (for forms)
CSRF_TRUSTED_ORIGINS = [
    "https://thesolutiondesk.ca",
    "https://www.thesolutiondesk.ca"
]

# Session cookie domain
SESSION_COOKIE_DOMAIN = ".thesolutiondesk.ca"  # Note the leading dot for subdomains
CSRF_COOKIE_DOMAIN = ".thesolutiondesk.ca"

# Security headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS settings (uncomment in production)
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
