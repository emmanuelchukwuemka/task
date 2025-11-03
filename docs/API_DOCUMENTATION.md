# Task Management API Documentation

## Overview

The Task Management API provides a complete backend solution for managing tasks with user authentication and analytics. It follows RESTful principles and uses JWT for authentication.

## Authentication

All API endpoints (except authentication endpoints) require a valid JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

### Register a New User

**Endpoint**: `POST /api/auth/register`

**Request Body**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response**:
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "role": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
}
```

**Status Codes**:
- `201`: User created successfully
- `400`: Invalid input data
- `409`: Username or email already exists

### Login

**Endpoint**: `POST /api/auth/login`

**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response**:
```json
{
  "message": "Login successful",
  "access_token": "string",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "role": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
}
```

**Status Codes**:
- `200`: Login successful
- `400`: Missing credentials
- `401`: Invalid credentials

### Get User Profile

**Endpoint**: `GET /api/auth/profile`

**Response**:
```json
{
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "role": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
}
```

**Status Codes**:
- `200`: Profile retrieved successfully
- `401`: Unauthorized
- `404`: User not found

### Update User Profile

**Endpoint**: `PUT /api/auth/profile`

**Request Body**:
```json
{
  "username": "string (optional)",
  "email": "string (optional)"
}
```

**Response**:
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "role": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
}
```

**Status Codes**:
- `200`: Profile updated successfully
- `400`: Invalid input data
- `401`: Unauthorized
- `404`: User not found
- `409`: Username or email already exists

## Tasks

### Get All Tasks

**Endpoint**: `GET /api/tasks`

**Query Parameters**:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10, max: 100)
- `status`: Filter by status (pending, in_progress, completed)
- `priority`: Filter by priority (low, medium, high)
- `search`: Search in title and description

**Response**:
```json
{
  "tasks": [
    {
      "id": "integer",
      "title": "string",
      "description": "string",
      "status": "string",
      "priority": "string",
      "due_date": "datetime",
      "created_at": "datetime",
      "updated_at": "datetime",
      "user_id": "integer"
    }
  ],
  "pagination": {
    "page": "integer",
    "pages": "integer",
    "per_page": "integer",
    "total": "integer"
  }
}
```

**Status Codes**:
- `200`: Tasks retrieved successfully
- `401`: Unauthorized

### Create a New Task

**Endpoint**: `POST /api/tasks`

**Request Body**:
```json
{
  "title": "string",
  "description": "string (optional)",
  "status": "string (optional, default: pending)",
  "priority": "string (optional, default: medium)",
  "due_date": "datetime (optional)"
}
```

**Response**:
```json
{
  "message": "Task created successfully",
  "task": {
    "id": "integer",
    "title": "string",
    "description": "string",
    "status": "string",
    "priority": "string",
    "due_date": "datetime",
    "created_at": "datetime",
    "updated_at": "datetime",
    "user_id": "integer"
  }
}
```

**Status Codes**:
- `201`: Task created successfully
- `400`: Invalid input data
- `401`: Unauthorized

### Get a Specific Task

**Endpoint**: `GET /api/tasks/{id}`

**Response**:
```json
{
  "task": {
    "id": "integer",
    "title": "string",
    "description": "string",
    "status": "string",
    "priority": "string",
    "due_date": "datetime",
    "created_at": "datetime",
    "updated_at": "datetime",
    "user_id": "integer"
  }
}
```

**Status Codes**:
- `200`: Task retrieved successfully
- `401`: Unauthorized
- `403`: Access denied (non-admin users can only access their own tasks)
- `404`: Task not found

### Update a Task

**Endpoint**: `PUT /api/tasks/{id}`

**Request Body**:
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "status": "string (optional)",
  "priority": "string (optional)",
  "due_date": "datetime (optional)"
}
```

**Response**:
```json
{
  "message": "Task updated successfully",
  "task": {
    "id": "integer",
    "title": "string",
    "description": "string",
    "status": "string",
    "priority": "string",
    "due_date": "datetime",
    "created_at": "datetime",
    "updated_at": "datetime",
    "user_id": "integer"
  }
}
```

**Status Codes**:
- `200`: Task updated successfully
- `400`: Invalid input data
- `401`: Unauthorized
- `403`: Access denied
- `404`: Task not found

### Delete a Task

**Endpoint**: `DELETE /api/tasks/{id}`

**Response**:
```json
{
  "message": "Task deleted successfully"
}
```

**Status Codes**:
- `200`: Task deleted successfully
- `401`: Unauthorized
- `403`: Access denied
- `404`: Task not found

## Analytics

### Get Task Statistics

**Endpoint**: `GET /api/analytics/statistics`

**Response for Admin Users**:
```json
{
  "statistics": {
    "total_tasks": "integer",
    "completed_tasks": "integer",
    "pending_tasks": "integer",
    "in_progress_tasks": "integer",
    "completion_rate": "float"
  }
}
```

**Response for Regular Users**:
```json
{
  "statistics": {
    "user_id": "integer",
    "total_tasks": "integer",
    "completed_tasks": "integer",
    "pending_tasks": "integer",
    "in_progress_tasks": "integer",
    "completion_rate": "float"
  }
}
```

**Status Codes**:
- `200`: Statistics retrieved successfully
- `401`: Unauthorized

### Get Tasks by Priority

**Endpoint**: `GET /api/analytics/priority`

**Response**:
```json
{
  "priority_stats": {
    "low": "integer",
    "medium": "integer",
    "high": "integer"
  }
}
```

**Status Codes**:
- `200`: Priority statistics retrieved successfully
- `401`: Unauthorized

### Get Tasks by Status

**Endpoint**: `GET /api/analytics/status`

**Response**:
```json
{
  "status_stats": {
    "pending": "integer",
    "in_progress": "integer",
    "completed": "integer"
  }
}
```

**Status Codes**:
- `200`: Status statistics retrieved successfully
- `401`: Unauthorized

## Error Responses

All error responses follow this format:

```json
{
  "message": "Error description"
}
```

For server errors, an additional `error` field may be included:

```json
{
  "message": "Error description",
  "error": "Detailed error information"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. Exceeding the limit will result in a `429 Too Many Requests` response.

## CORS Policy

The API allows cross-origin requests from the frontend domain specified in the configuration.

## Data Validation

All input data is validated on the server side:
- Required fields are checked
- Data types are validated
- String lengths are limited
- Email format is validated
- Password strength is enforced (min 8 characters, uppercase, lowercase, digit)

## Pagination

List endpoints support pagination:
- Default page size: 10 items
- Maximum page size: 100 items
- Page numbers start at 1

## Filtering and Search

List endpoints support filtering and search:
- Filter by status and priority
- Search in title and description
- Combine multiple filters

## Date Format

All dates are in ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`

## Role-Based Access Control

- **Admin users**: Can access all tasks and statistics
- **Regular users**: Can only access their own tasks and personal statistics