import pandas as pd
import queue
from os.path import abspath

def buy(c_percent, b_filename, p_filename):
    b_df = pd.read_excel(b_filename, index_col=None)
    p_df = pd.read_excel(p_filename, index_col=None)
    print(b_df)
    # print(list(b_df.columns.values))
    # print(list(p_df.columns.values))


    date = input("Input transaction date (DD/MM/YYYY): ") or '-1'
    price = int(input("Input stock unit price: ") or '-1') * c_percent
    quantity = int(input("Input bought stock quantity: ") or '-1')
    cost = price * quantity



    # update buy_history total cost, quantity, and stock
    t_quantity = b_df.iloc[0]['Quantity']
    t_cost = b_df.iloc[0]['Cost']
    t_stock = b_df.iloc[0]['Stock']
    t_quantity = t_quantity + quantity
    t_cost = t_cost + cost
    t_stock = t_stock + quantity
    b_df.at[0,'Quantity'] = t_quantity
    b_df.at[0, 'Cost'] = t_cost
    b_df.at[0,'Stock'] = t_stock


    # append new transaction and write to buy_history.xlsx
    new_row = {'Date':date, 'Price':price, 'Quantity':quantity, 'Cost':cost, 'Stock':quantity}
    b_df = b_df.append(new_row, ignore_index=True)
    print(b_df)
    b_df.to_excel(abspath('./abc/buy_history_test.xlsx'), index=False) 

    # update profit_summary 
    c_stock = p_df.iloc[-1]['Stock']
    c_balance = p_df.iloc[-1]['Balance']
    c_rprofit = p_df.iloc[-1]['Realised Profit']
    
    c_uprofit = 0
    for index, row in b_df.iterrows():
        if (index == 0):
            continue
        c_uprofit = c_uprofit+(price-row['Price'])*row['Stock']
    print("unrealized profit:", c_uprofit)

    # append new transaction and write to profit_summary.xlsx
    new_row = {'Date':date, 'Price':price, 'Stock':c_stock+quantity, \
        'Balance':c_balance-cost, 'Realised Profit':c_rprofit, 'Unrealised Profit':c_uprofit}
    p_df = p_df.append(new_row, ignore_index=True)
    print(p_df)
    p_df.to_excel(abspath('./abc/profit_summary_test.xlsx'), index=False)


def sell(s_filename, p_filename):
    b_df = pd.read_excel(b_filename, index_col=None)
    s_df = pd.read_excel(s_filename, index_col=None)
    p_df = pd.read_excel(s_filename, index_col=None)
    print(b_df)
    print(s_df)

    date = input("Input transaction date (DD/MM/YYYY): ") or '-1'
    price = int(input("Input stock unit price: ") or '-1')
    quantity = int(input("Input sold stock quantity: ") or '-1')
    profit = price * quantity



commision_percentage = 1
b_filename = abspath('./abc/buy_history_test.xlsx')
s_filename = abspath('./abc/sell_history_test.xlsx')
p_filename = abspath('./abc/profit_summary_test.xlsx')

# b_filename = abspath('./abc/buy_history.xlsx')
# s_filename = abspath('./abc/sell_history.xlsx')
# p_filename = abspath('./abc/profit_summary.xlsx')


action = input("Input transaction type: buy or sell? ") or 'buy'
if action == 'buy':
    buy(commision_percentage, b_filename, p_filename)
if action == 'sell':
    sell(s_filename, p_filename)