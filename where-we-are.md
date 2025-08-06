# Where We Are

This document summarizes the current capabilities of the application.

## Application Overview

The application is a FastAPI-based service that provides a REST API for managing and interacting with API specifications.

## Core Features

### 1. API Specification Management

- **CRUD Operations:** The application provides a full set of CRUD (Create, Read, Update, Delete) endpoints to manage API specifications in a database.
  - `POST /apis/`: Create a new API specification.
  - `GET /apis/`: Retrieve a list of all API specifications.
  - `GET /apis/{api_id}`: Retrieve a single API specification by its ID.
- **Database Storage:** API specifications are stored in a database using SQLAlchemy. The application is configured to use a local SQLite database for testing, but can be configured to use PostgreSQL for production.

### 2. OpenAPI Parsing

- **Parse from URL:** The application can parse an OpenAPI (or Swagger) specification from a given URL.
  - `POST /parse?url={url}`: Parses the OpenAPI specification at the given URL and returns the parsed JSON.
- **Caching:** The results of the parsing are cached in Redis to improve performance for repeated requests.

### 3. Schema Inference (Placeholder)

- **Infer from Description:** The application has an endpoint to infer an OpenAPI schema from a textual description of an API.
  - `POST /infer?api_description={description}`: Takes a description and is intended to return a generated OpenAPI schema.
- **Current Status:** This feature is currently a **placeholder**. It does not call an AI service to generate a schema. Instead, it returns a hardcoded, example schema. The necessary `openai` library is included in the project's dependencies, but the implementation is not yet complete.

### 4. Health Check

- **`/health` endpoint:** A simple endpoint to verify that the service is running.

## Technology Stack

- **Backend Framework:** FastAPI
- **Database:** SQLAlchemy (with SQLite for testing and `psycopg2` for PostgreSQL support)
- **Caching:** Redis
- **API Parsing:** `prance`
- **Testing:** `pytest`, `fakeredis`

## Next Steps

The immediate next step would be to implement the schema inference functionality using the OpenAI API. The existing code provides a clear starting point for this work.
