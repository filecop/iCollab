from flask import Flask
from flask_restful import Api
from backend.models import *



def init_app():
    iCollab = Flask(__name__)  # Object of Flask
    iCollab.debug = True
    iCollab.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///SnIappDB.sqlite3"
    iCollab.app_context().push()
    db.init_app(iCollab)
    db.create_all()
    return iCollab
app=init_app()


api = Api(app)
from apis import *
api.add_resource(GetCampaign, '/get/campaign/<int:campaignid>')
api.add_resource(CreateCampaign, '/create/campaign')
api.add_resource(GetUser, '/get/user/<int:userid>')


from backend.controllers import *

if __name__=="__main__":
    app.run(debug=True)
