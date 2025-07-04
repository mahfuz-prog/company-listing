import os
import secrets
from PIL import Image
from functools import wraps
from flask_login import current_user
from flask import current_app, flash, abort

def save_img(img, location):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(img.filename)
    img_fn = random_hex + f_ext
    img_path = os.path.join(current_app.root_path, location, img_fn)

    i = Image.open(img)
    i.save(img_path)

    return img_fn


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated and current_user.email == current_app.config.get('ADMIN_EMAIL'):
            return f(*args, **kwargs)
        else:
            flash('Please login as admin!')
            abort(403)
    return wrap