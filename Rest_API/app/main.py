from fastapi import FastAPI
from .database import Base, engine  # Import database models and engine
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from .routes import api  # Import the API router

# Create all database tables (assuming models are defined in .database)
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI(
    title="Weather API",  # Set a descriptive title for the API
    description="API for accessing weather data and statistics",  # Provide a clear description
    version="1.0.0",  # Set the API version
    swagger_ui_oauth2_redirect_url=None,  # Disable OAuth2 redirect for Swagger UI
    swagger_ui_parameters={"tryItOutEnabled": True},  # Enable the "Try it out" functionality in Swagger UI
    # openapi_url="/api/openapi.json",  # Optional: Customize OpenAPI JSON path
    # docs_url="/api/docs",  # Optional: Customize Swagger UI path
)

# Configure CORS middleware to allow requests from all origins (adjust as needed)
origins = ["*"]  # Allow requests from all origins (change for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow cookies for authenticated requests
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the API router from the `routes.py` module
app.include_router(api.router)

# Define a root endpoint for the API
@app.get("/")
async def root():
    """
    Root endpoint for the Weather API.

    Returns:
        A JSON response with a welcome message.
    """
    return {"message": "Welcome to the Weather API"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # Correct way to specify app