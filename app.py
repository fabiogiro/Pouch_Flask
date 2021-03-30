from flask import render_template, redirect, url_for, request, flash
from Models import CardModel, SyndicateModel, CompanyModel, PouchModel
import config
from Models.SyndicateModel import Syndicate
from Models.PouchModel import countcodepouchcard, countcodepouchsynd, countcodepouchcomp
from Controller import CardController, SyndicateController, CompanyController, \
                       PouchController, utils
from fpdf import FPDF
from datetime import datetime
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt

app = config.app
db = config.db


@app.route('/')
def index():
    return render_template('MainMenu.html')


@app.route('/card_menu')
def card_menu():
    cards = CardModel.findall()
    return render_template('Card/menu.html', cards=cards)


@app.route('/card_insert', methods=['GET', 'POST'])
def card_insert():
    flash('')
    if request.method == 'POST':
        message = CardController.criticacodecard(request.form['codecard'])
        if message.strip() == '':
            if request.form['namecard'].strip() == '':
                message = 'Name is empty'
            else:
                message = CardModel.insert(request.form['codecard'], request.form['namecard'])
                if message.strip() == '':
                    return redirect(url_for('card_menu'))
        flash(message)
    return render_template('Card/insert.html')


@app.route('/card_edit/<int:id>', methods=['GET', 'POST'])
def card_edit(id: int):
    flash('')
    card = CardModel.findone(id)
    if request.method == 'POST':
        if request.form['namecard'].strip() == '':
            message = 'Name is empty'
        else:
            message = CardModel.edit(card, request.form['namecard'])
            if message.strip() == '':
                return redirect(url_for('card_menu'))
        flash(message)
    return render_template('Card/edit.html', card=card)


@app.route('/card_delete/<int:id>', methods=['GET', 'POST'])
def card_delete(id: int):
    flash('')
    card = CardModel.findone(id)
    if request.method == 'POST':
        message = CardModel.delete(card)
        if message.strip() == '':
            return redirect(url_for('card_menu'))
        flash(message)
        return redirect(url_for('card_menu'))
    countcodepouch = countcodepouchcard(card.codecard)

    if countcodepouch > 0:
        flash('Have Pouch registered')
        return redirect(url_for('card_menu'))
    return render_template('Card/delete.html', card=card)


@app.route('/synd_menu')
def synd_menu():
    synds = SyndicateModel.findall()
    return render_template('Syndicate/menu.html', synds=synds)


@app.route('/synd_insert', methods=['GET', 'POST'])
def synd_insert():
    flash('')
    if request.method == 'POST':
        message = SyndicateController.criticacodesynd(request.form['codesynd'])
        if message.strip() == '':
            if request.form['namesynd'].strip() == '':
                message = 'Name is empty'
            else:
                message = SyndicateModel.insert(request.form['codesynd'], request.form['namesynd'])
                if message.strip() == '':
                    return redirect(url_for('synd_menu'))
        flash(message)
    return render_template('Syndicate/insert.html')


@app.route('/synd_edit/<int:id>', methods=['GET', 'POST'])
def synd_edit(id: int):
    flash('')
    synd = SyndicateModel.findone(id)
    if request.method == 'POST':
        if request.form['namesynd'].strip() == '':
            message = 'Name is empty'
        else:
            message = SyndicateModel.edit(synd, request.form['namesynd'])
            if message.strip() == '':
                return redirect(url_for('synd_menu'))
        flash(message)
    return render_template('Syndicate/edit.html', synd=synd)


@app.route('/synd_delete/<int:id>', methods=['GET', 'POST'])
def synd_delete(id: int):
    flash('')
    synd = SyndicateModel.findone(id)
    if request.method == 'POST':
        message = SyndicateModel.delete(synd)
        if message.strip() == '':
            return redirect(url_for('synd_menu'))
        flash(message)
        return redirect(url_for('synd_menu'))
    countcodepouch = countcodepouchsynd(synd.codesynd)

    if countcodepouch > 0:
        flash('Have Pouch registered')
        return redirect(url_for('synd_menu'))
    return render_template('Syndicate/delete.html', synd=synd)


@app.route('/comp_menu')
def comp_menu():
    comps = CompanyModel.findall()
    return render_template('Company/menu.html', comps=comps)


