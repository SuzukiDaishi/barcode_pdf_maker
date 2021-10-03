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
    parser.add_argument('--output', type=str, required=True, help='Output PDF file name. (no extension)')
    parser.add_argument('--input', type=str, required=True, help='Input CSV file.')
    args = parser.parse_args()

    OUTPUT_FILE_NAME = args.output
    CSV_FILE = args.input

    print('Load CSV file.')

    with open(CSV_FILE, 'r') as f:

        reader = csv.reader(f)

        header = next(reader)

        data = [r for r in reader]
        data = filter(lambda r: len(r[0].replace(' ',''))==13 or len(r[0].replace(' ',''))==8, data)
        data = [*map(lambda r: (r[1].replace('\u3000', ' ').strip(), r[0].replace(' ',''), r[2].replace('\u3000', ' ').strip()), data)]
        keys = set([d[2] for d in data])
        datas = {}
        for k in keys:
            datas[k] = [*filter(lambda d:d[2]==k, data)]

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

        pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
        pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
        for k in datas.keys():
            cv = canvas.Canvas(f'{OUTPUT_FILE_NAME}_{k}.pdf', pagesize=portrait(A4))
            cv.setFont('HeiseiKakuGo-W5', 50)
            cv.drawString(5*mm, 297*mm - 30*mm, k)
            cv.setFont('HeiseiMin-W3', 8)
            row = 1
            col = -1
            for i, d in enumerate(datas[k]):
                col += 1
                if col >= 4:
                    row += 1
                    col = 0
                if row >= 8:
                    cv.showPage()
                    cv.setFont('HeiseiMin-W3', 8)
                    row = 0
                    col = 0
                text = d[0]
                for i in range(0, len(text), 10):
                    cv.drawString(col*52*mm+5*mm, 297*mm - 5*mm - 35*mm*row - 4*mm*(i//10), text[i:i+10])
                cv.drawImage(f'./barcode/{d[0]}.png', col*52*mm, 297*mm - 35*mm - 35*mm*row , width=50*mm, height=25*mm)
            cv.showPage()
            cv.save()
            
        print('complete!!')