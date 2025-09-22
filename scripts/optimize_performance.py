#!/usr/bin/env python3
"""Performance optimization utilities"""

import time
from functools import wraps

def measure_time(func):
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {(end - start) * 1000:.2f}ms")
        return result
    return wrapper

# TODO: Add caching for frequently accessed data
# TODO: Optimize database queries with indexes
# TODO: Implement request rate limiting
# TODO: Add CDN for static assets