@app.route('/comp_insert', methods=['GET', 'POST'])
def comp_insert():
    flash('')
    if request.method == 'POST':
        message = CompanyController.criticacodecomp(request.form['codesynd'],
                                                    request.form['codecomp'])
        if message == '':
            if request.form['namecomp'].strip() == '':
                message = 'Name is empty'
            else:
                message = CompanyModel.insert(request.form['codesynd'], request.form['codecomp'],
                                    request.form['namecomp'])
                if message.strip() == '':
                    return redirect(url_for('comp_menu'))
        flash(message)

    result = SyndicateModel.findall()
    if result == '' or result is None:
        flash('Don´t have Syndicate registred')
        return redirect(url_for('comp_menu'))
    synds: Syndicate = SyndicateModel.findall()
    return render_template('Company/insert.html', synds=synds)


@app.route('/comp_edit/<int:id>', methods=['GET', 'POST'])
def comp_edit(id: int):
    flash('')
    comp = CompanyModel.findone(id)
    if request.method == 'POST':
        if request.form['namecomp'].strip() == '':
            message = 'Name is empty'
        else:
            message = CompanyModel.edit(comp, request.form['namecomp'])
            if message.strip() == '':
                return redirect(url_for('comp_menu'))
        flash(message)
    return render_template('Company/edit.html', comp=comp)


@app.route('/comp_delete/<int:id>', methods=['GET', 'POST'])
def comp_delete(id: int):
    flash('')
    comp = CompanyModel.findone(id)
    if request.method == 'POST':
        message = CompanyModel.delete(comp)
        if message.strip() == '':
            return redirect(url_for('comp_menu'))
        flash(message)
        return redirect(url_for('comp_menu'))
    countcodepouch = countcodepouchcomp(comp.codecomp)

    if countcodepouch > 0:
        flash('Have Pouch registered')
        return redirect(url_for('comp_menu'))
    return render_template('Company/delete.html', comp=comp)


@app.route('/search_pouch', methods=['GET', 'POST'])
def searchpouch():
    if request.method == 'POST':
        message, pouchs = PouchController.search(request.form['searchfield'])
        if message == None:
            return render_template('Pouch/menu.html', pouchs=pouchs)

        flash(message)
    return render_template('Pouch/search.html')


@app.route('/pouch_menu')
def pouch_menu():
    pouchs = PouchModel.findall()
    return render_template('Pouch/menu.html', pouchs=pouchs)


@app.route('/pouch_insert', methods=['GET', 'POST'])
def pouch_insert():
    flash('')
    if request.method == 'POST':
        if request.form['codepouch'].strip() == '':
            message = 'Code is empty'
        else:
            message = PouchController.criticacodepouch(request.form['codepouch'].strip().upper())
            if message.strip() == '':
                result = CompanyModel.findcodesyndcomp(request.form['codesynd'],
                                                       request.form['codecomp'])
                if result == None:
                    codesynd = request.form['codesynd']
                    codecomp = request.form['codecomp']
                    message = f"Don't have Company {codecomp} with this Syndicate {codesynd}"
                else:
                    message = utils.date_valid(request.form['dtarrived'])
                    if message == None:
                        message = utils.criticaint(request.form['quant'], 'Quant')
                        if message.strip() == '':
                            message = utils.criticaint(request.form['value'], 'Value')
                            if message.strip() == '':
                                message = PouchModel.insert(request.form['codepouch'].upper(),
                                                            request.form['dtarrived'],
                                                            request.form['codecard'],
                                                            request.form['codesynd'],
                                                            request.form['codecomp'],
                                                            request.form['quant'],
                                                            request.form['value'])
                                if message.strip() == '':
                                    pouchs = PouchModel.finddtarrived(request.form['dtarrived'])
                                    return render_template('Pouch/menu.html', pouchs=pouchs)
        flash(message)
    cards: CardModel.Card = CardModel.findall()
    synds : SyndicateModel.Syndicate = SyndicateModel.findall()
    comps: CompanyModel.Company = CompanyModel.findall()
    return render_template('Pouch/insert.html', cards=cards, synds=synds, comps=comps)


@app.route('/pouch_edit/<int:id>', methods=['GET', 'POST'])
def pouch_edit(id: int):
    flash('')
    pouch = PouchModel.findone(id)
    if request.method == 'POST':
        message = utils.date_valid(request.form['dtarrived'])
        if message.strip() == '':
            message = utils.criticaint(request.form['quant'], 'Quant')
            if message.strip() == '':
                message = utils.criticaint(request.form['value'], 'Value')
                if message.strip() == '':
                    dtarrived = request.form['dtarrived']
                    message = PouchModel.edit(pouch, request.form['dtarrived'],
                                                     request.form['quant'],
                                                     request.form['value'])
                    if message.strip() == '':
                        pouchs = PouchModel.finddtarrived(dtarrived)
                        return render_template('Pouch/menu.html', pouchs=pouchs)
        flash(message)
    return render_template('Pouch/edit.html', pouch=pouch)


