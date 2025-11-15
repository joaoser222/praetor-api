## Middlewares in PraetorAPI

This document explains how middlewares are used in the project, how to create new ones, and how to register them in the application.

### Global Middlewares

Global middlewares are applied to all application routes and are registered in the `main.py` file. They are ideal for cross-cutting functionalities such as logging, CORS handling, performance monitoring, and header manipulation.

In the project, existing middlewares are configured as follows in `main.py`:

```python
# main.py
from core.middlewares.logging import LoggingMiddleware
 
app.add_middleware(CORSMiddleware, ...) # Configures CORS
app.add_middleware(LoggingMiddleware)   # Adds logging middleware
```

**Characteristics:**
- ✅ Automatically applied to all routes
- ✅ Executed in the order they are registered
- ✅ Can intercept requests and responses
- ✅ Can modify headers, add logs, etc.