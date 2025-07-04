from docx import Document
import re
import json
docx_path="C:\\Users\\l43ar\\Downloads\\mermaiddynamic\\sdd.docx"
def extract_mermaid_from_docx(docx_path) -> dict:
    doc = Document(docx_path)
    full_text = ""

    # Extract full text from the document
    for para in doc.paragraphs:
        full_text += para.text + "\n"

    # Regex to extract mermaid code blocks
    mermaid_blocks = re.findall(r"```mermaid(.*?)```", full_text, re.DOTALL)

    # Store in dict with keys as 1,2,3,...
    mermaid_dict = {str(idx + 1): block.strip() for idx, block in enumerate(mermaid_blocks)}

    # Save to diagram.json
    with open("diagram.json", "w") as f:
        json.dump(mermaid_dict, f, indent=4)

    print(f"\nExtracted {len(mermaid_blocks)} Mermaid diagrams and saved to diagram.json\n")

    return mermaid_dict
extract_mermaid_from_docx(docx_path=docx_path)