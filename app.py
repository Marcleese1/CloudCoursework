from flask import Flask, render_template, request, redirect, url_for, flash, Response
import boto3
from filters import datetimeformat, file_type

app = Flask(__name__)#initialising the app using flask
app.jinja_env.filters['datetimeformat'] = datetimeformat#filtering the date to only show the time update as opposed to the whole thing
app.jinja_env.filters['file_type'] = file_type#filtering the type of file to only show the extention of the file
app.secret_key = 'secret'
s3 = boto3.resource('s3')#setting the boto3 recourse to s3 for the whole project
bucket = s3.Bucket('mybucket745')#setting the bucket to my bucket made in s3

@app.route('/')#the home page of the small web app it renders out the home page which displays the link to go to the files page
def home():
    return render_template("home.html")





@app.route('/Upload', methods=['POST'])#the logic to upload files to the bucket
def upload():
    file = request.files['file']#requests the file

    bucket.Object(file.filename).put(Body=file)#gets the filename and saves the file to the bucket as the same name

    flash('File uploaded successfully')
    return redirect(url_for('files'))



@app.route('/download', methods=['POST'])#allows the user to download files
def download():
    key = request.form['key']#gets the key from the bucket

    file_obj = bucket.Object(key).get()

    #returns the response from the bucket and saves the file to the downloads folder
    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition":"attachment;filename={}".format(key)}
    )

#displays the list of files in the bucket
@app.route('/files')
def files():
    summaries = bucket.objects.all()#gets all the objects in the bucket

    return render_template('files.html', bucket=bucket, files=summaries)#returns the objects in the bucket and displays them in the HTML od the files.html page


#allows the user to delete items from the bucket
@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']#gets the key from the bucket item

    bucket.Object(key).delete()#deletes that bucket irem

    flash('File deleted successfully')
    return redirect(url_for('files'))

if __name__=='__main__':#the statement used to run the file
    app.run(debug=True)
