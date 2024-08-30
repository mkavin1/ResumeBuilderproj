from flask import Flask, render_template, request, redirect, url_for
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError
import os

app = Flask(__name__)

# AWS S3 Configuration
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1'
)
bucket_name = 'rbbt'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    # Extract form data
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    experience = request.form.get('experience')
    education = request.form.get('education')
    skills = request.form.get('skills')
    template_type = request.form.get('template')

    # Create PDF in memory
    pdf = BytesIO()
    c = canvas.Canvas(pdf, pagesize=letter)
    width, height = letter

    # Template-based content
    if template_type == 'template1':
        c.drawString(100, height - 50, f"Name: {name}")
        c.drawString(100, height - 70, f"Email: {email}")
        c.drawString(100, height - 90, f"Phone: {phone}")
        c.drawString(100, height - 110, f"Address: {address}")
        c.drawString(100, height - 130, "Experience:")
        c.drawString(100, height - 150, experience)
        c.drawString(100, height - 190, "Education:")
        c.drawString(100, height - 210, education)
        c.drawString(100, height - 250, "Skills:")
        c.drawString(100, height - 270, skills)
    else:
        c.drawString(100, height - 50, f"RESUME OF {name.upper()}")
        c.drawString(100, height - 90, f"Contact: {email}, {phone}")
        c.drawString(100, height - 130, f"Address: {address}")
        c.drawString(100, height - 180, "Experience:")
        c.drawString(100, height - 200, experience)
        c.drawString(100, height - 250, "Education:")
        c.drawString(100, height - 270, education)
        c.drawString(100, height - 320, "Skills:")
        c.drawString(100, height - 340, skills)

    # Finalize the PDF
    c.showPage()
    c.save()

    # Upload to S3
    pdf.seek(0)
    file_name = 'resume.pdf'
    try:
        s3_client.upload_fileobj(pdf, bucket_name, file_name)
        # Generate a presigned URL for download
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': file_name},
            ExpiresIn=3600  # URL expiry time in seconds
        )
    except NoCredentialsError:
        return "Credentials not available"

    # Redirect to the presigned URL for download
    return redirect(url)

if __name__ == '__main__':
    app.run(debug=True)
