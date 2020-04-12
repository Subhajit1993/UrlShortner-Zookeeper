from flask import current_app, request, json, Response, redirect
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, InvalidRequestError
from app import db
from models.users import User
from models.urls import Url
from app import zk
import hashlib

db.create_all()
db.session.commit()

fixed_increment_id = 1000000

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode(num, alphabet=BASE62):
    """Encode a positive number in Base X

    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def decode(string, alphabet=BASE62):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1
    return num


def index():
    db.session.add(User(name="Flask", email="example@example.com"))
    db.session.commit()
    resp = Response(
        json.dumps({

        }),
        status=200,
        mimetype='application/json'
    )
    return resp


def get_seq():
    global fixed_increment_id
    seq = zk.create("/node", b"a value", sequence=True)
    seq = seq[5:]
    seq = (int(seq))
    seq = seq + fixed_increment_id
    return seq


def get_url(short_code):
    url = Url.query.get(short_code)
    return redirect(url.original_url, code=302)


def add_url():
    post_data = request.data
    post_data_dict = json.loads(post_data)
    original_url = post_data_dict.get('original_url')
    seq = get_seq()
    encoded_id = (encode(seq))
    short_code = encoded_id
    db.session.add(Url(original_url=original_url, short_code=short_code))
    try:
        db.session.commit()
        final_url = "http://localhost:5000/" + short_code
    except Exception as e:
        db.session.rollback()
        return Response(
            json.dumps("Some error occurred"),
            status=200,
            mimetype='application/json'
        )
    finally:
        db.session.close()
    resp = Response(
        json.dumps(final_url),
        status=200,
        mimetype='application/json'
    )
    return resp
