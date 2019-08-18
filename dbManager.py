import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid

# try:
#     cred = credentials.Certificate('serviceAccountKey.json')
#     firebase_admin.initialize_app(cred)
# except Exception as e:
#     print(e)

def add_product_to_cloud(col="products",data={}):
    db = firestore.client()
    try:
        db.collection(col).document(str(uuid.uuid4())).set(data)
        return True
    except Exception as e:
        print(e)
        return False

def get_product_from_cloud(col="products"):
    db = firestore.client()
    try:
        ref = db.collection(col)
        docs = ref.stream()
        for doc in docs:
            yield {
                'id':doc.id,
                'data':doc.to_dict()
            }
    except Exception as e:
        print(e)

if __name__ == "__main__":
    data = get_product_from_cloud()
    for item in data:
        print(item)