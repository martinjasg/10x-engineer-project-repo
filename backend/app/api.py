

# ============== Updated with Google-Style Docstrings ==============

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import filter_prompts_by_collection, search_prompts
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Check the health status of the API.

    Returns:
        HealthResponse: Contains the status and version information.
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
) -> PromptList:
    """Retrieve a list of prompts with optional filtering by collection and search query.

    Args:
        collection_id (Optional[str]): The ID of a collection to filter prompts.
        search (Optional[str]): Search term to filter prompts by title or content.

    Returns:
        PromptList: A list of prompts and total count.
    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str) -> Prompt:
    """Retrieve a prompt by its ID.

    Args:
        prompt_id (str): The unique ID of the prompt.

    Returns:
        Prompt: The prompt object if found.

    Raises:
        HTTPException: If the prompt is not found.
    """
    prompt = storage.get_prompt(prompt_id)
    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate) -> Prompt:
    """Create a new prompt.

    Args:
        prompt_data (PromptCreate): The data required to create a new prompt.

    Returns:
        Prompt: The created prompt object.

    Raises:
        HTTPException: If the collection does not exist.
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate) -> Prompt:
    """Update an existing prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (PromptUpdate): The new data to update the prompt with.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt or the collection does not exist.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # Update and set the updated_at timestamp
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptUpdate) -> Prompt:
    """Partially update a prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (PromptUpdate): The data to update the prompt with.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt is not found.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Update only provided fields
    updated_fields = prompt_data.dict(exclude_unset=True)
    updated_prompt_data = existing.copy(update=updated_fields)
    
    # Save changes with updated timestamp
    updated_prompt = updated_prompt_data.copy(update={"updated_at": get_current_time()})
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str) -> None:
    """Delete a prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to delete.

    Raises:
        HTTPException: If the prompt is not found.
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections() -> CollectionList:
    """Retrieve a list of all collections.

    Returns:
        CollectionList: A list of collection objects and total count.
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str) -> Collection:
    """Retrieve a collection by its ID.

    Args:
        collection_id (str): The unique ID of the collection.

    Returns:
        Collection: The collection object if found.

    Raises:
        HTTPException: If the collection is not found.
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate) -> Collection:
    """Create a new collection.

    Args:
        collection_data (CollectionCreate): The data required to create a new collection.

    Returns:
        Collection: The created collection object.
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str) -> None:
    """Delete a collection by its ID and manage related prompts.

    Args:
        collection_id (str): The ID of the collection to delete.

    Non-existence raises:
        HTTPException: If the collection is not found.

    Side Effects:
        Disassociates prompts from deleted collection and updates timestamps.
    """
    # Check if collection exists before deletion
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Retrieve and update prompts associated with this collection
    prompts_with_collection = storage.get_prompts_by_collection(collection_id)
    for prompt in prompts_with_collection:
        updated_prompt = Prompt(
            id=prompt.id,
            title=prompt.title,
            content=prompt.content,
            description=prompt.description,
            collection_id=None,  # Disassociate from the deleted collection
            created_at=prompt.created_at,
            updated_at=get_current_time()  # Update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)  # Persist changes

    return None


# Sort utility function with applied change
def sort_prompts_by_date(prompts, descending=True) -> list:
    """Sort a list of prompts by creation date.

    Args:
        prompts (list): A list of prompts to sort.
        descending (bool): Determines sort order, True for newest first.

    Returns:
        list: Sorted list of prompts.
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)
