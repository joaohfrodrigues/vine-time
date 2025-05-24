import csv

# Input and output file paths
input_file = "/Users/ctw01425/projects/vine_trivia/test.csv"
output_file = "/Users/ctw01425/projects/vine_trivia/vine_time_card_data.csv"

# Reformat the CSV
with open(input_file, newline='', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)  # Enclose all fields in double quotes
    for row in reader:
        writer.writerow(row)

print(f"Formatted CSV saved to: {output_file}")