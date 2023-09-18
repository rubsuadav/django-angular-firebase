import random
from firebase_admin import firestore
from firebase_admin import auth


def generate_phone_number():
    phone_number = ''
    for i in range(9):
        if i == 0:
            phone_number += str(random.randint(6, 7))
        else:
            phone_number += str(random.randint(0, 9))
    return phone_number


def delete_collection_ref(col_ref):
    db = firestore.client()
    posts_ref = db.collection(col_ref)
    docs = posts_ref.stream()
    for doc in docs:
        doc.reference.delete()


def delete_posts_collection():
    delete_collection_ref(u'posts')


def delete_users_collection():
    delete_collection_ref(u'users')


def delete_auth_users():
    for u in auth.list_users().users:
        auth.delete_user(u.uid)
