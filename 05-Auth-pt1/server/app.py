
# Import what we need from our config file!
# from config import app, api, Resource, request, session, NotFound, bcrypt

# Let's start by moving most of our imports and other things into a new file called config.py
    # This will allow us to leave our app file focus just on routing and reduce clutter! Let's move lines 28-55!!! 🫡
from flask import Flask, request, session
from flask_migrate import Migrate

from flask_restful import Api, Resource
# from werkzeug.exceptions import NotFound, Unauthorized

from flask_cors import CORS

# Import Bcrypt from flask_bcrypt
from flask_bcrypt import Bcrypt

from models import db, Production, CastMember, User

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Set up:
    # generate a secrete key `python -c 'import os; print(os.urandom(16))'`
app.secret_key = b'5\xe9t\x01\x12A\n\xe4\xb0\x9b\x05\xde\xd4\xc5\x888'

# Make a variable called bcrypt set it equal to Bcrypt with app passed to it
bcrypt = Bcrypt( app )

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Before starting here, let's make sure our models are in order!!! 🌟

# 1.✅ Create a Signup route
class Signup ( Resource ) :
    #1.2 The signup route should have a post method
    def post ( self ) :
        #1.2.1 Get the values from the request body with get_json
        rq = request.get_json()
        User.clear_validation_errors()
        try :
            #1.2.2 Create a new user, however only pass email/username ( and any other values we may have )
            new_user = User(
                username = rq[ 'username' ],
                #1.2.3 Call the password_hash method on the new user and set it to the password from the request
                password_hash = rq[ 'password' ]
            )

            if new_user.validation_errors :
                raise ValueError
            
            #1.2.4 Add and commit
            db.session.add( new_user )
            db.session.commit()

            #1.2.5 Add the user id to session under the key of user_id
            session[ 'user_id' ] = new_user.id

            #1.2.6 send the new user back to the client with a status of 201
            return new_user.to_dict(), 201
        except :
            errors = new_user.validation_errors
            new_user.clear_validation_errors()
            return { 'errors': errors }, 422
    #1.3 Test out your route with the client or Postman

    #1.1 Use add_resource to add a new endpoint '/signup' 
api.add_resource( Signup, '/signup', endpoint = 'signup' )

# 2.✅ Test this route in the client/src/components/Authentication.sj 

# 3.✅ Create a Login route
class Login ( Resource ) :
    def post ( self ) :
        username = request.get_json()[ 'username' ]
        password = request.get_json()[ 'password' ]

        user = User.query.filter( User.username.like( f'{ username }' ) ).first()

        if user and user.authenticate( password ) :
            session[ 'user_id' ] = user.id
            # print( session[ 'user_id' ] )
            return user.to_dict(), 200
        else :
            return { 'errors':['Invalid username or password.'] }, 401

api.add_resource( Login, '/login', endpoint = 'login' )


# 4.✅ Create an AutoLogin class that inherits from Resource
    # 4.1 use api.add_resource to add an automatic login route
    # 4.2 Create a get method
        # 4.2.1 Access the user_id from session with session.get
        # 4.2.2 Use the user id to query the user with a .filter
        # 4.2.3 If the user id is in sessions and found make a response to send to the client. else raise the Unauthorized exception
class AutoLogin ( Resource ) :
    def get ( self ) :
        if session[ 'user_id' ] :
            user = User.find_by_id( session[ 'user_id' ] )
            if user :
                return user.to_dict(), 200
            else :
                return { 'errors': ['User not found.'] }, 404
        else :
            return {}, 204

api.add_resource( AutoLogin, '/auto_login' )
# 5.✅ Head back to client/src/App.js and try refreshing the page and checking if the user stays logged in...

# 6.✅ Logout 
    # 6.1 Create a class Logout that inherits from Resource 
    # 6.2 Create a method called delete
    # 6.3 Clear the user id in session by setting the key to None
    # 6.4 create a 204 no content response to send back to the client
class Logout ( Resource ) :
    def delete ( self ) :
        session[ 'user_id' ] = None
        return {}, 204
    
api.add_resource( Logout, '/logout' )

# 7.✅ Navigate to client/src/components/Navigation.js to build the logout button!


class Productions(Resource):
    def get(self):
        return Production.all(), 200

    def post(self):
        if session[ 'user_id' ] :
            rq = request.get_json()
            try :
                new_prod = Production(
                    title=rq['title'],
                    genre=rq['genre'],
                    budget=int(rq['budget']),
                    image=rq['image'],
                    director=rq['director'],
                    description=rq['description']
                )
            
                if new_prod.validation_errors :
                    raise ValueError
                
                db.session.add( new_prod )
                db.session.commit()
                return new_prod.to_dict(), 201
            
            except :
                errors = new_prod.validation_errors
                new_prod.clear_validation_errors()
                return { 'errors': errors }, 422
        else :
            return { 'errors': ['You must be logged in to do that action.'] }, 401

api.add_resource(Productions, '/productions')


class ProductionByID(Resource):
    def get(self,id):
        prod = Production.find_by_id( id )
        if prod:
            return prod.to_dict(), 200
        else :
            return { 'errors': ['Production not found.'] }, 404

    def patch(self, id):
        if session[ 'user_id' ] :
            prod = Production.find_by_id( id )
            if prod:
                try:
                    for attr in request.form:
                        setattr(prod, attr, request.form[attr])

                    prod.ongoing = bool(request.form['ongoing'])
                    prod.budget = request.form['budget']

                    if prod.validation_errors :
                        raise ValueError
                    
                    db.session.add( prod )
                    db.session.commit()
                    return prod.to_dict(), 200
                
                except :
                    errors = prod.validation_errors
                    prod.clear_validation_errors()
                    return { 'errors': errors }, 422
            else :
                return { 'errors': ['Production not found.'] }, 404
        else :
            return { 'errors': ['You must be logged in to do that action.'] }, 401

    def delete(self, id):
        if session[ 'user_id' ] :
            prod = Production.find_by_id( id )
            if prod :
                for cm in prod.cast :
                    db.session.delete( cm )
                db.session.delete( prod )
                db.session.commit()
                return {}, 204
            else :
                return { 'errors': ['Production not found.'] }, 404
        else :
            return { 'errors': ['You must be logged in to do that action.'] }, 401

api.add_resource(ProductionByID, '/productions/<int:id>')

class PostById ( Resource ) :
    def patch ( self, id ) :
        # check to see if there is a user and the post is there's
        if session[ 'user_id' ] and session[ 'user_id' ] == post.user_id :
            post = Post.query.get( id )
        
# @app.errorhandler(NotFound)
# def handle_not_found(e):
#     response = make_response(
#         "Not Found: Sorry the resource you are looking for does not exist",
#         404
#     )

#     return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)