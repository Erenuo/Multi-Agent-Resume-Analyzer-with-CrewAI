from crewai.tools import tool
import os


@tool("Resume File Parser")
def parse_resume_file(file_path: str) -> str:
    """
    Parse and extract text content from a local resume file.
    Supports .txt files.
    """
    try:
        file_path = file_path.strip().strip('"').strip("'")
        
        if not os.path.exists(file_path):
            return f"Error: File not found at '{file_path}'. Please check the path and try again."
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if not content.strip():
            return "Error: The file is empty. Please provide a resume with content."
        
        return content
        
    except PermissionError:
        return f"Error: Permission denied when trying to read '{file_path}'."
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            return f"Error: Could not decode file. Details: {str(e)}"
    except Exception as e:
        return f"Error reading file: {str(e)}"
