import json
from fpdf import FPDF

def parse_to_string(dic):
    for key in dic:
        print(key)

class PDF(FPDF):
    def drawTable(self, headers, items):
        for col in headers:
            if (col.lower() == 'description'):
                self.cell(60, 10, col, 1, 0, 'C')
            else: 
                self.cell(40, 10, col, 1, 0, 'C')
        self.ln()
        total = 0 # storing the total amount of the purchased items
        for item in items:
            desc = item['description']
            quantity = item['quantity']
            unit_price = item['unit_price']
            amount = unit_price * quantity
            total += amount
            arr = [desc, quantity, unit_price, amount]
            for idx, col in enumerate(arr):
                col = str(col)
                if (idx == 0):
                    self.cell(60, 10, col, 0, 0, 'C')
                else: 
                    self.cell(40, 10, col, 0, 0, 'C')
            self.ln()
        self.set_x(150) 
        self.cell(40, 10, str(total), 0, 0, 'C')
        self.ln()

    def header(self):
        self.set_font('Arial', 'B', 30)
        self.cell(40, 20, "INVOICE", 0 ,1)

    def footer(self):
        self.set_font('Arial', '', 8)
        self.cell(180, 10, "Thnx for using My product", 0,1, 'C')

with open("test.json", "r") as f:
    json_dict = json.load(f)
 
# invoice_number
# invoice_date
# due_date
# bill_to
# company
# items
# tax_percentage
# notes
# signature

# storing variablese
items = json_dict["items"]
bill_to = json_dict["bill_to"]
invoice_number = json_dict["invoice_number"]
invoice_date = json_dict["invoice_date"]
due_date = json_dict["due_date"]
company = json_dict["company"]
headers = ["Description", "Quantity", "Unit Price", "Amount"]

pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 8)
pdf.cell(40, 5, "Aro CO", 0, 0)
pdf.ln()

pdf.set_font('Arial', '', 8)
pdf.multi_cell(80, 3, """Flat No. 12B,
Sunshine Residency Apartments, 
5th Cross, JP Nagar Phase 6,
Bengaluru, Karnataka 560078
India""")
pdf.ln() # adding the new line

# bill to
pdf.set_font('Arial', 'B', 8)
pdf.cell(40, 2, "Bill To:")
pdf.ln()
pdf.set_font('Arial', '', 8)
pdf.cell(40, 5, bill_to['name'])
pdf.ln()
pdf.multi_cell(80, 3, bill_to['address'])

# Invoice meta block (flex style)
pdf.set_xy(100, 52)
pdf.cell(30, 5, "Invoice #:", 0, 0)
pdf.cell(40, 5, invoice_number, 0, 0)

pdf.set_xy(100, 56)
pdf.cell(30, 5, "Invoice date:", 0, 0)
pdf.cell(40, 5, invoice_date, 0, 0)

pdf.set_xy(100, 60)
pdf.cell(30, 5, "Due date:", 0, 0)
pdf.cell(40, 5, due_date, 0, 0)
pdf.ln(10)

pdf.drawTable(headers, items)
pdf.output("invoice.pdf", 'F')
