import os, argparse
import csv, barcode
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import inch, mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, required=True, help='Output PDF file name.')
    parser.add_argument('--input', type=str, required=True, help='Input CSV file name.')
    args = parser.parse_args()

    OUTPUT_FILE_NAME = args.output
    CSV_FILE = args.input

    print('Load CSV file.')

    with open(CSV_FILE, 'r') as f:

        reader = csv.reader(f)

        header = next(reader)

        data = [r for r in reader]
        data = filter(lambda r: len(r[0].replace(' ',''))==13 or len(r[0].replace(' ',''))==8, data)
        data = [*map(lambda r: (r[1].strip().replace('\u3000', ' '), r[0].replace(' ','')), data)]
        image_paths = [*map(lambda p:f'./barcode/{p[0]}.png', data)]

        print('Make barcode images.')

        if not os.path.exists('./barcode'):
            os.makedirs('./barcode')

        for row in data:
            if len(row[1]) == 8:
                jan = barcode.get('ean8', row[1], writer=ImageWriter())
                filename = jan.save(f'./barcode/{row[0]}',options={
                    'module_height':43.85,
                    'module_width':0.675,
                    'font_size':40,
                    'text_distance':1.5,
                    'font_path':'font/Avenir.ttc'
                    })
            else:
                jan = barcode.get('ean13', row[1], writer=ImageWriter())
                filename = jan.save(f'./barcode/{row[0]}',options={
                    'module_height':43.85,
                    'module_width':0.675,
                    'font_size':40,
                    'text_distance':1.5,
                    'font_path':'font/Avenir.ttc'
                    })
        
        print('Make PDF file.')

        cv = canvas.Canvas(OUTPUT_FILE_NAME, pagesize=portrait(A4))

        pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
        cv.setFont('HeiseiKakuGo-W5', 10)

        row = 0
        col = -1
        # 210mm x 297mm
        for i, img in enumerate(image_paths):
            col += 1
            if col >= 5:
                row += 1
                col = -1
            if row >= 7:
                cv.showPage()
                cv.setFont('HeiseiKakuGo-W5', 10)
                row = 0
                col = 0
            cv.drawString(col*52*mm+5*mm, 297*mm - 10*mm - 50*mm*row, data[i][0])
            cv.drawImage(img, col*52*mm, 297*mm - 40*mm - 50*mm*row , width=50*mm, height=25*mm)
        cv.showPage()
        cv.save()

        print('complete!!')