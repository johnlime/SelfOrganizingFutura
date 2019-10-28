from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

canvas = canvas.Canvas("edited_fonts/output.pdf")

pdfmetrics.registerFont(TTFont('Futura', 'Futura.ttc'))
canvas.setFont('Futura', 18)
canvas.drawString(30, 785, "Self Organizing Futura")
canvas.drawString(430, 785, "Mioto Takahashi")

for i in range(1, len(alphabet)):
    for j in range(10):
        if i % 7 != 0:
            svg_font = svg2rlg("edited_fonts/uppercase/" + alphabet[i - 1] + "_to_" + alphabet[i] + "_" + str(j) + ".svg")
        svg_font.scale(0.04, 0.04)
        renderPDF.draw(svg_font, canvas, 8.5 * (10 * (i % 7) + j) - 70, 700 - 80 * int(i / 7))

for i in range(1, len(alphabet)):
    for j in range(10):
        if i % 7 != 0:
            svg_font = svg2rlg("edited_fonts/lowercase/" + alphabet[i - 1] + "_to_" + alphabet[i] + "_" + str(j) + ".svg")
        svg_font.scale(0.04, 0.04)
        renderPDF.draw(svg_font, canvas, 8.5 * (10 * (i % 7) + j) - 70, 370 - 80 * int(i / 7))

for i in range(1, 10):
    for j in range(10):
        svg_font = svg2rlg("edited_fonts/numbers/" + str(i - 1) + "_to_" + str(i) + "_" + str(j) + ".svg")
        svg_font.scale(0.04, 0.04)
        renderPDF.draw(svg_font, canvas, 6 * (10 * i + j) - 50, 30)
canvas.setFont('Futura', 8)
canvas.drawString(20, 20, "https://github.com/johnlime/Self_Organizing_Futura")
canvas.save()
