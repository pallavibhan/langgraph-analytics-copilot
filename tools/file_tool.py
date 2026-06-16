import os
from langchain_core.tools import tool

@tool
def save_to_markdown(filename: str, content: str) -> str:
    """
    Saves the final data metrics, analytical breakdown, and SQL queries into a structured Markdown (.md) file.
    Use this tool ONLY when you have compiled the final answer matrix and are ready to deliver the complete report to the user.
    """
    print("Markdown Tool Called")
    try:
        # Ensure outputs directory exists
        os.makedirs("outputs", exist_ok=True)
        
        # Clean the filename to ensure it ends with .md
        if not filename.endswith(".md"):
            filename = f"{filename}.md"
            
        filepath = os.path.join("outputs", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"Success: Final report safely exported to Markdown file at '{filepath}'."
    except Exception as e:
        return f"Error saving file: {str(e)}"