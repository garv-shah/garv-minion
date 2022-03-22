import csv
from datetime import datetime
from time import sleep, time

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.offsetbox import AnchoredText
from tradingview_ta import TA_Handler, Interval

symbol_list = []
symbol_to_name = {}

# Loads the data from a csv file if it exists
try:
    with open("./data/input_companies.csv", 'r') as csv_file:
        # Creates a dictionary from the csv file
        reader = csv.DictReader(csv_file)
        csv_dict = list(reader)
        # Sets the values of the layout fields to the values in the csv file
        for company in csv_dict:
            symbol_list.append(company['Code'])
            symbol_to_name[company['Code']] = company['Company name']
        csv_file.close()
except FileNotFoundError:
    pass

print(symbol_list)
print(symbol_to_name)

output_list = []
output_dict = {}

    for symbol in symbol_list:
        print(symbol)
        output = TA_Handler(
            symbol=symbol,
            screener="australia",
            exchange="ASX",
            interval=Interval.INTERVAL_1_DAY
        )

        summary = output.get_analysis().summary

        output_list.append([symbol, summary])
        if summary['RECOMMENDATION'] == 'STRONG_BUY':
            output_dict[symbol] = summary

    print(output_dict)

    with open("./data/ASX_Stock_Game_Data.csv", 'w+', newline='') as csvfile:
        fieldnames = list(output_dict.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(output_dict)
        csvfile.close()

keys = list(output_dict.keys())
vals = [float(output_dict[key]['BUY']) for key in keys]
plt.style.use('seaborn-dark')
plt.figure(figsize=(23, 5))
ax = sns.barplot(x=keys, y=vals)

for x in range(len(list(output_dict.keys()))):
    ax.text(x-0.1, 0.85, symbol_to_name[list(output_dict.keys())[x]][0:55], fontsize=6.5, rotation=90)

now = datetime.now()
time_string = now.strftime("%d/%m/%Y %H:%M:%S")
plt.text(0.005, 0.02, f"Generated at {time_string} - Garv Shah", fontsize=14, transform=plt.gcf().transFigure)
plt.xlabel('\nSymbol')
plt.ylabel('Buy Intensity')
plt.title('Daily NOVA Stock Advice')
plt.grid()
plt.savefig('./NOVA_Stock_Advice.png')


if __name__ == "__main__":
    main()
