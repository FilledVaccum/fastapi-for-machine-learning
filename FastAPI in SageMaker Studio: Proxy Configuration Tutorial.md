# FastAPI in SageMaker Studio: Proxy Configuration Tutorial

## The Problem

When trying to access FastAPI documentation at:
https://bqgjxpl5jkzt2rn.studio.us-west-2.sagemaker.aws/jupyterlab/default/proxy/8000/docs


You encountered this error:
Failed to load API definition.
Fetch error
Not Found /openapi.json


## Why It Happened

### 1. Server Not Running Initially
The first issue was that no FastAPI server was running on port 8000. When you try to access any URL, there needs to be an active server listening on that port.

### 2. Proxy Path Mismatch
The main issue was a proxy path configuration problem. SageMaker Studio uses a proxy system where:

• **External URL**: https://domain/jupyterlab/default/proxy/8000/docs
• **Internal URL**: http://localhost:8000/docs

When FastAPI generates its OpenAPI specification (/openapi.json), it needs to know about this proxy path to create correct URLs for the Swagger UI.

### 3. How Swagger UI Works
The Swagger UI documentation page loads JavaScript that fetches the API specification from /openapi.json. Without proper proxy configuration, FastAPI generates URLs that don't account for the proxy path, causing the fetch to fail.

## The Resolution

### Step 1: Start the Server
bash
uvicorn main:app --host 0.0.0.0 --port 8000


### Step 2: Add Root Path Configuration
bash
uvicorn main:app --host 0.0.0.0 --port 8000 --root-path /jupyterlab/default/proxy/8000


## Why It Worked

### The --root-path Parameter
The --root-path /jupyterlab/default/proxy/8000 parameter tells FastAPI:

1. Proxy Awareness: "You're running behind a proxy at this path"
2. URL Generation: Generate all URLs with this prefix
3. OpenAPI Spec: Include the correct server URL in the OpenAPI specification

### Before vs After

Before (without --root-path):
json
{
  "openapi": "3.1.0",
  "servers": [{"url": "/"}],
  ...
}


After (with --root-path):
json
{
  "openapi": "3.1.0", 
  "servers": [{"url": "/jupyterlab/default/proxy/8000"}],
  ...
}


### Complete Working Command
bash
uvicorn main:app --host 0.0.0.0 --port 8000 --root-path /jupyterlab/default/proxy/8000


## Key Takeaways

1. Always start your server first before trying to access endpoints
2. Use --root-path when running behind proxies (SageMaker Studio, reverse proxies, etc.)
3. The root path should match your proxy configuration exactly
4. --host 0.0.0.0 allows external connections (required for SageMaker Studio)

This configuration ensures FastAPI generates correct URLs that work with SageMaker Studio's proxy system, allowing the Swagger UI to properly load the API documentation.