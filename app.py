from flask import Flask, render_template, request, redirect, url_for, flash, Response
import boto3
# client = boto3.client('s3', region_name='eu-west-2')
#from flask_bootstrap import Bootstrap
# client.upload_file('images/image_0.jpg', 'MyBucket745', 'image_0.jpg')###
from filters import datetimeformat, file_type

app = Flask(__name__)
#Bootstrap(app)
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type
app.secret_key = 'secret'
s3 = boto3.resource('s3')
bucket = s3.Bucket('mybucket745')

@app.route('/')
def home():
    return render_template("home.html")





@app.route('/Upload', methods=['POST'])
def upload():
    file = request.files['file']

    bucket.Object(file.filename).put(Body=file)

    flash('File uploaded successfully')
    return redirect(url_for('files'))



@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']

    file_obj = bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition":"attachment;filename={}".format(key)}
    )

@app.route('/files')
def files():
    summaries = bucket.objects.all()

    return render_template('files.html', bucket=bucket, files=summaries)

@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    bucket.Object(key).delete()

    flash('File deleted successfully')
    return redirect(url_for('files'))

if __name__=='__main__':
    app.run(debug=True)
