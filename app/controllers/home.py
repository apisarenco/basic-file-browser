from app import app
from flask import render_template, flash, redirect, url_for, request
from app.models import directory
from app.view_models import dir as dir_model


@app.route('/dir', defaults = {'path': ''})
@app.route('/dir/<path:path>', methods=['GET'])
def dir(path):
    dir_obj = directory.Directory(path)
    model = dir_model.Dir(dir_obj)
    return render_template('public/main.html', title='New', model=model)
