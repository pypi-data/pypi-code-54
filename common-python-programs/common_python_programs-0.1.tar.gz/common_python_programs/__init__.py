from flask import Flask, render_template, request
import os
import pandas as pd


def joke():
    return (u'Wenn ist das Nunst\u00fcck git und Slotermeyer? Ja! ... '
            u'Beiherhund das Oder die Flipperwaldt gersput.')


def introduction():
    return "this package was created for the internal usgae"


def check_palindrome(string):
    if str(string) == str(string)[::-1]:
        return str(string) + ' is a palindrome'
    else:
        return str(string) + ' is not a palindrome'


def upload_file(path):
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(path, file.filename))
        # os.path.join("C:/Users/saich/Desktop/Optiva/",f.filename)
        return 'file uploaded successfully'

    return '''<!doctype html>
    <title>Upload File</title>
    <h1>Upload New File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


def file_to_html(file_path):
    """convert the dataframe into html page"""
    df = pd.read_csv(file_path)
    return df.to_html()


def drop_empty_rows_columns(data_frame):
    """ drops the empty columns and empty rows which may contains empty values or nan """
    data_frame = data_frame.dropna(how='all', axis=1)
    data_frame = data_frame.dropna(how='all', axis=0)
    data_frame = data_frame.fillna('')
    columns_to_be_dropped = []
    rows_to_be_dropped = []
    for column in data_frame.columns:
        if set(data_frame[column]) == {''}:
            columns_to_be_dropped.append(column)
    for index in data_frame.index:
        if set(data_frame.loc[index].values) == {''}:
            rows_to_be_dropped.append(index)
    data_frame = data_frame.drop(columns_to_be_dropped, axis=1)
    data_frame = data_frame.drop(rows_to_be_dropped, axis=0)
    return data_frame


def get_files_in_directory(directory_path):
    """ return the list of names in a directory"""
    files = []
    for filename in os.listdir(directory_path):
        path = os.path.join(directory_path, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def data_frame_to_json(data_frame):
    """ return the data_frame in the from of json"""
    return data_frame.to_json()