@app.route('/pouch_delete/<int:id>', methods=['GET', 'POST'])
def pouch_delete(id: int):
    flash('')
    pouch = PouchModel.findone(id)
    dtarrived = pouch.dtarrived
    if request.method == 'POST':
        message = PouchModel.delete(pouch)
        if message.strip() == '':
            pouchs = PouchModel.finddtarrived(dtarrived)
            return render_template('Pouch/menu.html', pouchs=pouchs)
        flash(message)
    return render_template('Pouch/delete.html', pouch=pouch)


@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        field = request.form['searchfield']
        dtarrived = field[6:] + '-' + field[3:5] + '-' + field[:2]

        message = utils.date_valid(dtarrived)

        if message == None:
            message, pouchs = PouchController.search(request.form['searchfield'])
            data = pouchs

            if message == None:
                searchfield = request.form['searchfield']

                filepdf = FPDF('P', 'mm', 'A4')  # Portrait

                filepdf.add_page()
                filepdf.set_font('Arial', '', 10)
                filepdf.cell(190, 4, 'Página ' + str(filepdf.page_no()), 0, 1, 'R')
                filepdf.set_font('Arial', 'B', 16)
                filepdf.cell(190, 4, 'Date Arrived Report - ' + searchfield +
                             '          ' + datetime.strftime(datetime.today().now(),
                                                        '%d/%m/%Y %H:%M'), 0, 1, 'C')
                filepdf.set_font('Courier', '', 10)
                filepdf.cell(190, 4, ' ', 0, 1, 'R')
                # 60 = weight 20 = height by cell 0 = border 1 = break line L = align
                subtitle = '   Date    Pouch      Card       Syndicate       ' \
                           'Company        Quant  Value'
                filepdf.set_font('Courier', '', 10)
                filepdf.cell(190, 4, subtitle, 0, 1, 'L')
                contline = 2
                for reg in data:
                    dtarrive = reg.dtarrived[:2] + '/' + reg.dtarrived[5:7] + '/' \
                               + reg.dtarrived[0:4]
                    codepouch = reg.codepouch
                    codecard = reg.codecard
                    codesynd = reg.codesynd
                    codecomp = reg.codecomp
                    quant = reg.quant
                    value = reg.value

                    if contline > 59:
                        filepdf.add_page()
                        filepdf.set_font('Arial', '', 10)
                        filepdf.cell(190, 4, 'Page ' + str(filepdf.page_no()), 0, 1, 'R')
                        subtitle = '   Date    Pouch      Card       Syndicate       Company        ' \
                                   'Quant  Value'
                        filepdf.set_font('Courier', '', 10)
                        filepdf.cell(190, 4, subtitle, 0, 1, 'L')
                        contline = 2

                    contline += 1

                    filepdf.cell(210, 4, f'{dtarrive:} {codepouch:<10} {codecard:<10} '
                                         f'{codesynd:<15} {codecomp:<15} {quant:>4} '
                                         f'{value:>6.2f}', 0, 1, 'L')
                try:
                    dtarrived = searchfield[6:] + '-' + searchfield[3:5] + '-' + searchfield[:2]
                    filepdf.output(f'ReportPouch_{dtarrived}.pdf', 'F')  # D - Web   F- Local
                    message = 'Generated Report'
                except Exception:
                    message =  'The file pdf is open'
        flash(message)
    return render_template('Report/search.html')


def getparameters(optiondate: str, option: str, searchfield: str) -> str:
    year = searchfield[-4:]

    message = ''

    if optiondate == 'monthyear':
        month = searchfield[:2]
        dtini, dtfinal = utils.first_last_day(int(month), int(year))

        # lstdate, lstquant, lstvalue = PouchModel.getdataanalysis(dtini, dtfinal, 'monthyear')
        npday, npquant, npvalue = PouchModel.getdataanalysis(dtini, dtfinal, 'monthyear')

        # if len(lstdate) > 0:
        if utils.founddata(npday):
            x = npday  # lstdate
            ylabel = ''

            if option == 'quant':
                y = npquant  # lstquant
                ylabel = 'Quant'
