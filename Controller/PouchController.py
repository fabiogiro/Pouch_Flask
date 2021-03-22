from Controller.utils import date_valid
from Models.PouchModel import findcodepouch
from Models import PouchModel


def criticasearch(field: str) -> str:
    if field.strip() == '':
        return 'Data Arrived is empty'
    if not date_valid(field):
        return 'Date invalid'


def criticacodepouch(codepouch: str) -> str:
    message = ''
    result = findcodepouch(codepouch)
    if result != None:
        message = f'Code {codepouch} already exist'
    return message


def search(field: str) -> tuple:
    message = criticasearch(field)
    pouchs = ''
    if message == '' or message == None:
        dtarrived = field[6:] + '-' + field[3:5] + '-' + field[:2]
        pouchs = PouchModel.finddtarrived(dtarrived)
        if pouchs == None:
            message = 'Date Arrived not found'
    return message, pouchs
