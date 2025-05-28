from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_sample_pdf():
    c = canvas.Canvas("inputs/sample.pdf", pagesize=letter)
    c.drawString(100, 750, "Invoice #123")
    c.drawString(100, 730, "Amount: $500")
    c.drawString(100, 710, "Date: 2025-05-28")
    c.drawString(100, 690, "Company: XYZ Corp")
    c.save()
    print("Sample PDF created at inputs/sample.pdf")

if __name__ == "__main__":
    create_sample_pdf()