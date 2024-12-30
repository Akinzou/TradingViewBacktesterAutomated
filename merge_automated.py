import sys
import pandas as pd
from datetime import datetime, timedelta
import argparse
import csv
parser = argparse.ArgumentParser()

#---------------INPUTS--------------
parser.add_argument('--sl', type=float, required=True)
parser.add_argument('--tp', type=float, required=True)
parser.add_argument('--time_frame', type=float, required=True)
parser.add_argument('--filename', type=str, required=True)
parser.add_argument('--inv', type=str, required=True)
parser.add_argument('--decimal_places', type=int, required=True)
args = parser.parse_args()
sl = args.sl
file_name = args.filename
tp = args.tp
inv = args.inv
decimal_places = args.decimal_places
spread_pips = 10 ** -decimal_places
#-----------------------------------

pips = 1/spread_pips

if inv == "yes":
    invert = True
else:
    invert = False

PNL = 0
entry_price = 0
floatinPLN = 0
loss = 0
wins = 0
num_of_sl = 0
num_of_tp = 0
losslist = []
winslist = []
startingDate = 0

# Wczytywanie danych
positions_df = pd.read_csv('positions.csv')
prices_df = pd.read_csv('prices.csv')

# Praca na positions_df
positions_types = positions_df['Type'].tolist()
positions_dates = positions_df['Date/Time'].tolist()  # Dodanie listy dla daty/czasu

# Usuwanie dwóch pierwszych elementów z list
positions_types = positions_types[2:]
positions_dates = positions_dates[2:]



# Odwracanie list
positions_types.reverse()
positions_dates.reverse()


# Dodanie pół godziny do każdej daty w positions_dates
print(positions_dates)
positions_dates = [(datetime.strptime(date, '%Y-%m-%d %H:%M') + timedelta(minutes=args.time_frame)).strftime('%Y-%m-%d %H:%M') for date in positions_dates]
print(positions_dates)

# Praca na prices_df
prices_df = prices_df.iloc[:, 0].str.split('\t', expand=True)
prices_columns = ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'TICKVOL', 'VOL', 'SPREAD']
prices_df.columns = prices_columns

# Konwersja DATE i TIME do datetime
prices_df['DATE'] = pd.to_datetime(prices_df['DATE'], format='%Y.%m.%d')
prices_df['TIME'] = pd.to_datetime(prices_df['TIME'], format='%H:%M:%S').dt.time

# Połączenie DATE i TIME w jedną kolumnę DATETIME
prices_df['DATETIME'] = pd.to_datetime(prices_df['DATE'].astype(str) + ' ' + prices_df['TIME'].astype(str))

# Formatowanie DATETIME do formatu bez sekund
prices_df['DATETIME'] = prices_df['DATETIME'].dt.strftime('%Y-%m-%d %H:%M')

# Tworzenie listy prices_dates z połączonej kolumny DATETIME bez sekund
prices_dates = prices_df['DATETIME'].tolist()

# Usunięcie zbędnych kolumn
prices_df.drop(columns=['DATE', 'TIME'], inplace=True)

prices_close = prices_df['CLOSE'].tolist()
prices_high = prices_df['HIGH'].tolist()
prices_low = prices_df['LOW'].tolist()



if invert:
    print(positions_types)
    for i in range(len(positions_types)):
        original_value = positions_types[i]

        if original_value == 'Entry Long':
            positions_types[i] = 'Entry Short'
        elif original_value == 'Exit Long':
            positions_types[i] = 'Exit Short'
        elif original_value == 'Entry Short':
            positions_types[i] = 'Entry Long'
        elif original_value == 'Exit Short':
            positions_types[i] = 'Exit Long'
    print(positions_types)

def findmedian(prices):
    if len(prices) != 0:
        print(pips)
        print(prices)
        prices_sorted = sorted(prices)
        n = len(prices_sorted)
        srodek = n // 2

        # Jeśli liczba elementów jest parzysta
        if n % 2 == 0:
            return str(round((prices_sorted[srodek - 1] + prices_sorted[srodek]) / 2, 2))  + " pips"
        # Jeśli liczba elementów jest nieparzysta
        else:
            return str(round(prices_sorted[srodek], 2)) + " pips"
    else:
        return "Only tp/sl"


positions_date = datetime.strptime(positions_dates[0], '%Y-%m-%d %H:%M')
prices_date = datetime.strptime(prices_dates[0], '%Y-%m-%d %H:%M')

