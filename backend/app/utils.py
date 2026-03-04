

# ============== Updated with Google-Style Docstrings ==============

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by the creation date.

    Args:
        prompts (List[Prompt]): List of prompt objects to sort.
        descending (bool): If True, sort from newest to oldest. Defaults to True.

    Returns:
        List[Prompt]: The sorted list of prompts.
    """
    # BUG #3: This sorts ascending (oldest first) when it should sort descending (newest first)
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by their associated collection ID.

    Args:
        prompts (List[Prompt]): List of prompts to filter.
        collection_id (str): The collection ID to filter prompts by.

    Returns:
        List[Prompt]: A list of prompts linked to the specified collection.
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search for prompts by title or description.

    Args:
        prompts (List[Prompt]): List of prompts to search within.
        query (str): The search term to match against prompt titles or descriptions.

    Returns:
        List[Prompt]: A list of prompts that contain the search term in their title or description.
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Check if prompt content is valid.

    A valid prompt must:
    - Not be empty
    - Not be just whitespace
    - Be at least 10 characters long

    Args:
        content (str): The content of the prompt to validate.

    Returns:
        bool: True if the content is valid, False otherwise.
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
    Variables are in the format {{variable_name}}

    Args:
        content (str): The prompt content to search for variables.

    Returns:
        List[str]: A list of variables found within the prompt content.
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
