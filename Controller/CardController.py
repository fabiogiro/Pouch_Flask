from Models.CardModel import findcodecard
from Controller import utils


def criticacodecard(codecard: str) -> str:
    message = utils.criticaint(codecard, 'Code')
    if message == '':
        result = findcodecard(codecard)
        if result != None:
            message = f'Code {codecard} already exist'
    return message
