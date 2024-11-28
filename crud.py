from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import pymysql.cursors
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import boto3

load_dotenv()

app = Flask(__name__)
CORS(app)

bucket_name = os.getenv('BUCKET_NAME')
aws_region = os.getenv('REGION')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

bucket = boto3.client('s3',aws_region, aws_access_key_id, aws_secret_access_key)

def get_db_connection():
    connection = pymysql.connect(
        host=os.getenv('HOST'),
        port=os.getenv('PORT'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

@app.route('/')
def index():
    return 'Welcome to the CRUD Notes :)'

@app.route('/nota', methods=['POST'])
def create_nota():
    data = request.json
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO Notas (Cliente, Direccion_Facturacion, Direccion_Envio, Total) VALUES (%s, %s, %s, %s)', 
        (data['cliente'], data['direccion_facturacion'], data['direccion_envio'], data['total']))
        cursor.execute('INSERT INTO ContenidoNota (Producto, Cantidad, Precio_Unitario, Importe) VALUES (%s, %s, %s, %s)', 
        (data['producto'], data['cantidad'], data['precio_unitario'], data['importe']))
        cursor.close()
    connection.commit()
    connection.close()

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    c.drawString(100, 735, f"Cliente: {data['cliente']}")
    c.drawString(100, 720, f"Dirección de Facturación: {data['direccion_facturacion']}")
    c.drawString(100, 705, f"Dirección de Envío: {data['direccion_envio']}")
    c.drawString(100, 690, f"Total: {data['total']}")
    c.drawString(100, 675, f"Producto: {data['producto']}")
    c.drawString(100, 660, f"Cantidad: {data['cantidad']}")
    c.drawString(100, 645, f"Precio Unitario: {data['precio_unitario']}")
    c.drawString(100, 630, f"Importe: {data['importe']}")
    c.save()

    pdf_buffer.seek(0)
    bucket.upload_fileobj(pdf_buffer,bucket_name,f'{data["cliente"]}.pdf')
    url = f"https://{bucket_name}.s3.amazonaws.com/{data['cliente']}"

    return jsonify({'message': 'Nota creada'}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)