for i in range(len(positions_types)-1):
    found_entry = False
    positions_date = datetime.strptime(positions_dates[i], '%Y-%m-%d %H:%M')
    positions_date_close = datetime.strptime(positions_dates[i+1], '%Y-%m-%d %H:%M')
    prices_date = datetime.strptime(prices_dates[i], '%Y-%m-%d %H:%M')
    #search entry price
    for x in range(startingDate, len(prices_dates)):
        if found_entry:
            startingDate = 0 if x - 2 < 0 else x - 2
            break
        if positions_types[i] == 'Entry Short' or positions_types[i] == 'Entry Long':
            prices_date = datetime.strptime(prices_dates[x], '%Y-%m-%d %H:%M')
            if prices_date == positions_date:
                if positions_types[i] == 'Entry Short':
                    entry_price = float(prices_low[x])
                    print("Entry short: ", positions_date, "Price:", entry_price)
                elif positions_types[i] == 'Entry Long':
                    entry_price = float(prices_high[x])
                    print("Entry long: ", positions_date, "Price:", entry_price)
                found_entry = True

        #search exit price
        if found_entry:
            if positions_types[i] == 'Entry Short':
                print("Looking for exit price for short...")
                for y in range(x, len(prices_dates)):
                    close_price_date = datetime.strptime(prices_dates[y], '%Y-%m-%d %H:%M')
                    if positions_date <= close_price_date < positions_date_close:
                        floatinPLN = (entry_price - float(prices_high[y])) * pips
                        if floatinPLN <= sl:
                            print("SL before closing: ", close_price_date, "floating: ", floatinPLN, prices_high[y])
                            PNL += floatinPLN
                            loss += 1
                            num_of_sl += 1
                            break

                        floatinPLN = (entry_price - float(prices_low[y])) * pips
                        if floatinPLN >= tp:
                            print("TP: ", close_price_date, "floating: ", floatinPLN)
                            print("TP before closing: ", close_price_date, "floating: ", floatinPLN, prices_low[y])
                            PNL += floatinPLN
                            wins += 1
                            num_of_tp += 1
                            break

                    elif close_price_date >= positions_date_close:
                        floatinPLN = (entry_price - float(prices_high[y])) * pips
                        if floatinPLN <= sl:
                            print("SL when closing: ", close_price_date, "floating: ", floatinPLN, prices_high[y])
                            PNL += floatinPLN
                            loss += 1
                            num_of_sl += 1
                            break

                        floatinPLN = (entry_price - float(prices_low[y])) * pips
                        if floatinPLN >= tp:
                            print("TP before closing: ", close_price_date, "floating: ", floatinPLN, prices_low[y])
                            PNL += floatinPLN
                            wins += 1
                            num_of_tp += 1
                            break

                        print(entry_price, float(prices_high[y]))
                        print(entry_price - float(prices_high[y]))
                        floatinPLN = (entry_price - float(prices_high[y])) * pips
                        if floatinPLN < 0:
                            print("Closing: ", close_price_date, "floating: ", floatinPLN, prices_high[y])
                            PNL += floatinPLN
                            losslist.append(floatinPLN)
                            loss += 1
                            break

                        if floatinPLN >= 0:
                            print("Closing: ", close_price_date, "floating: ", floatinPLN, prices_high[y])
                            PNL += floatinPLN
                            wins += 1
                            break

            if positions_types[i] == 'Entry Long':
                print("Looking for exit price for long...")
                for y in range(x, len(prices_dates)):
                    close_price_date = datetime.strptime(prices_dates[y], '%Y-%m-%d %H:%M')
                    if positions_date <= close_price_date < positions_date_close:
                        floatinPLN = (float(prices_low[y]) - entry_price) * pips
                        if floatinPLN <= sl:
                            print("SL before closing: ", close_price_date, "floating: ", floatinPLN, prices_low[y])
                            PNL += floatinPLN
                            loss += 1
                            num_of_sl += 1
                            break

                        floatinPLN = (float(prices_high[y]) - entry_price) * pips
                        if floatinPLN >= tp:
                            print("TP before closing: ", close_price_date, "floating: ", floatinPLN, prices_high[y])
                            PNL += floatinPLN
                            wins += 1
                            num_of_tp += 1
                            break

                    elif close_price_date >= positions_date_close:
                        floatinPLN = (float(prices_low[y]) - entry_price) * pips
                        if floatinPLN <= sl:
                            print("SL when closing: ", close_price_date, "floating: ", floatinPLN, prices_low[y])
                            PNL += floatinPLN
                            loss += 1
                            num_of_sl += 1
                            break

                        floatinPLN = (float(prices_high[y]) - entry_price) * pips
                        if floatinPLN >= tp:
                            print("SL when closing: ", close_price_date, "floating: ", floatinPLN, prices_high[y])
                            PNL += floatinPLN
                            wins += 1
                            num_of_tp += 1
                            break

                        floatinPLN = (float(prices_close[y]) - entry_price) * pips
                        if floatinPLN < 0:
                            print("Closing: ", close_price_date, "floating: ", floatinPLN, prices_low[y])
                            PNL += floatinPLN
                            losslist.append(floatinPLN)
                            loss += 1
                            break

                        if floatinPLN >= 0:
                            print("Closing: ", close_price_date, "floating: ", floatinPLN, prices_low[y])
                            PNL += floatinPLN
                            winslist.append(floatinPLN)
                            wins += 1
                            break

print(f'\n\nOverall:\n'
      f'PNL: {round(PNL, 2)} pips\n'
      f'Num of SL: {num_of_sl}\n'
      f'Num of TP: {num_of_tp}\n'
      f'Winrate: {round((wins / (wins + loss)) * 100, 2)}%\n'
      f'TPrate: {"NA" if (num_of_tp + num_of_sl) == 0 else f"{round((num_of_tp / (num_of_tp + num_of_sl)) * 100, 2)}%"}\n'
      f'Wins: {wins}, Loss: {loss}\n'
      f'Median loss: {findmedian(losslist)}\n'
      f'Median win: {findmedian(winslist)}'
      )


with open(file_name, 'a', newline='') as file:  # Tryb 'a' (append)
    writer = csv.writer(file)
    winrate = round((wins / (wins + loss)) * 100, 2)
    TPrate = "NA" if (num_of_tp + num_of_sl) == 0 else f"{round((num_of_tp / (num_of_tp + num_of_sl)) * 100, 2)}%"

    # Zapis danych na końcu pliku
    writer.writerow([
        tp, sl,
        winrate,
        TPrate,
        round(PNL, 2)
    ])