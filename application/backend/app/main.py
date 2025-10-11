"""
Main FastAPI application entry point
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time
from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.db.mongodb import MongoDB

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.APP_ENV}")
    
    # Connect to MongoDB
    await MongoDB.connect_db()
    logger.info("Database connected successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    await MongoDB.close_db()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-level FastAPI backend for Stylic AI cross-platform application",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"] if settings.CORS_ALLOW_METHODS == "*" else settings.CORS_ALLOW_METHODS.split(","),
    allow_headers=["*"] if settings.CORS_ALLOW_HEADERS == "*" else settings.CORS_ALLOW_HEADERS.split(","),
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing"""
    start_time = time.time()
    
    # Log request
    logger.info(
        f"Request started",
        extra={
            "method": request.method,
            "url": str(request.url),
            "client": request.client.host if request.client else None
        }
    )
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Log response
    logger.info(
        f"Request completed",
        extra={
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "duration": f"{duration:.3f}s"
        }
    )
    
    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation error",
            "details": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Import and include routers
# Note: These will be created in the next steps
# from app.api.v1.endpoints import auth, users, photoshoots, payments, credits
# 
# app.include_router(
#     auth.router,
#     prefix=f"{settings.API_V1_PREFIX}/auth",
#     tags=["Authentication"]
# )
# 
# app.include_router(
#     users.router,
#     prefix=f"{settings.API_V1_PREFIX}/users",
#     tags=["Users"]
# )
# 
# app.include_router(
#     photoshoots.router,
#     prefix=f"{settings.API_V1_PREFIX}/photoshoots",
#     tags=["Photoshoots"]
# )
# 
# app.include_router(
#     payments.router,
#     prefix=f"{settings.API_V1_PREFIX}/payments",
#     tags=["Payments"]
# )
# 
# app.include_router(
#     credits.router,
#     prefix=f"{settings.API_V1_PREFIX}/credits",
#     tags=["Credits"]
# )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

