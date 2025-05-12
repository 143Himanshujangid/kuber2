import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Data directory
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Static data directory
STATIC_DATA_DIR = DATA_DIR / "static"
STATIC_DATA_DIR.mkdir(exist_ok=True)

# User data directory
USER_DATA_DIR = DATA_DIR / "users"
USER_DATA_DIR.mkdir(exist_ok=True)

# Application settings
APP_SETTINGS = {
    "name": "Kuber Industry Analytics",
    "version": "1.0.0",
    "description": "Advanced Data Visualization Web App for Kuber Industry",
    "theme": {
        "primary_color": "#4CAF50",
        "secondary_color": "#45a049",
        "background_color": "#f5f5f5",
        "text_color": "#333333",
        "font_family": "Arial, sans-serif"
    }
}

# User roles and permissions
USER_ROLES = {
    "admin": {
        "permissions": ["read", "write", "delete", "upload", "download", "manage_users"]
    },
    "analyst": {
        "permissions": ["read", "write", "upload", "download"]
    },
    "viewer": {
        "permissions": ["read", "download"]
    }
}

# File upload settings
UPLOAD_SETTINGS = {
    "allowed_extensions": [".csv", ".xlsx", ".xls"],
    "max_file_size": 10 * 1024 * 1024  # 10MB
}

# Visualization settings
VIZ_SETTINGS = {
    "default_chart_height": 500,
    "default_chart_width": 800,
    "color_palette": "plotly",
    "template": "plotly_white"
}

# Export settings
EXPORT_SETTINGS = {
    "allowed_formats": ["csv", "excel", "png", "pdf"],
    "default_format": "csv"
}

# Session settings
SESSION_SETTINGS = {
    "timeout": 3600,  # 1 hour
    "max_retries": 3
}

# Logging settings
LOGGING_SETTINGS = {
    "log_file": BASE_DIR / "logs" / "app.log",
    "log_level": "INFO",
    "max_file_size": 5 * 1024 * 1024,  # 5MB
    "backup_count": 5
}

# Create necessary directories
for directory in [DATA_DIR, STATIC_DATA_DIR, USER_DATA_DIR, BASE_DIR / "logs"]:
    directory.mkdir(exist_ok=True) 