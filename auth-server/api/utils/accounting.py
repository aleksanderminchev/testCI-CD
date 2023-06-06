from flask import send_file
import pandas as pd
from models.customer import Customer
from api.app import db
from dateutil.relativedelta import relativedelta
from datetime import datetime


def send_excel_file_accounting(name):
    """Sends the accounting file"""
    return send_file(f'D:\\Work\\TopTutors\\toptutors-flask-react-app\\toptutors-api\\{name}')


def export_data_to_excel(data, date_check):
    """Creates the excel file"""
    date_requested = date_check.strftime("%Y-%m-%d")
    columnNames = ['ID', 'Customer Name',
                   'Email',
                   'Net Payments',
                   "Revenue",
                   "Balance",
                   "Prepayments",
                   "Receivables",
                   "Total Bookings Value"]
    dataframe = pd.DataFrame(data, columns=columnNames)
    dataframe.to_excel(f'Accounting_{date_requested}.xlsx')
    return f'Accounting_{date_requested}.xlsx'


def calculate_balances(date):
    """
    Calculates individual balance for every customer account
    """
    try:
        date_check = date
        date_check = date_check.replace(hour=23, minute=59, second=59)
        customers = Customer.query.all()

        all_data = []
        for customer in customers:
            if customer.created_at <= date_check:
                id = customer.id
                net_payment = calculate_net_payment(customer, date_check)
                average_hourly_price = calculate_average_hourly_price(customer,
                                                                      date_check)
                accrued_hours = get_accrued_hours(customer, date_check)
                """Revenue formula is
                net_revenue = average_hourly_price * accrued_hours"""
                net_revenue = average_hourly_price['average_hourly_price'] * \
                    accrued_hours
                """Total balance formulat is
                accrual_balance = net_payment - net_revenue
                """
                accrual_balance = net_payment - net_revenue
                """For prepayments and receivables we check 
                if the balance total is positive or negative"""
                prepayments = 1
                receivables = 0
                if accrual_balance < 0:
                    receivables = 1
                    prepayments = 0
                elif accrual_balance == 0:
                    prepayments = 0
                    receivables = 0
                row = {"ID": id,
                       "Customer Name": f'{customer.user.first_name} {customer.user.last_name}',
                       "Email": customer.user.email,
                       "Net Payments": net_payment,
                       "Revenue": net_revenue,
                       "Balance": accrual_balance,
                       "Prepayments": prepayments,
                       "Receivables": receivables,
                       "Total Bookings Value": average_hourly_price['total_orders']}
                all_data.append(row)

        return all_data
    except Exception as e:
        raise ValueError('invalid date or data')


def calculate_revenue_generated(start_date, end_date):
    """Calculates the revenue generated for each customer
    between the 2 dates, used for yearly review"""
    try:
        initial_balance = calculate_balances(start_date)
        final_balance = calculate_balances(end_date)
        columnNames = ['ID', 'Customer Name',
                       'Email',
                       'Net Payments',
                       "Revenue",
                       "Balance",
                       "Prepayments",
                       "Receivables",
                       "Total Bookings Value"]
        y_string = start_date.strftime("%Y-%m-%d")
        x_string = end_date.strftime("%Y-%m-%d")
        initial_dataframe = pd.DataFrame(initial_balance, columns=columnNames)
        final_dataframe = pd.DataFrame(final_balance, columns=columnNames)
        merged_dataframe = final_dataframe.merge(initial_dataframe,
                                                 on=['ID', 'Customer Name',
                                                     "Email"],
                                                 how='outer').drop_duplicates(['ID', 'Customer Name', 'Email'])
        merged_dataframe['Diffrence in revenue'] = merged_dataframe['Revenue_x'] - \
            merged_dataframe['Revenue_y']
        merged_dataframe.rename(columns={"Revenue_x": f"Revenue until {x_string}",
                                "Revenue_y": f"Revenue until{y_string}",
                                         "Balance_x": f"Balance until{x_string}",
                                         "Balance_y": f"Balance until{y_string}",
                                         "Net Payments_x": f"Net Payments until {x_string}",
                                         "Net Payments_y": f"Net Payments until {y_string}"},
                                inplace=True)
        merged_dataframe.drop(['Prepayments_x',
                               'Prepayments_y',
                               "Receivables_x",
                               "Receivables_y",
                               "Total Bookings Value_x",
                               "Total Bookings Value_y"], axis=1, inplace=True)
        # merged_dataframe.to_excel('merge.xlsx')
        return final_balance
    except Exception as e:
        raise ValueError('invalid date or data')


def calculate_net_payment(customer, date_check):
    """Calculates the net payments
    net_payment= payments-refunds
    """
    if not isinstance(date_check, datetime):
        raise ValueError("Invalid date_check")
    try:
        transactions = customer.transactions
        net_revenue = 0
        for j in transactions:
            if j.created_at <= date_check:
                if j.type_transaction.value == 'payment':
                    net_revenue += j.amount
                elif j.type_transaction.value == 'refund':
                    net_revenue -= j.amount
        return net_revenue
    except Exception as e:
        raise ValueError("Invalid customer or date")


def calculate_average_hourly_price(customer, date_check):
    """Calculates the average hourly price and the total amount of unvoided orders
    this will be used to calculate the revenue
    """
    if not isinstance(date_check, datetime):
        raise ValueError("Invalid date_check")
    try:
        total_price = 0
        total_hours = 0
        total_orders = 0

        for i in customer.orders:
            # void date after that date_check and paid
            if i.booking_date <= date_check:
                if i.void_date is None:
                    total_orders += 1
                    total_price += i.total_price
                    total_hours += i.total_hours
                elif i.void_date > date_check:
                    total_orders += 1
                    total_price += i.total_price
                    total_hours += i.total_hours
        if total_hours == 0:
            total_hours = 1
        if total_price == 0:
            return {"average_hourly_price": total_price, "total_orders": total_orders}
        return {"average_hourly_price": round(total_price/total_hours, 2), "total_orders": total_orders}
    except Exception as e:
        raise ValueError('invalid date or customer')


def get_accrued_hours(customer, date_check):
    """Calculates the total amount of hours this user
    has used up(accrued) so far
    this will be used to calculate the revenue
    """
    if not isinstance(date_check, datetime):
        raise ValueError("Invalid date_check")
    try:
        students = customer.students
        status_dict_check = {'good cancellation',
                             'bad cancellation teacher',
                             'scheduled'}
        hours = 0
        for j in students:
            for i in j.lessons:
                if not i.trial_lesson:
                    if i.from_time <= date_check:
                        duration = i.duration_in_minutes/60
                        # if i.status.value == 'bad cancellation student':
                        #    if duration > 2:
                        #        hours += 2
                        #    else:
                        #        hours += duration
                        if i.status.value not in status_dict_check:
                            hours += duration
        return round(hours)
    except Exception as e:
        raise ValueError("Invalid customer or student")
