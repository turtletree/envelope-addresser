import codecs
import csv

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

font_chinese = 'STSong-Light'  # from Adobe's Asian Language Packs
pdfmetrics.registerFont(UnicodeCIDFont(font_chinese))

# Create a new PDF document as the output
pdf = canvas.Canvas('/path/to/output.pdf', pagesize=letter)
width, height = letter
top_margin = 40
left_margin = 40
line_spacing = 20
recipient_height = height / 4 * 3
recipient_left_margin = width / 3
font_size = 15
eng_font = 'Helvetica'

# assuming all envelopes have the same sender info / return address
sender_line1 = "Mr. & Mrs. Paul Smith"
sender_line2 = "1 Main St"
sender_line3 = "Boston, MA 02110"
sender_line4 = "USA"

with codecs.open('/path/to/input.csv', 'r', encoding='utf-8') as f:
    # create a csv reader from csv file
    csv_reader = csv.reader(f)
    # iterate over each row in the csv, ignore the first row
    curPage = 0
    for row in csv_reader:
        if curPage == 0:
            curPage += 1
            continue

        name, street, unit, city, state, zip, country = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        line1 = name
        line2 = street + " " + unit if unit else street
        line3 = city + ", " + state + " " + zip
        line4 = country

        # add sender info lines to the top left corner of the current page
        pdf.setFont(eng_font, font_size) # you know the font to use here
        pdf.drawString(left_margin, height - top_margin, sender_line1)
        pdf.drawString(left_margin, height - top_margin - line_spacing, sender_line2)
        pdf.drawString(left_margin, height - top_margin - line_spacing * 2, sender_line3)
        pdf.drawString(left_margin, height - top_margin - line_spacing * 3, sender_line4)

        # Set recipient font and font size based on language
        if name.isascii() and street.isascii() and city.isascii() and state.isascii():
            pdf.setFont(eng_font, font_size)
        else:
            pdf.setFont(font_chinese, font_size)
        # add lines to the center of the page
        pdf.drawString(recipient_left_margin, recipient_height, line1)
        pdf.drawString(recipient_left_margin, recipient_height - line_spacing, line2)
        pdf.drawString(recipient_left_margin, recipient_height - line_spacing * 2, line3)
        pdf.drawString(recipient_left_margin, recipient_height - line_spacing * 3, line4)

        # save the current page and start a new page
        pdf.showPage()

# Save the PDF document
pdf.save()
