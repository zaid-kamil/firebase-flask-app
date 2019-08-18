import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth,firestore

# try:
#     user = auth.create_user(
#         email='xaidmeta@gmail.com',
#         email_verified=False,
#         phone_number='+917860380291',
#         password='almight',
#         display_name='Zaid Kamil',
#         disabled=False
#     )
#     print('Sucessfully created new user: {0}'.format(user.uid))
# except Exception as e:
#     print(e)

def save_auth(file,details):
    with open(file+".auth",'wb') as f:
        pickle.dump(details,f)


def load_auth(file):
    with open(file+'.auth','rb') as f:
        return pickle.load(f)


def register_user(email,phone_number,password,display_name):
    cred = credentials.Certificate("serviceAccountKey.json")
    fbadmin =firebase_admin.initialize_app(cred)
    try:
        user = auth.create_user(
            email=email,
            email_verified=False,
            phone_number=phone_number,
            password=password,
            display_name=display_name,
            disabled=False
        )
        save_auth(email.split('@')[0],details={'password':password,'name':display_name})
        return user
    except Exception as e:
        print(e)

def verify_user(email,password):
    detail = load_auth(email.split('@')[0])
    if password == detail.get('password'):
        try:
            record = auth.get_user_by_email(email)
            return record
        except Exception as e:
            print('error',e)
            return {'msg':'some error occurred'}
    else:
        return {"msg":'invalid password'}
        