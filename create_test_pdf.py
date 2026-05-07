from reportlab.pdfgen import canvas
c = canvas.Canvas("test_contract.pdf")
text = """CONTRACT
WHEREAS, Party A shall indemnify Party B pursuant to this Agreement 
notwithstanding prior discussions, subject to terms herein."""
y = 750
for line in text.split('\n'):
    c.drawString(50, y, line)
    y -= 20
c.save()
print("✅ test_contract.pdf created!")