import datetime


class MyCalender:
        
    def __init__(self):
        super().__init__()
        self.date_eastern = ''
        self.easter_day = ''
        self.holidays = [
            '01.01',
            '06.01',
            '01.05',
            '03.10',
            '31.10',
            '24.12',
            '25.12',
            '26.12',
            '30.12',            
        ]
        
        # method calls to fill self.holidays
        self.calculate_eastern()
        self.fill_holidays()
     
    def calculate_eastern(self):
        """
        calculation of easter date via gausian formular
        
        Oster-Formel nach Carl Friedrich Gauß
        a = Jahr mod 4
        b = Jahr mod 7
        c = Jahr mod 19
        d = (19c + M) mod 30
        e = (2a + 4b + 6d + N) mod 7
        
        Formel für Berechnung des Ostertags:
        f = (c+11d+22e)/451
        
        Ostersonntag = 22+d+e-7f. 
        Wenn dieses Ergebnis größer als 31, so liegt Ostern im April. 
        Dann muss folgende Formel benutzt werden: 
        Ostersonntag = 22+d+e -7f-31 = d+e-7f-9
        
        source: https://www1.wdr.de/wissen/mensch/osterformel-gauss-100.html
        """
        
        this_year = datetime.datetime.now().year        
        M = 24
        N = 5
        
        a = this_year % 4
        b = this_year % 7
        c = this_year % 19
        d = (19 * c + M) % 30
        e = (2 * a + 4 * b + 6 * d + N) % 7        
        f = (c + 11 * d + 22 * e) // 451        
        easter = 22 + d + e - 7 * f
        
        easter_day = easter if easter <= 31 else easter - 31
        easter_month = '03' if easter <= 31 else '04'
        
        self.easter_day = f'{easter_day:02}.{easter_month}'
        self.date_eastern = datetime.datetime.strptime(f'{self.easter_day}.{this_year}', '%d.%m.%Y')
        return None
        
    def fill_holidays(self):
        eastern_related_holiday_days = [
            self.date_eastern,
            self.date_eastern - datetime.timedelta(days=2),
            self.date_eastern - datetime.timedelta(days=1),
            self.date_eastern + datetime.timedelta(days=1),
            self.date_eastern + datetime.timedelta(days=39),
            self.date_eastern + datetime.timedelta(days=49),
            self.date_eastern + datetime.timedelta(days=50),
        ]
        
        for holiday in eastern_related_holiday_days:
            self.holidays.append(
                f'{holiday:%d.%m}'
            )
        return None
