import csv
from fpdf import FPDF
from PIL import Image
import os

# File paths
csv_file = "vine_time_card_data.csv"
image_dir = "img"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Function to create a card
def create_card(vine_name, description, vine_id, trivia_question, answer):
    pdf = FPDF("P", "mm", (88, 126))  # Card size

    # Front of card (image side)
    pdf.add_page()
    image_path = None
    for ext in ['jpg', 'jpeg', 'png']:  # Check for multiple extensions
        potential_path = os.path.join(image_dir, f"{vine_id}.{ext}")
        if os.path.exists(potential_path):
            image_path = potential_path
            break

    if image_path:
        pdf.image(image_path, x=0, y=0, w=88, h=126)  # Fill the entire card with the image
    else:
        print(f"Image not found for reference: {vine_id}")
        return

    # Back of card (text side)
    pdf.add_page()
    pdf.set_fill_color(255, 255, 255)  # White background
    pdf.rect(0, 0, 88, 126, 'F')  # Fill the background
    pdf.set_draw_color(0, 0, 0)  # Black border
    pdf.rect(2, 2, 84, 122)  # Add a border

    pdf.set_margins(5, 5, 5)
    pdf.add_font("Pacifico-Regular", "", "/Library/Fonts/Pacifico-Regular.ttf", uni=True)
    pdf.add_font("DejaVuSerif", "", "/Library/Fonts/DejaVuSerif.ttf", uni=True)

    pdf.set_font("Pacifico-Regular", '', 20)
    pdf.set_text_color(80, 177, 139)  # Green title
    pdf.multi_cell(0, 10, vine_name, align="C")
    
    pdf.set_y(pdf.get_y() + 4)  # Move down 4mm

    pdf.set_font("DejaVuSerif", '', 12)
    pdf.set_text_color(0, 0, 0)  # Black text
    pdf.multi_cell(0, 7, description)
    
    pdf.set_y(pdf.get_y() + 5)  # Move down 5mm

    pdf.set_font("Pacifico-Regular", '', 12)
    pdf.set_text_color(80, 177, 139)  # Green trivia title
    pdf.multi_cell(0, 7, "Trivia")
    
    pdf.set_font("DejaVuSerif", '', 12)
    pdf.set_text_color(0, 0, 0)  # Black text
    pdf.multi_cell(0, 7, trivia_question)
    
    pdf.set_y(pdf.get_y() + 4)  # Move down 5mm
    
    pdf.set_font("DejaVuSerif", '', 11)
    pdf.set_text_color(128, 128, 128)  # Gray italic text
    pdf.multi_cell(0, 6, f"Answer: {answer}")

    # # Add game name at the bottom of the same page
    # print(pdf.get_y())
    # pdf.set_y(126-12)  # 12mm from the bottom
    # pdf.set_font("Pacifico-Regular", '', 16)
    # pdf.set_text_color(80, 177, 139)
    # pdf.cell(0, 1, "Sabes esse vine?", align="C")

    # Save PDF
    pdf_path = os.path.join(output_dir, f"vine_card_{vine_id.lower().replace(' ', '_')}.pdf")
    pdf.output(pdf_path)
    print(f"PDF created: {pdf_path}")

# Read CSV and generate cards
try:
    with open(csv_file, newline='', encoding='utf-8-sig') as csvfile:  # Use utf-8-sig to handle BOM
        reader = csv.DictReader(csvfile)
        # Debug: Print the header row
        print(f"CSV Header: {reader.fieldnames}")
        for row in reader:
            create_card(
                vine_name=row["vine_name"],
                description=row["description"],
                vine_id=row["vine_id"],
                trivia_question=row["trivia_question"],
                answer=row["answer"]
            )
except Exception as e:
    print(f"Error processing CSV: {e}")