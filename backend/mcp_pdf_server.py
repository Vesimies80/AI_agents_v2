from mcp.server.fastmcp import FastMCP
from mcp.types import Resource
import typing
from pypdf import PdfReader
from pathlib import Path

mcp = FastMCP("northwind")
#Filler prompt
@mcp.prompt()
def example_prompt(code: str) -> str:
    return f"Please review this code:\n\n{code}"

#Using pypdf to read a pdf with path (TODO try and reduce amount of tokens processed this way if possible)
@mcp.tool()
def read_pdf(path: str) -> list[str]:
    """Read the text from a pdf file, divide it by each newline and return it as a list"""
    
    reader = PdfReader(path)
    result = []
    for page in reader.pages:
        text = page.extract_text()
        split_text = text.split(' \n')
        for row in split_text:
            #Ignore empty rows
            if row != '':
                result.append(row)
    return result

#TODO think about security should path be present here or should there be a helper function to figure out what file is referred to (This would be slower, but could be safer so agent doesn't reveal full path)
#For now this will only work with a certain folder and doesn't handle same or similarly named files very well
@mcp.tool()
def list_available_pdfs() -> list[tuple[str, str]]:
    """Returns a list of (filename, full_path) pairs for available PDFs each pair is 1 pdf"""
    project_root = Path(__file__).parent.parent
    pdf_folder = project_root / "pdfs"
    return [(file.name, str(file.resolve())) for file in pdf_folder.glob("*.pdf")]

if __name__ == "__main__":
    print("Starting server...")
    # Initialize and run the server
    mcp.run(transport="stdio")