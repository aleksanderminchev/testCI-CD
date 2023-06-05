
from tkinter import W
import numpy as np
import matplotlib as mpl
import pandas as pd
from io import StringIO
import csv


def createCSV(teachers, wagepayments, start_date, end_date):
    pdTeachers = pd.array([{"Id": i.id,
                           "First name": i.user.first_name,
                            "Last name": i.user.last_name,
                            'Email': i.user.email,
                            'Bank Number': i.bank_number,
                            'Reg number': i.reg_number,
                            'CPR': i.payroll_id}for i in teachers])
    pdWages = pd.array([{'Id': i.teacher_id,
                        'Earnings from lessons': i.amount-i.referrals_amount,
                         'Number of Lessons': i.hours,
                         'Number of Referrals': i.referrals_number,
                         'Earnings from other compensation': i.referrals_amount+0,
                         'Total earnings': i.amount+0} for i in wagepayments])
    teachersData = pd.DataFrame(pdTeachers)
    wagesDate = pd.DataFrame(pdWages)
    merger = teachersData.merge(
        wagesDate, left_on='Id', right_on='Id', sort=True)
    merger = merger.sort_values('Id')
    print(teachersData)
    print(merger)
    merger.to_excel(f'wages_{start_date}_{end_date}.xlsx', sheet_name='Wages')


def generate_excell_response():
    data = StringIO()
    w = csv.writer(data)
    pd.ExcelWriter()
    # write header
    w.writerow(('Id',
                'First name',
                'Last name',
                'Email',
                'Bank Number',
                'Reg Number',
                'CPR',
                'Earnings from lessons',
                'Number of Lessons',
                'Number of Referrals'
                'Earnings from other compensation',
                'Total earnings'))
    yield data.getvalue()
    data.seek(0)
    data.truncate(0)
    # write each log item
    file_data = pd.read_excel('wages.xlsx')
    file_data = file_data.drop('Unnamed: 0', axis=1)
    array = file_data.to_numpy()
    print(array)
    for item in array:
        print(item)
        w.writerow((
            item  # format datetime as string

        ))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
