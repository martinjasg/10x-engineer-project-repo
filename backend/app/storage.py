

# ============== Updated with Google-Style Docstrings ==============

class Storage:
    """In-memory storage for managing prompts and collections.

    Attributes:
        _prompts (Dict[str, Prompt]): Internal storage for prompts.
        _collections (Dict[str, Collection]): Internal storage for collections.
    """
    def __init__(self):
        """Initialize the Storage class with empty in-memory dictionaries."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Store a new prompt in in-memory storage.

        Args:
            prompt (Prompt): The prompt object to be stored.

        Returns:
            Prompt: The stored prompt object.
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its ID.

        Args:
            prompt_id (str): The unique ID of the prompt.

        Returns:
            Optional[Prompt]: The prompt object if found, else None.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all stored prompts.

        Returns:
            List[Prompt]: A list of all prompt objects.
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt to update.
            prompt (Prompt): The updated prompt object.

        Returns:
            Optional[Prompt]: The updated prompt object if found, else None.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt to delete.

        Returns:
            bool: True if the prompt was deleted, False otherwise.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Store a new collection in in-memory storage.

        Args:
            collection (Collection): The collection object to be stored.

        Returns:
            Collection: The stored collection object.
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its ID.

        Args:
            collection_id (str): The unique ID of the collection.

        Returns:
            Optional[Collection]: The collection object if found, else None.
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieve all stored collections.

        Returns:
            List[Collection]: A list of all collection objects.
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to delete.

        Returns:
            bool: True if the collection was deleted, False otherwise.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieve prompts associated with a specific collection.

        Args:
            collection_id (str): The ID of the collection to filter prompts.

        Returns:
            List[Prompt]: A list of prompt objects belonging to the collection.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Clear all prompts and collections from storage."""
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()
