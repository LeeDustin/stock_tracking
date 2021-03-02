import pandas as pd
from os.path import abspath
import os.path
from os import path

commision_percentage = 1
stock_name = input("Input stock name:  ") or 'test'
b_filename = abspath('./'+stock_name+'/buy_history.xlsx')
s_filename = abspath('./'+stock_name+'/sell_history.xlsx')
p_filename = abspath('./'+stock_name+'/profit_summary.xlsx')
# filename = stock_name+".xlsx"

# # Iterating over one column - `f` is some function that processes your data
# result = [f(x) for x in df['col']]
# # Iterating over two columns, use `zip`
# result = [f(x, y) for x, y in zip(df['col1'], df['col2'])]
# # Iterating over multiple columns - same data type
# result = [f(row[0], ..., row[n]) for row in df[['col1', ...,'coln']].to_numpy()]
# # Iterating over multiple columns - differing data type
# result = [f(row[0], ..., row[n]) for row in zip(df['col1'], ..., df['coln'])]

# Function to insert row in the dataframe 
def insert_row(row_num, orig_df, row_to_add):
    row_num= min(max(0, row_num), len(orig_df))
    df_part_1 = orig_df.loc[0:row_num]   
    df_part_2 = orig_df.loc[row_num+1:]
    df_final = df_part_1.append(row_to_add, ignore_index = True)
    df_final = df_final.append(df_part_2, ignore_index = True)
    return df_final

def buy_stock(b_filename, p_filename):
    # print(filename)
    b_df = pd.read_excel(b_filename, index_col=None)
    p_df = pd.read_excel(p_filename, index_col=None)
    # print(list(b_df.columns.values))
    # print(list(p_df.columns.values))

    date = input("Input transaction date (DD/MM/YYYY): ") or '-1'
    price = int(input("Input stock unit price: ") or '-1') * (1+commision_percentage/100)
    quantity = int(input("Input bought stock quantity: ") or '-1')
    cost = price * quantity

    # update buy_history total cost, quantity, and stock
    b_t_quantity = b_df.iloc[0]['Quantity']
    b_t_cost = b_df.iloc[0]['Cost']
    b_t_holding = b_df.iloc[0]['Holding']
    b_t_quantity = b_t_quantity + quantity
    b_t_cost = b_t_cost + cost
    b_t_holding = b_t_holding + quantity
    b_df.at[0,'Quantity'] = b_t_quantity
    b_df.at[0, 'Cost'] = b_t_cost
    b_df.at[0,'Holding'] = b_t_holding


    # append new transaction and write to buy_history.xlsx
    new_row = {'Date':date, 'Price':price, 'Quantity':quantity, 'Cost':cost, 'Holding':quantity}
    # b_df = insert_row(0, b_df, new_row)
    b_df = b_df.append(new_row, ignore_index=True)
    b_df.to_excel(b_filename, index=False) 

    # update profit_summary 
    p_holding = p_df.iloc[-1]['Total Holding']
    p_balance = p_df.iloc[-1]['Total Balance']
    p_rprofit = p_df.iloc[-1]['Realised Profit']
    
    p_uprofit = 0
    for index, row in b_df.iterrows():
        if (index == 0):
            continue
        p_uprofit = p_uprofit+(price-row['Price'])*row['Holding']
    # print("unrealized profit:", p_uprofit)

    # append new transaction and write to profit_summary.xlsx
    new_row = {'Date':date, 'Price':price, 'Total Holding':p_holding+quantity, \
        'Total Balance':p_balance-cost, 'Realised Profit':p_rprofit, 'Unrealised Profit':p_uprofit}
    # p_df = insert_row(-1, p_df, new_row)
    p_df.at[0, "Date"]= "Current"
    p_df.at[0, "Price"]= price
    p_df.at[0, "Total Holding"]= p_holding+quantity
    p_df.at[0, "Total Balance"]= p_balance-cost
    p_df.at[0, "Realised Profit"]= p_rprofit
    p_df.at[0, "Unrealised Profit"]= p_uprofit

    p_df = p_df.append(new_row, ignore_index=True)
    p_df.to_excel(p_filename, index=False)


    # print("b_df:")
    # print(b_df)
    # print("p_df:")
    # print(p_df)


