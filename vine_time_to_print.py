import csv
from fpdf import FPDF
import os

# File paths
csv_file = "vine_time_card_data.csv"
image_dir = "img"
output_pdf = "output/vine_cards_sheet.pdf"
os.makedirs("output", exist_ok=True)

CARD_W, CARD_H = 88, 126  # mm
A4_W, A4_H = 210, 297     # mm

# Calculate how many cards fit per row and column
CARDS_PER_ROW = A4_W // CARD_W
CARDS_PER_COL = A4_H // CARD_H
CARDS_PER_PAGE = int(CARDS_PER_ROW * CARDS_PER_COL)

def add_card_to_sheet(pdf, x, y, vine_name, description, vine_id, trivia_question, answer, image_path):
    # Front (image)
    pdf.set_xy(x, y)
    if image_path:
        pdf.image(image_path, x=x, y=y, w=CARD_W, h=CARD_H)
    else:
        pdf.set_fill_color(200, 200, 200)
        pdf.rect(x, y, CARD_W, CARD_H, 'F')
        pdf.set_font("Pacifico-Regular", "", 16)
        pdf.set_text_color(255, 0, 0)
        pdf.set_xy(x, y + CARD_H/2 - 10)
        pdf.cell(CARD_W, 20, "Image not found", align="C")

def add_back_to_sheet(pdf, x, y, vine_name, description, trivia_question, answer):
    pdf.set_xy(x, y)
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(x, y, CARD_W, CARD_H, 'F')
    # Remove black border
    # pdf.set_draw_color(0, 0, 0)
    # pdf.rect(x+2, y+2, CARD_W-4, CARD_H-4)
    pdf.set_margins(0, 0, 0)
    pdf.set_font("Pacifico-Regular", "", 20)
    pdf.set_text_color(80, 177, 139)
    pdf.set_xy(x, y+6)
    pdf.multi_cell(CARD_W, 10, vine_name, align="C")
    pdf.set_y(pdf.get_y() + 4)
    pdf.set_font("DejaVuSerif", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.set_x(x+5)
    pdf.multi_cell(CARD_W-10, 7, description)
    pdf.set_y(pdf.get_y() + 5)
    pdf.set_font("Pacifico-Regular", "", 12)
    pdf.set_text_color(80, 177, 139)
    pdf.set_x(x+5)
    pdf.multi_cell(CARD_W-10, 7, "Trivia")
    pdf.set_font("DejaVuSerif", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.set_x(x+5)
    pdf.multi_cell(CARD_W-10, 7, trivia_question)
    pdf.set_y(pdf.get_y() + 4)
    pdf.set_font("DejaVuSerif", "", 11)
    pdf.set_text_color(128, 128, 128)
    pdf.set_x(x+5)
    pdf.multi_cell(CARD_W-10, 6, f"Answer: {answer}")
    # Game name at bottom
    pdf.set_font("Pacifico-Regular", "", 14)
    pdf.set_text_color(80, 177, 139)
    pdf.set_xy(x, y + CARD_H - 12)
    pdf.cell(CARD_W, 10, "Sabes esse vine?", align="C")

# Read all cards
cards = []
with open(csv_file, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        image_path = None
        for ext in ['jpg', 'jpeg', 'png']:
            potential_path = os.path.join(image_dir, f"{row['vine_id']}.{ext}")
            if os.path.exists(potential_path):
                image_path = potential_path
                break
        cards.append({
            "vine_name": row["vine_name"],
            "description": row["description"],
            "vine_id": row["vine_id"],
            "trivia_question": row["trivia_question"],
            "answer": row["answer"],
            "image_path": image_path
        })

# Create A4 PDF for fronts and backs
pdf = FPDF("P", "mm", "A4")
pdf.set_auto_page_break(False)
# Register custom fonts
pdf.add_font("Pacifico-Regular", "", "/Library/Fonts/Pacifico-Regular.ttf", uni=True)
pdf.add_font("DejaVuSerif", "", "/Library/Fonts/DejaVuSerif.ttf", uni=True)

num_pages = (len(cards) + CARDS_PER_PAGE - 1) // CARDS_PER_PAGE
for page in range(num_pages):
    # --- Fronts page ---
    pdf.add_page()
    for i in range(CARDS_PER_PAGE):
        card_idx = page * CARDS_PER_PAGE + i
        if card_idx >= len(cards):
            break
        card = cards[card_idx]
        row = i // int(CARDS_PER_ROW)
        col = i % int(CARDS_PER_ROW)
        x = col * CARD_W
        y = row * CARD_H
        add_card_to_sheet(pdf, x, y, **card)
    # --- Backs page ---
    pdf.add_page()
    total_cards_width = CARDS_PER_ROW * CARD_W
    for i in range(CARDS_PER_PAGE):
        card_idx = page * CARDS_PER_PAGE + i
        if card_idx >= len(cards):
            break
        card = cards[card_idx]
        row = i // int(CARDS_PER_ROW)
        # MIRROR the column for backs:
        col = int(CARDS_PER_ROW) - 1 - (i % int(CARDS_PER_ROW))
        x = (A4_W - total_cards_width) + col * CARD_W
        y = row * CARD_H
        add_back_to_sheet(pdf, x, y, card["vine_name"], card["description"], card["trivia_question"], card["answer"])
pdf.output(output_pdf)
print(f"PDF created: {output_pdf}")