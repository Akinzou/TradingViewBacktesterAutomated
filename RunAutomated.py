import os
import csv
stop_loss = int(input("Enter the minimum Stop Loss value: "))
take_profit = int(input("Enter the minimum Take Profit value: "))
max_sl = int(input("Enter the maximum Stop Loss value: "))
max_tp = int(input("Enter the maximum Take Profit value: "))
step = int(input("Enter the Step value: "))
time_frame = input("Enter the TimeFrame value (in minutes only for non-standard charts like Renko, else write 0): ")
name_input = input("Enter the name: ")
invert = input("Do you want to switch buy to sell and sell to buy (invert)? (yes/no): ")
spread_pips = input("How many decimal places does your symbol have? ")

headers = ["TP", "SL", "Winrate (%)", "TPrate (%)", "PNL"]

name = f"output/{name_input}.csv"

with open(name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

os.system(f'python merge_automated.py --sl -1 --tp -1 --time_frame {time_frame} --filename {name} --inv {invert} --decimal_places {spread_pips}')

if max_sl-stop_loss >= max_tp-take_profit:
    for i in range(stop_loss, max_sl + step, step):
        for x in range (take_profit, max_tp + step, step):
            os.system(f'python merge_automated.py --sl {i} --tp {x} --time_frame {time_frame} --filename {name} --inv {invert} --decimal_places {spread_pips}' )


else:
    for i in range(take_profit, max_tp + step, step):
        for x in range(stop_loss, max_sl + step, step):
            os.system(f'python merge_automated.py --sl {x} --tp {i} --time_frame {time_frame} --filename {name}  --inv {invert} --decimal_places {spread_pips}')