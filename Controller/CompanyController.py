from Models.CompanyModel import findcodesyndcomp
from Controller import utils


def criticacodecomp(codesynd: int, codecomp) -> str:
    message = utils.criticaint(codecomp,'Code')
    if message == '':
        result = findcodesyndcomp(codesynd, codecomp)
        if result != None:
            message = f'Syndicate {codesynd} - Company {codecomp} already exist'
    return message
