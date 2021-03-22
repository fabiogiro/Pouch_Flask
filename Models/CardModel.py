import config

db = config.db
app = config.app


class Card(db.Model):
    __tablenamw__ = 'Card'
    id = db.Column(db.Integer, primary_key=True)
    codecard = db.Column(db.Integer,  unique=True, nullable=False)
    namecard = db.Column(db.String(20), nullable=False)

    def __init__(self, codecard, namecard):
        self.codecard = codecard
        self.namecard = namecard


def createclass():
    db.create_all()


def findall():
    return Card.query.filter_by().order_by('codecard')


def findone(id):
    return Card.query.get(id)


def findcodecard(codecard) -> str:
    return Card.query.filter_by(codecard=codecard).first()


def insert(codecard, namecard):
    try:
        card = Card(codecard, namecard)
        db.session.add(card)
        db.session.commit()
        return ''
    except Exception as error:
        return f'Error: {error.__class__}'


def edit(card, namecard):
    try:
        card.namecard = namecard
        db.session.commit()
        return ''
    except Exception as error:
        return f'Error: {error.__class__}'


def delete(card):
    try:
        db.session.delete(card)
        db.session.commit()
        return ''
    except Exception as error:
        return f'Error: {error.__class__}'
