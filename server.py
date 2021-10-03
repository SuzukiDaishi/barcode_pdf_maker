
# スプレッドシートでバーコードを生成するサーバー(良ければどうぞ)

import os
import csv,barcode
from barcode.writer import ImageWriter

from flask import Flask, request, send_file, jsonify
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def root():
    return jsonify({'message':'このAPIはバーコードを生成するやつです。'})

@app.route('/barcode')
def get_barcode():
    code = request.args.get('code')
    code = str(int(code))

    if os.path.exists('./barcode.png'):
        os.remove('./barcode.png')

    if len(code) == 8:
        jan = barcode.get('ean8', code, writer=ImageWriter())
        jan.save(
            f'barcode',options={
                'module_height':43.85,
                'module_width':0.675,
                'font_size':40,
                'text_distance':1.5,
                'font_path':'/System/Library/Fonts/Avenir.ttc'
            }
        )
    else :
        jan = barcode.get('jan', code, writer=ImageWriter())
        jan.save(
            f'barcode',options={
                'module_height':43.85,
                'module_width':0.675,
                'font_size':40,
                'text_distance':1.5,
                'font_path':'/System/Library/Fonts/Avenir.ttc'
            }
        )
    return send_file('./barcode.png', mimetype='image/gif')

if __name__ == "__main__":
    app.run(port=8888)