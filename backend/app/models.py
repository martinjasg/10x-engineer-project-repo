

# ============== Updated with Google-Style Docstrings ==============

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique identifier using UUID4.

    Returns:
        str: A unique string identifier.
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Get the current UTC time.

    Returns:
        datetime: Current time in UTC timezone.
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for prompt attributes.

    Attributes:
        title (str): Title of the prompt.
        content (str): Content body of the prompt.
        description (Optional[str]): Description or summary of the prompt.
        collection_id (Optional[str]): Identifier of the associated collection.
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Model for creating a new prompt, inherits from PromptBase."""
    pass


class PromptUpdate(BaseModel):
    """Model for updating an existing prompt.

    Attributes:
        title (Optional[str]): New title of the prompt.
        content (Optional[str]): New content of the prompt.
        description (Optional[str]): New description of the prompt.
        collection_id (Optional[str]): New collection ID for the prompt.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class Prompt(PromptBase):
    """Detailed prompt model for database retrieval.

    Attributes:
        id (str): Unique identifier for the prompt.
        created_at (datetime): Timestamp of when the prompt was created.
        updated_at (datetime): Timestamp of the last update to the prompt.
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base model for collection attributes.

    Attributes:
        name (str): Name of the collection.
        description (Optional[str]): Description or summary of the collection.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Model for creating a new collection, inherits from CollectionBase."""
    pass


class Collection(CollectionBase):
    """Detailed collection model for database retrieval.

    Attributes:
        id (str): Unique identifier for the collection.
        created_at (datetime): Timestamp of when the collection was created.
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Model for returning a list of prompts in API responses.

    Attributes:
        prompts (List[Prompt]): List of prompt objects.
        total (int): Total number of prompts in the list.
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Model for returning a list of collections in API responses.

    Attributes:
        collections (List[Collection]): List of collection objects.
        total (int): Total number of collections in the list.
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Model for returning health status of the API.

    Attributes:
        status (str): The current health status.
        version (str): The current version of the API.
    """
    status: str
    version: str


