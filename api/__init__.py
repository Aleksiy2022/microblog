"""
Package 'api'.

The 'api' package serves as a comprehensive backend solution for interacting
with the provided frontend of the microblog. It offers extensive functionality
for accessing and managing microblog data, ensuring seamless communication
between services.

Components of the package:
1. The 'core' package contains the main configuration of the application.
2. The 'db' package is required for interacting with the database.
3. The 'routers' package is necessary for organizing and structuring the code
that handles route requests.
4. The 'dependencies' module contains dependencies that process data received
by view functions.
5. The 'main' module acts as the central module where the initialization and
configuration of the web server and its components take place.
"""

__all__ = ("settings",)

from .core import settings
