import pandas as pd
from os.path import abspath
import os.path
from os import path

def buy_stock(c_percent, b_filename, p_filename):
    
    b_df = pd.read_excel(b_filename, index_col=None)
    p_df = pd.read_excel(p_filename, index_col=None)
    # print(list(b_df.columns.values))
    # print(list(p_df.columns.values))

    date = input("Input transaction date (DD/MM/YYYY): ") or '-1'
    price = int(input("Input stock unit price: ") or '-1') * (1+c_percent/100)
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
    b_df = b_df.append(new_row, ignore_index=True)
    b_df.to_excel(b_filename, index=False, ) 

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
    p_df = p_df.append(new_row, ignore_index=True)
    p_df.to_excel(p_filename, index=False)


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
            print("buying at index " + str(index) + ", holding >= remiaining")
            b_df.at[index, 'Holding'] = b_df.iloc[index]['Holding'] - remaining_quantity
            p_rprofit = p_rprofit + remaining_quantity * (price - b_df.at[index, 'Price'])
            b_df.at[0,'Holding'] = b_df.iloc[0]['Holding'] - remaining_quantity
            break
        if b_df.iloc[index]['Holding'] < remaining_quantity:
            print("buying at index " + str(index) + ", holding < remiaining")
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
    p_df = p_df.append(new_row, ignore_index=True)
    p_df.to_excel(p_filename, index=False)

def create_new_stock(stock_name):
    print("Created new folder for " + stock_name)


# Function to insert row in the dataframe 
def Insert_row(row_number, df, row_value): 
    # Starting value of upper half 
    start_upper = 0
   
    # End value of upper half 
    end_upper = row_number 
   
    # Start value of lower half 
    start_lower = row_number 
   
    # End value of lower half 
    end_lower = df.shape[0] 
   
    # Create a list of upper_half index 
    upper_half = [*range(start_upper, end_upper, 1)] 
   
    # Create a list of lower_half index 
    lower_half = [*range(start_lower, end_lower, 1)] 
   
    # Increment the value of lower half by 1 
    lower_half = [x.__add__(1) for x in lower_half] 
   
    # Combine the two lists 
    index_ = upper_half + lower_half 
   
    # Update the index of the dataframe 
    df.index = index_ 
   
    # Insert a row at the end 
    df.loc[row_number] = row_value 
    
    # Sort the index labels 
    df = df.sort_index() 
   
    # return the dataframe 
    return df 
   
# Let's create a row which we want to insert 
row_number = 2
row_value = ['11/2/2011', 'Wrestling', 12000] 
  
if row_number > df.index.max()+1: 
    print("Invalid row_number") 
else: 
      
    # Let's call the function and insert the row 
    # at the second position 
    df = Insert_row(row_number, df, row_value) 
   
    # Print the updated dataframe 
    print(df) 

stock_name = input("Input stock name:  ") or 'test'

with pd.ExcelWriter(stock_name+'.xlsx') as writer:  
    df1.to_excel(writer, sheet_name='buy_history')
    df2.to_excel(writer, sheet_name='sell_history')
    df2.to_excel(writer, sheet_name='profit_summary')

if not path.exists(stock_name):
    exit("no stock named " + stock_name + " exists!")

b_filename = abspath('./'+stock_name+'/buy_history_test.xlsx')
s_filename = abspath('./'+stock_name+'/sell_history_test.xlsx')
p_filename = abspath('./'+stock_name+'/profit_summary_test.xlsx')

# b_filename = abspath('./'+stock_name+'/buy_history.xlsx')
# s_filename = abspath('./'+stock_name+'/sell_history.xlsx')
# p_filename = abspath('./'+stock_name+'/profit_summary.xlsx')

commision_percentage = 5

action = input("Input transaction type: buy or sell? ") or 'buy'
if action == 'buy':
    buy_stock(commision_percentage, b_filename, p_filename)
if action == 'sell':
    sell_stock(b_filename, s_filename, p_filename)