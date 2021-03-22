from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

database = 'sqlite:///POUCH.db'
app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

migarate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#Console
# python3 app.py db init
# python3 app.py db migrate
# python3 app.py db upgrade

# python3 app.py db makemigrations
# python3 app.py db migrate

engine = create_engine(database, connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
session = Session()