def sell_stock(b_filename, s_filename, p_filename):
    b_df = pd.read_excel(b_filename, index_col=None)
    s_df = pd.read_excel(s_filename, index_col=None)
    p_df = pd.read_excel(p_filename, index_col=None)
    # print(list(p_df.columns.values))


    date = input("Input transaction date (DD/MM/YYYY): ") or '-1'
    price = int(input("Input stock unit price: ") or '-1')
    quantity = int(input("Input sold stock quantity: ") or '-1')
    profit = price * quantity

    # update buy_history total and individual stock, then write it back
    b_t_holding = b_df.iloc[0]['Holding']
    if quantity > b_t_holding:
        exit("Error: sold quantity > holding quantity")

    remaining_quantity = quantity
    p_rprofit = p_df.iloc[-1]['Realised Profit']

    for index, row in b_df.iterrows():
        if index == 0 or b_df.iloc[index]['Holding'] == 0:
            continue
        if b_df.iloc[index]['Holding'] >= remaining_quantity:
            # print("buying at index " + str(index) + ", holding >= remiaining")
            b_df.at[index, 'Holding'] = b_df.iloc[index]['Holding'] - remaining_quantity
            p_rprofit = p_rprofit + remaining_quantity * (price - b_df.at[index, 'Price'])
            b_df.at[0,'Holding'] = b_df.iloc[0]['Holding'] - remaining_quantity
            break
        if b_df.iloc[index]['Holding'] < remaining_quantity:
            # print("buying at index " + str(index) + ", holding < remiaining")
            p_rprofit = p_rprofit + b_df.at[index, 'Holding'] * (price - b_df.at[index, 'Price'])
            remaining_quantity = remaining_quantity - b_df.iloc[index]['Holding']
            b_df.at[index, 'Holding'] = 0
            b_df.at[0,'Holding'] = b_df.iloc[0]['Holding'] - b_df.iloc[index]['Holding']
            continue
    b_df.to_excel(b_filename, index=False) 

    # update sell_history total quantity and profit
    s_t_quantity = s_df.iloc[0]['Quantity']
    s_t_profit = s_df.iloc[0]['Profit']
    s_t_quantity = s_t_quantity + quantity
    s_t_profit = s_t_profit + profit
    s_df.at[0,'Quantity'] = s_t_quantity
    s_df.at[0, 'Profit'] = s_t_profit

    # append new transaction and write to sell_history.xlsx
    new_row = {'Date':date, 'Price':price, 'Quantity':quantity, 'Profit':profit}
    s_df = s_df.append(new_row, ignore_index=True)
    s_df.to_excel(s_filename, index=False) 

    # update profit_summary 
    p_holding = p_df.iloc[-1]['Total Holding']
    p_balance = p_df.iloc[-1]['Total Balance']

    p_uprofit = 0
    for index, row in b_df.iterrows():
        if (index == 0):
            continue
        p_uprofit = p_uprofit+(price-row['Price'])*row['Holding']

    # append new transaction and write to profit_summary.xlsx
    new_row = {'Date':date, 'Price':price, 'Total Holding':p_holding-quantity, \
        'Total Balance':p_balance+profit, 'Realised Profit':p_rprofit, 'Unrealised Profit':p_uprofit}
    p_df.at[0, "Date"]= "Current"
    p_df.at[0, "Price"]= price
    p_df.at[0, "Total Holding"]= p_holding-quantity
    p_df.at[0, "Total Balance"]= p_balance+profit
    p_df.at[0, "Realised Profit"]= p_rprofit
    p_df.at[0, "Unrealised Profit"]= p_uprofit
    p_df = p_df.append(new_row, ignore_index=True)
    p_df.to_excel(p_filename, index=False)

    # print("b_df:")
    # print(b_df)
    # print("s_df:")
    # print(s_df)
    # print("p_df:")
    # print(p_df)

def create_new_stock(stock_name):
    os.mkdir(stock_name)

    b_df= pd.DataFrame([["Total", 0, 0, 0, 0]], columns=['Date', 'Price', 'Quantity','Cost','Holding'])
    s_df= pd.DataFrame([["Total", 0, 0, 0]], columns=['Date', 'Price', 'Quantity','Profit'])
    p_df= pd.DataFrame([["Current", 0, 0, 0, 0, 0]], columns=['Date', 'Price', 'Total Holding','Total Balance','Realised Profit','Unrealised Profit'])

    b_df.to_excel(b_filename, index=False)
    s_df.to_excel(s_filename, index=False)
    p_df.to_excel(p_filename, index=False)

    print("Created new folder for " + stock_name)


if not path.exists(stock_name):
    action = input("no stock named " + stock_name + " exists, create new folder? (Y/N)  ") or "Y"
    if action == "N":
        exit("Exiting program...")
    elif action == "Y":
        create_new_stock(stock_name)
    else :
        exit("Invalid response: not Y or N")



action = input("Input transaction type: buy or sell? ") or 'buy'
# with pd.ExcelWriter(filename) as writer:
if action == 'buy':
    buy_stock(b_filename, p_filename)
if action == 'sell':
    sell_stock(b_filename, s_filename, p_filename)