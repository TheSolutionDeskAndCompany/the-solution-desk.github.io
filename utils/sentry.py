"""
Sentry integration for error monitoring in production
"""
import os
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

logger = logging.getLogger(__name__)

def init_sentry(app):
    """
    Initialize Sentry SDK if configured in environment
    """
    dsn = os.environ.get('SENTRY_DSN')
    environment = os.environ.get('FLASK_ENV', 'development')
    
    if not dsn:
        logger.info("Sentry DSN not configured, skipping Sentry initialization")
        return
    
    # Only enable Sentry in production by default
    if environment != 'production' and not os.environ.get('SENTRY_ENABLE_DEV', False):
        logger.info(f"Sentry disabled in {environment} environment")
        return
    
    logger.info(f"Initializing Sentry in {environment} environment")
    
    # Initialize Sentry with Flask and SQLAlchemy integrations
    sentry_sdk.init(
        dsn=dsn,
        integrations=[
            FlaskIntegration(),
            SqlalchemyIntegration(),
        ],
        
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # Adjust this in production as needed.
        traces_sample_rate=float(os.environ.get('SENTRY_SAMPLE_RATE', '0.2')),
        
        # Configure environment
        environment=environment,
        
        # Enable performance monitoring
        enable_tracing=True,
        
        # By default, send release info if available
        release=os.environ.get('SENTRY_RELEASE'),
        
        # Don't include local variables in stack traces by default
        # to avoid potentially exposing sensitive information
        include_local_variables=False,
    )
    
    # Test that Sentry is working
    if os.environ.get('SENTRY_TEST', False):
        logger.info("Testing Sentry integration with a test exception")
        try:
            1 / 0
        except Exception as e:
            sentry_sdk.capture_exception(e)
