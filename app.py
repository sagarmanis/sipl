from flask import  Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import paddleocr
from paddleocr import PaddleOCR
import base64
import os
from pdf2image import convert_from_path
import json
import io

app = Flask(__name__)

parser = reqparse.RequestParser()
parser.add_argument('imageBase64', type=str)
parser.add_argument('clientCode', type=str)
parser.add_argument('token', type=str)
parser.add_argument('pdfBase64', type=str)

@app.route('/SpeedPostCaptcha',methods=['POST'])
def SpeedPostCaptcha():
    try:
        request.get_json(force=True)
        args = parser.parse_args()
        file_path='content/images/APIImage/1.jpg'
        if(len(args['imageBase64'])>500):
            image_data = base64.b64decode(args['imageBase64'].encode())
            with open(file_path, "wb") as file:
                file.write(image_data)
        else:
            file_path=args['imageBase64']#'https://prnt.sc/opnQvtaHODFB'
        ocr = PaddleOCR()
        result = ocr.ocr(file_path,det=True)
        return result[0][0][1][0]
    except Exception as e:
        return str(e)
    
@app.route('/ReadImage',methods=['POST'])
def ReadImage():
    try:
        request.get_json(force=True)
        args = parser.parse_args()
        file_path='content/images/APIImage/1.jpg'
        if(len(args['imageBase64'])>500):
            image_data = base64.b64decode(args['imageBase64'].encode())
            with open(file_path, "wb") as file:
                file.write(image_data)
        else:
            file_path=args['imageBase64']#'https://prnt.sc/opnQvtaHODFB'
        ocr = PaddleOCR()
        result = ocr.ocr(file_path,det=True)
        return result
    except Exception as e:
        return str(e)   
    

@app.route('/ConvertPdfToImage',methods=['POST'])
def ConvertPdfToImage():
    try:
        image_format='PNG'
        request.get_json(force=True)
        args = parser.parse_args()
        clientCode=args['clientCode']
        token=args['token']
        base64_string=args['pdfBase64']
        
        output_path=f"content/pdf/{clientCode}.pdf"
        pdf_bytes = base64.b64decode(base64_string)
        with open(output_path, 'wb') as pdf_file:
            pdf_file.write(pdf_bytes)

        #output_dir = 'path/to/your/output_directory'
        #os.makedirs(output_dir, exist_ok=True)
        images = convert_from_path(output_path, dpi=200,poppler_path=r'C:\Utils\Poppler')
        json_list = []
        
        for i in range(len(images)):  
            buffer = io.BytesIO()
            images[i].save(buffer, format="PNG")
            image_data = buffer.getvalue()
            base64_encoded = base64.b64encode(image_data).decode("utf-8")
            jsonString = {
                "Name": f"page_{i + 1}.{image_format}",
                "imageBase64": base64_encoded
            }
            json_list.append(jsonString)
        json_string =json.dumps(json_list)           
        return json_string
    except Exception as e:
        return str(e)       

if __name__ == '__main__':
    app.run()