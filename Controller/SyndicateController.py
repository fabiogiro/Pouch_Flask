from Models.SyndicateModel import findcodesynd
from Controller import utils


def criticacodesynd(codesynd: int) -> str:
    message = utils.criticaint(codesynd,'Code')
    if message == '':
        result = findcodesynd(codesynd)
        if result != None:
            message = f'Code {codesynd} already exist'
    return message