#                plt.bar(x, y, label='QUANT', color='g')
                plt.bar(x, y, color='g')
            elif option == 'value':
                y = npvalue  # lstvalue
                ylabel = 'Value'
#                plt.bar(x, y, label='VALUE', color='b')
                plt.bar(x, y, color='b')

            plt.xlabel('Day')
            plt.ylabel(ylabel)
            plt.title(f'{str(month):0>2}/{str(year)}')
            plt.grid(True)
#            plt.legend()
#            plt.show()
            # https://www.youtube.com/watch?v=cXlMfA7aH1U
            plt.savefig(f'{str(year)}_{str(month):0>2}_{ylabel}.pdf', format='pdf',
                        transparent=True, bbox_inches='tight')
            message = f'Report {str(year)}_{str(month):0>2}_{ylabel}.pdf saved'
        else:
            message = "Don´t have register"

    if optiondate == 'year':
        message = processyear(int(year), option)

    return message


def processyear(year: int, option: str):
    npmonth = np.zeros(12)
    npquant = np.zeros(12)
    npvalue = np.zeros(12)

    dtini = str(year) + '-01-01'
    dtfinal = str(year) + '-12-31'

    # lstdate, lstquant, lstvalue = PouchModel.getdataanalysis(dtini, dtfinal, 'year')
    npmonth, npquant, npvalue = PouchModel.getdataanalysis(dtini, dtfinal, 'year')

    if utils.founddata(npmonth):
    # if len(lstdate) > 0:
        # dct = {'month': lstdate, 'quant': lstquant, 'value': lstvalue}
        dct = {'month': npmonth, 'quant': npquant, 'value': npvalue}

        frame = DataFrame(dct)
        # group by from pandas is slower than group by from database
        if option == 'quant':
            frame.groupby(by='month')['quant'].mean()
        else:
            frame.groupby(by='month')['value'].mean()

        x = frame['month']
        ylabel = ''

        #    countmonth = 0
        #    totquant = 0
        #    totvalue = 0
        #    month = 0
        #
        #    for count in range(1, len(lstdate)):
        #        monthactual = lstdate[count]
        #        if month == 0:   # first time
        #            month = monthactual
        #        if month != monthactual:
        #            npmonth[month - 1] = month
        #            npquant[month - 1] = round(totquant / countmonth)
        #            npvalue[month - 1] = round(totvalue / countmonth)
        #
        #            month = monthactual
        #
        #            countmonth = 0
        #            totquant = 0
        #            totvalue = 0
        #
        #        countmonth += 1
        #        totquant += lstquant[count]
        #        totvalue += lstvalue[count]
        #
        #    npmonth[month - 1] = month
        #    npquant[month - 1] = round(totquant / countmonth)
        #    npvalue[month - 1] = round(totvalue / countmonth)
        #
        #    x = npmonth
        #
        #    if option == 1:
        #        y = npquant
        #        plt.bar(x, y, label='QUANT', color='g')
        #    elif option == 2:
        #        y = npvalue
        #        plt.bar(x, y, label='VALUE', color='b')

        if option == 'quant':
            y = frame['quant']
            ylabel = 'Quant'
#            plt.bar(x, y, label='QUANT', color='g')
            plt.bar(x, y, color='g')
        elif option == 'value':
            y = frame['value']
            ylabel = 'Value'
#            plt.bar(x, y, label='VALUE', color='b')
            plt.bar(x, y, label='VALUE', color='b')

        plt.xlabel('Month')
        plt.ylabel(ylabel)
        plt.title(str(year))
        plt.grid(True)
#        plt.legend()
#        plt.show()
        plt.savefig(f'{str(year)}_{ylabel}.pdf', format='pdf', transparent=True,
                    bbox_inches='tight')
        return f'Report {str(year)}_{ylabel}.pdf saved'
    else:
        return "Don´t have register"


@app.route('/dataanalysis', methods=['GET', 'POST'])
def dataanalysis():
    flash('')
    if request.method == 'POST':
        field = request.form['searchfield']

        optiondate = request.form['optiondate']
        if optiondate == 'monthyear':
            dtarrived = field[-4:] + '-' + field[:2] + '-01'
        else:
            dtarrived = field + '-01-01'

        message = utils.date_valid(dtarrived)

        if message == None:
            option = request.form['option']

            message = getparameters(optiondate, option, request.form['searchfield'])
        flash(message)
    return render_template('DataAnalysis/search.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
