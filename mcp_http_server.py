import os
import sys
import json
from mcp.server.fastmcp import FastMCP

# File Generation Utilities
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pptx import Presentation

# 1. Initialize official FastMCP Server Engine
# FastMCP built-in native SSE transport handles all protocol routing automatically!
mcp = FastMCP("Multi-Format Report Server")

# -------------------------------------------------------------------------
# 🛠️ Highly Versatile Multi-Format File Engine
# -------------------------------------------------------------------------
def execute_file_creation(filename: str, file_type: str, raw_content: str) -> str:
    os.makedirs("outputs", exist_ok=True)
    filepath = os.path.join("outputs", filename)
    file_type = file_type.lower().strip()
    
    # 📝 Markdown Engine
    if file_type == "markdown" or filename.endswith(".md"):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(raw_content)
            
    # 📊 Excel Engine
    elif file_type in ["excel", "xlsx", "csv"]:
        try:
            data = json.loads(raw_content)
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False)
        except Exception:
            df = pd.DataFrame([{"Report Content": raw_content}])
            df.to_excel(filepath, index=False)

    # 📄 PDF Engine
    elif file_type == "pdf":
        c = canvas.Canvas(filepath, pagesize=letter)
        textobject = c.beginText(50, 750)
        textobject.setFont("Helvetica", 10)
        for line in raw_content.split("\n"):
            textobject.textLine(line)
        c.drawText(textobject)
        c.save()

    # 📉 PowerPoint Engine
    elif file_type in ["powerpoint", "pptx"]:
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        txBox = slide.shapes.add_textbox(100, 100, 500, 500)
        txBox.text_frame.text = raw_content
        prs.save(filepath)
        
    else:
        return f"Unsupported file type profile: '{file_type}'"

    return f"Success: File safely exported to local storage path at '{filepath}'"

# -------------------------------------------------------------------------
# 🔌 Bind Tool Definition Directly to FastMCP Infrastructure
# -------------------------------------------------------------------------
@mcp.tool(
    name="generate_multi_format_report",
    description="Compiles raw summary analytics data matrices directly into physical business file downloads such as Markdown, Excel spreadsheets, PDFs, or PowerPoint decks."
)
def generate_multi_format_report(filename: str, file_type: str, raw_content: str) -> str:
    return execute_file_creation(filename, file_type, raw_content)

if __name__ == "__main__":
    # FastMCP native 'sse' transport ko direct execute karenge.
    # Yeh automatically built-in uvicorn server ko port 8000 aur host 0.0.0.0 par up kar dega.
    print("🚀 Starting FastMCP Native SSE Engine on port 8000...", file=sys.stderr)
    mcp.run(transport='sse')