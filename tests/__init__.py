"""
Package tests

This package is designed for testing the functionality of the REST API "api". It includes settings,
creation of a fake database, and tests for conducting testing.

Package components:
1. Settings (`conftest`): Settings and configurations for tests, including environment parameters and other
    configuration data.
2. Factories (`factories`): Module for creating a fake database that can be used in tests to isolate the application
    from the real database.
3. Overridden application dependencies (`overrides_dependencies`).
4. Database query tests (`test_db_queries`).
5. Tests for routers and other application components (`test_api`).
"""