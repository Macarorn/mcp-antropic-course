from pydantic import Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc

@mcp.tool(
    name="read_doc_contents",
    description="Leer el contenido de un documento y retornarlo como un string"
)

def read_document(
    doc_id: str = Field(description="ID del documento a leer")
):
    if doc_id not in docs:
        raise ValueError(f"Documento '{doc_id}' no encontrado")
    return docs[doc_id]

# Esto es todo lo que toma escribir una tool

# TODO: Write a tool to edit a doc

@mcp.tool(
    name="edit_document",
    description="Editar un documento al reemplazar un string en el contenido del documento"
)

def edit_document(
    doc_id:str = Field(description="Id of the document that will be edited"),
    old_str:str = Field(description="The text to replace. Must match exactly, include a withe space"),
    new_str:str = Field(description="The new text to insert in place of the old text")
):
    if doc_id not in docs:
        raise ValueError(f"Documento '{doc_id}' no encontrado")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    return f"Documento '{doc_id}' editado exitosamente"

# TODO: Write a resource to return all doc id's
# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
