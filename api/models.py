"""
Pydantic Models for API Request/Response Schemas

This module defines all the data models used for API request and response schemas.
It includes models for workflows, executions, file operations, and error handling.

Key Models:
    - WorkflowCreateRequest: For creating new workflows
    - WorkflowExecuteRequest: For executing workflows with user input
    - WorkflowResponse: Standard workflow response format
    - WorkflowExecutionResponse: Execution result format
    - File-related models: For file upload/management operations
    - Error models: Standard error response format

Features:
    - Pydantic validation and serialization
    - Type hints and field descriptions
    - Enum-based status management
    - DateTime handling with proper formatting
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum

class WorkflowStatus(str, Enum):
    """
    Enumeration of possible workflow status values.
    
    States:
        CREATED: Workflow has been created but code generation hasn't started
        GENERATING: AI is currently generating code for the workflow
        READY: Code generation complete, workflow ready for execution
        EXECUTING: Workflow is currently being executed
        COMPLETED: Workflow execution completed successfully
        FAILED: Workflow creation or execution failed
    """
    CREATED = "created"
    GENERATING = "generating"
    READY = "ready"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"

class WorkflowCreateRequest(BaseModel):
    """
    Request model for creating a new workflow.
    
    Used when users want to create a workflow from a natural language description.
    The system will generate executable code based on the description and context.
    """
    description: str = Field(..., description="Natural language description of the workflow")
    name: Optional[str] = Field(None, description="Optional name for the workflow")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for code generation")

class WorkflowExecuteRequest(BaseModel):
    """
    Request model for executing an existing workflow.
    
    Contains the user input to process and optional file attachments.
    The workflow will be executed with this input and return results.
    """
    user_input: str = Field(..., description="Input data to process through the workflow")
    attached_file_ids: Optional[List[int]] = Field(None, description="List of file IDs attached to this query")

class WorkflowResponse(BaseModel):
    """
    Standard response model for workflow operations.
    
    Contains all workflow metadata including generated code, status, and timing.
    Used for both creation and retrieval endpoints.
    """
    id: str = Field(..., description="Unique workflow identifier")
    name: Optional[str] = Field(None, description="Workflow name")
    description: str = Field(..., description="Workflow description")
    status: WorkflowStatus = Field(..., description="Current workflow status")
    generated_code: Optional[str] = Field(None, description="Generated Python code")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    error: Optional[str] = Field(None, description="Error message if failed")

class WorkflowExecutionResponse(BaseModel):
    """
    Response model for workflow execution operations.
    
    Contains execution results, status, timing, and any errors that occurred.
    Tracks individual execution instances of workflows.
    """
    workflow_id: str = Field(..., description="Workflow identifier")
    execution_id: str = Field(..., description="Unique execution identifier")
    result: Optional[str] = Field(None, description="Execution result")
    status: str = Field(..., description="Execution status")
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")
    error: Optional[str] = Field(None, description="Error message if failed")
    created_at: datetime = Field(..., description="Execution start timestamp")

class ErrorResponse(BaseModel):
    """
    Standard error response model.
    
    Used for consistent error formatting across all API endpoints.
    Includes timestamp for debugging and optional detailed error information.
    """
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class FileUploadResponse(BaseModel):
    """
    Response model for file upload operations.
    
    Contains file metadata from the Paradigm API after successful upload.
    Files are processed and indexed automatically for use in workflows.
    """
    id: int = Field(..., description="File ID in Paradigm")
    filename: str = Field(..., description="Original filename")
    bytes: int = Field(..., description="File size in bytes")
    status: str = Field(..., description="Processing status")
    created_at: int = Field(..., description="Creation timestamp")
    purpose: str = Field(..., description="File purpose")

class FileInfoResponse(BaseModel):
    """
    Response model for file information requests.
    
    Provides metadata about uploaded files and optionally their content.
    Used to check file status and retrieve file details.
    """
    id: int = Field(..., description="File ID")
    filename: str = Field(..., description="Filename")
    status: str = Field(..., description="Processing status")
    created_at: int = Field(..., description="Creation timestamp")
    purpose: str = Field(..., description="File purpose")
    content: Optional[str] = Field(None, description="File content if requested")

class FileQuestionRequest(BaseModel):
    """
    Request model for asking questions about uploaded files.
    
    Enables users to query specific files using natural language.
    The system will analyze the file content to answer the question.
    """
    question: str = Field(..., description="Question to ask about the file")

class FileQuestionResponse(BaseModel):
    """
    Response model for file question operations.
    
    Contains the AI-generated answer and relevant document chunks.
    Provides both the response and source material for transparency.
    """
    response: str = Field(..., description="Answer to the question")
    chunks: List[Dict[str, Any]] = Field(..., description="Relevant document chunks")

class WorkflowWithFilesRequest(BaseModel):
    """
    Request model for creating workflows that use uploaded files.
    
    Extends basic workflow creation with file attachment capabilities.
    The generated workflow will have access to the specified uploaded files.
    """
    description: str = Field(..., description="Natural language description of the workflow")
    name: Optional[str] = Field(None, description="Optional name for the workflow")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for code generation")
    uploaded_file_ids: Optional[List[int]] = Field(None, description="List of uploaded file IDs to use in workflow")

