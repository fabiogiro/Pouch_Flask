import config

db = config.db
app = config.app


class Syndicate(db.Model):
    __tablenamw__ = 'Syndicate'
    id = db.Column(db.Integer, primary_key=True)
    codesynd = db.Column(db.Integer,  unique=True, nullable=False)
    namesynd = db.Column(db.String(20), nullable=False)

    def __init__(self, codesynd, namesynd):
        self.codesynd = codesynd
        self.namesynd = namesynd


def createclass():
    db.create_all()


def findall():
    return Syndicate.query.filter_by().order_by('codesynd')


def findone(id):
    return Syndicate.query.get(id)


def findcodesynd(codesynd):
    return Syndicate.query.filter_by(codesynd=codesynd).first()


def insert(codesynd, namesynd):
    try:
        synd =Syndicate(codesynd, namesynd)
        db.session.add(synd)
        db.session.commit()
        return ''
    except Exception as error:
        return f'Error: {error.__class__}'


def edit(synd, namesynd):
    try:
        synd.namesynd = namesynd
        db.session.commit()
        return ''
    except Exception as error:
        return f'Error: {error.__class__}'


def delete(synd):
    try:
        db.session.delete(synd)
        db.session.commit()
        return ''
    except Exception as error:
        return f'Error: {error.__class__}'
