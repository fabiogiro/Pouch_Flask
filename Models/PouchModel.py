import config
from Controller.utils import first_last_day

app = config.app
db = config.db
engine = config.engine
session = config.session


class Pouch(db.Model):
    __tablename__ = 'Pouch'
    id = db.Column(db.Integer, primary_key=True)
    codepouch = db.Column(db.String(10), unique=True, nullable=False, index=True)
    dtarrived = db.Column(db.String(10), nullable=False, index=True)
    codecard = db.Column(db.Integer, nullable=False)
    codesynd = db.Column(db.Integer, nullable=False)
    codecomp = db.Column(db.Integer, nullable=False)
    quant = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, codepouch, dtarrived, codecard, codesynd, codecomp, quant, value):
        self.codepouch = codepouch
        self.dtarrived = dtarrived
        self.codecard = codecard
        self.codesynd = codesynd
        self.codecomp = codecomp
        self.quant = quant
        self.value = value


def findall():
    return Pouch.query.filter_by().order_by('codepouch')


def findone(id):
    return Pouch.query.get(id)


def findcodepouch(codepouch):
    return Pouch.query.filter_by(codepouch=codepouch).first()


def finddtarrived(dtarrived):
    return Pouch.query.filter_by(dtarrived=dtarrived).order_by('codepouch')


def countcodepouchcard(codecard: str) -> int:
    sql = f'SELECT COUNT(CODEPOUCH) FROM POUCH WHERE CODECARD = {codecard}'

    data = session.execute(sql)
    for reg in data:
        return reg[0]
    return 0


def countcodepouchsynd(codesynd: str) -> int:
    sql = f'SELECT COUNT(CODEPOUCH) FROM POUCH WHERE CODESYND = {codesynd}'

    data = session.execute(sql)
    for reg in data:
        return reg[0]
    return 0


def countcodepouchcomp(codecomp: str) -> int:
    sql = f'SELECT COUNT(CODEPOUCH) FROM POUCH WHERE CODECOMP = {codecomp}'

    data = session.execute(sql)
    for reg in data:
        return reg[0]
    return 0


def getdataanalysis(dtini: str, dtfinal: str, optiondate: str) -> tuple:
    sql = f'SELECT DISTINCT(DTARRIVED), AVG(QUANT) AS TOTQUANT, AVG(VALUE) AS TOTVALUE' \
          ' FROM POUCH' \
          f' WHERE DTARRIVED BETWEEN "{str(dtini)}" AND "{str(dtfinal)}"'
    sql = sql + ' GROUP BY DTARRIVED'
    sql = sql + ' ORDER BY DTARRIVED'

    data = session.execute(sql)

    lstdate = []
    lstquant = []
    lstvalue = []

    month = int(dtini[5:7])
    year = int(dtini[:4])

    if optiondate == 'monthyear''':
        dt1, dt2 = first_last_day(month, year)
        dt2_str = dt2.strftime('%Y-%m-%d')  # convert date to str
        maxday = int(dt2_str[-2::])
        # initialize the list
        for i in range(0, maxday):
            lstdate.append(0)
            lstquant.append(0)
            lstvalue.append(0)
    elif optiondate == 'year':
        # initialize the list
        for i in range(0, 366):
            lstdate.append(0)
            lstquant.append(0)
            lstvalue.append(0)

    i = 0
    for reg in data:
        daymonth = 0
        if optiondate == 'monthyear':
            daymonth = int(reg[0][-2::])
            # lstdate.append(int(reg[0][-2::]))  # day 2020-01-20  -> 20
        elif optiondate == 'year':
            daymonth = int(reg[0][5:7])  # month 2020-01-20  -> 01
            # lstdate.append(int(reg[0][5:7]))  # month 2020-01-20  -> 01
        lstdate[i] = daymonth
        lstquant[i] = reg[1]
        lstvalue[i] = reg[2]

        i += 1

    return lstdate, lstquant, lstvalue


def insert(codepouch, dtarrived, codecard, codesynd, codecomp, quant, value):
    try:
        pouch = Pouch(codepouch, dtarrived, codecard, codesynd, codecomp, quant, value)
        db.session.add(pouch)
        db.session.commit()
        return ''
    except Exception as error:
        return f'Error: {error.__class__}'


def edit(pouch, dtarrived, quant, value):
    try:
        pouch.dtarrived = dtarrived
        pouch.quant = quant
        pouch.value = value
        db.session.commit()
        return ''
    except Exception as error:
        return f'Error: {error.__class__}'


def delete(pouch):
    try:
        db.session.delete(pouch)
        db.session.commit()
        return ''
    except Exception as error:
        return f'Error: {error.__class__}'
