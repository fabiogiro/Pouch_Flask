import config

app = config.app
db = config.db


class Company(db.Model):
    __tablename__ = 'Company'
    id = db.Column(db.Integer, primary_key=True)
    codesynd = db.Column(db.Integer, nullable=False)
    codecomp = db.Column(db.Integer, nullable=False)
    namecomp = db.Column(db.String(50), nullable=False)

    def __init__(self, codesynd, codecomp, namecomp):
        self.codesynd = codesynd
        self.codecomp = codecomp
        self.namecomp = namecomp


def findall():
    return Company.query.filter_by().order_by('codesynd', 'codecomp')


def findone(id):
    return Company.query.get(id)


def findcodesyndcomp(codesynd, codecomp):
    return Company.query.filter_by(codesynd=codesynd, codecomp=codecomp).first()


def insert(codesynd, codecomp, namecomp):
    try:
        comp = Company(codesynd, codecomp, namecomp)
        db.session.add(comp)
        db.session.commit()
        return ''
    except Exception as error:
        return f'Error: {error.__class__}'


def edit(comp, namecomp):
    try:
        comp.namecomp = namecomp
        db.session.commit()
        return ''
    except Exception as error:
        return f'Error: {error.__class__}'


def delete(comp):
    try:
        db.session.delete(comp)
        db.session.commit()
        return ''
    except Exception as error:
        return f'Error: {error.__class__}'
