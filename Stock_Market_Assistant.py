#Fedor Fedorets

import requests
#api = "demo"
api = "QQIP56OR1PKRHMGO"
#api = "UT8T0V8KPTBS9Q6V"
#api = "XKWE0ESZZHO5OD6V"

#Code für die erste Aufgabe
def task1():
    #Am Anfang nach Ticker fragen
    tic = input("\nPlease specify ticker: ")

    #Die Daten für diesen Ticker aus Json Datei kriegen
    url1 = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={tic}&apikey={api}"
    data1 = requests.get(url1).json()

    #Nach dem gewünschten Jahr fragen
    year = input("\nPlease specify year: ")
    
    #Fehlermeldung für alles außer Jahre 2000-2023 und erneute Frage
    while year not in str(list(range(2000, 2024))) or int(year) not in range(2000, 2024):
        year = input("Year not found! Try another year: ")

    #Am Ende Dieser Funktion bekommt man eine Zeile mit dem Monat, Schlusskurs am Ende des Monats und die Rendite im Vergleich zum Vormonat
    def monthly_return(month):

        #Dummy-Variable für While-Loop für die Findung des letzten Tages des Monats
        problem = True
        #Die Suche beginnt ab 26. jedes Monats. Man könnte auch ab 0 suchen, aber wir versuchen sinnlose Durchläufe zu minimieren.
        day = 26
        #While-Loop für die Findung des letzten Tages des Monats, an dem die Börse geöffnet war, und des entsprechenden Schlusskurses.
        while problem == True:
            #Wenn innerhalb von try ein Fehler aufgetaucht ist (z.B. keine Daten im Json gefunden), dann wird except ausgeführt.
            #Bis try ohne Fehler ausgeführt wird, bleiben wir im Loop.
            try:
                problem = False
                #If Befehl für die Korrekte Suche im json. Die Monate fangen da mit einem "0" an, z.B. 09 für September
                if month <= 9:
                    a1 = data1["Monthly Adjusted Time Series"][f"{year}-0{month}-{str(day)}"]["5. adjusted close"]
                else:
                    a1 = data1["Monthly Adjusted Time Series"][f"{year}-{month}-{str(day)}"]["5. adjusted close"]
            except:
                #Wenn in try ein Fehler auftaucht, wird except ausgeführt und die Nummer des Tages um 1 erhöht. Dann beginnt Loop wieder.
                problem = True
                day += 1 
        
        #Folgende While-Loop funktioniert analog zur vorherigen. Man bekommt aber am Ende die Daten für Vorperiode. 
        problem = True
        day = 26
        while problem == True:
            try:
                problem = False
                #Hier ist wichtig, dass die Vorperiode für Januar, der Dezember des vorherigen Jahres ist.
                if month == 1:
                    a0 = data1["Monthly Adjusted Time Series"][f"{int(year)-1}-12-{str(day)}"]["5. adjusted close"]
                elif 2 <= month <= 10:
                    a0 = data1["Monthly Adjusted Time Series"][f"{year}-0{month-1}-{str(day)}"]["5. adjusted close"]
                else:
                    a0 = data1["Monthly Adjusted Time Series"][f"{year}-{month-1}-{str(day)}"]["5. adjusted close"]
            except:
                problem = True
                day += 1  
        
        #Hier wird aus den zwei aufeinanderfolgenden Kusen die Rendite berechnet und auf zwei Nachkommastellen gerundet.
        roi = ((float(a1)-float(a0))/float(a0))*100
        roi_round = round(roi, 2)

        #Hier bekommt man die Zeile mit Datum, Schlusskurs und Rendite FÜR EIN MONAT.
        if month <= 9:
            print(f"{year}-0{month}    {a1}    {roi_round}%")
        else:
            print(f"{year}-{month}    {a1}    {roi_round}%")

    #Diese Loop baut eine Tabelle indem sie den Titel ausgibt und dann die vorherige Funktion für alle Monate 1-12 durchläuft.
    month = 1
    print("\n  Date      Price      Return")
    while month <= 12:
        monthly_return(month)
        month += 1
    print("\n")

#Code für die zweite Aufgabe
def task2():

    #Ticker abfragen
    tic = input("\nPlease specify ticker: ")
    #Datum abfragen im speziellen Format
    date = input("\nPlease specify date YYYY-MM-DD: ")
    #Die json Datei für diesen Ticker bekommen
    url2 = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={tic}&outputsize=full&apikey={api}"
    data2 = requests.get(url2).json()

    #Ticker aus Json bekommen
    tic0 = data2["Meta Data"]["2. Symbol"] 

    #Fehlermeldung für das falsche Datum
    problem = True
    while problem == True:
        try:
            problem = False
            cl = data2["Time Series (Daily)"][f"{date}"]["4. close"]
        except:
            problem = True
            date = input("\nDate not found! Try another date: ")
    
    #Ausgabe von Ticker-Name und Schlusskurs an dem Tag.
    print(f"\nYour ticker: {tic0}")
    print(f"Close on {date}: {cl}\n")

#Code für die Einführung und Begrüßung
def intro():
    #Ausgabe von Erklärungen und Beschreibung von Funktionen
    print("\n\nHello! I am your Smart Stock Market Assistant.\nI can only execute two types of tasks at the moment:(( But don't worry, new features will be added soon!")
    print("\nLet's get to work!")
    print("I can calculate the monthly return for a particular stock in a particular year. To do this, select task 1.")
    print("I can also find the price of any stock on any day. To do this, select task 2.")
    print("\nHere is some important info before you start:")
    print("Ticker - name of the stock, e.g. IBM, TSLA, AAPL, MSFT, UAL")
    print("Return is calculated as percentage change in price compared to the previous period")
    print("Return function works for year 2023 and earlier")
    print("Try switching APIs at the top of the code if something doesn't work (demo api only works with IBM ticker)")

    #Fragen nach der Aufgabennummer
    task = input("\nWhat do you want me to do?\n\n1. Monthly Return\n2. Historical Prices\n3. Exit\n\nEnter task number: ")
    
    #Die Dummy-Variable für While-Loop definieren
    home = False

    #While-Loop. Wenn man hier reingeht, hat man immer eine definierte Aufgabennummer (task) und Dummy-Variable True oder False.
    #Davon ist abhängig ob man weitere Aufgabe wählt oder aus dem Loop rausgeht.
    while home == False:
        if task == "1":
            #Die erste Aufgabe ausführen und dann nach der neuen Aufgabennummer fragen, mit der man wieder in Loop reingeht.
            task1()
            print("Great!")
            task = input("\nWhat do you want me to do?\n\n1. Monthly Return\n2. Historical Prices\n3. Exit\n\nEnter task number: ")
            #Dank dieser Variable bleibt man immer weiter im Loop
            home = False
        
        elif task == "2":
            task2()
            print("Great!")
            task = input("\nWhat do you want me to do?\n\n1. Monthly Return\n2. Historical Prices\n3. Exit\n\nEnter task number: ")
            home = False

        elif task == "3":
            #Wenn man dritte Option wählt (exit). Dann bricht man aus dem Loop (home=True) und exit() wird ausgeführt.
            home = True
            exit()

        else:
            #Hier wird man nach der Aufgabennummer noch mal gefragt und bleibt weiter im Loop.
            print("\nIncorrect task!\n")
            home = False
            task = input("\nEnter task number: ")

#Programm abschließen
def exit():
    print("\nBye bye!\n")

#Anfang  
intro()
