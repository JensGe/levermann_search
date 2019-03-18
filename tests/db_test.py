import dataset
from utils import constants as cst


def create_test_tables():
    with dataset.connect(cst.TEST_DATABASE) as db:
        db.query(
            """
        create table Aktien (
            ISIN varchar(127) null,
            WKN varchar(127) null,
            Name varchar(255) not null,
            Waehrung varchar(5) null,
            URI varchar(255) not null primary key,
            Handelsplatz varchar(15) null,
            Aktiv binary(1) default '1' null
            );
        
       
        create table Aktienauswahl (
            AktienURI varchar(255) null,
            constraint Aktienauswahl_Aktien_URI_fk
                foreign key (AktienURI) references Aktien (URI)
            );
        
        create table Aktienhistorien (
            AktienURI varchar(255) not null,
            Datum date not null,
            Eroeffnungswert decimal(8,2) null,
            Schlusswert decimal(8,2) null,
            primary key (AktienURI, Datum),
            constraint Aktienhistorien_Aktien_URI_fk
                foreign key (AktienURI) references Aktien (URI)
            );
        
        create table Aktienindizes (
            URI varchar(255) not null primary key,
            Ursprung varchar(127) not null,
            Name varchar(127) not null,
            Large_Cap_Index binary(1) not null,
            Aktiv binary(1) default '0' not null,
            Handelsstartzeit time null,
            Handelsschlusszeit time null
            );
        
        create table Aktientermine (
            AktienURI varchar(255) not null,
            Datum date not null,
            Terminart varchar(127) not null,
            Status varchar(15) null,
            primary key (AktienURI, Datum),
            constraint Aktientermine_Aktie_ISIN_fk
                foreign key (AktienURI) references Aktien (URI)
            );
        
        create table Indexhistorien (
            IndexURI varchar(255) not null,
            Datum date not null,
            Eroeffnungswert decimal(8,2) null,
            Schlusswert decimal(8,2) null,
            primary key (IndexURI, Datum),
            constraint Indexhistorien_Aktienindizes_URI_fk
                foreign key (IndexURI) references Aktienindizes (URI)
            );
        
        create table Indexinhalte (
            IndexURI varchar(255) not null,
            AktienURI varchar(255) not null,
            Abrufdatum date not null,
            primary key (IndexURI, AktienURI, Abrufdatum),
            constraint Indexinhalte_Aktienindizes_URI_fk
                foreign key (IndexURI) references Aktienindizes (URI)
            );
        
       
        create table Levermannscores (
            AktienURI varchar(255) not null,
            Kalenderwoche varchar(8) null,
            Datum date not null,
            Lev01_Wert decimal(6,2) null,
            Lev01_Score smallint(6) null,
            Lev02_Wert decimal(6,2) null,
            Lev02_Score smallint(6) null,
            Lev03_Wert decimal(6,2) null,
            Lev03_Score smallint(6) null,
            Lev04_Wert decimal(6,2) null,
            Lev04_Score smallint(6) null,
            Lev05_Wert decimal(6,2) null,
            Lev05_Score smallint(6) null,
            Lev06_Wert decimal(6,2) null,
            Lev06_Score smallint(6) null,
            Lev07_Wert decimal(6,2) null,
            Lev07_Score smallint(6) null,
            Lev08_Wert decimal(6,2) null,
            Lev08_Score smallint(6) null,
            Lev09_Wert decimal(6,2) null,
            Lev09_Score smallint(6) null,
            Lev10_Wert decimal(6,2) null,
            Lev10_Score smallint(6) null,
            Lev11_Score smallint(6) null,
            Lev12_Wert decimal(6,2) null,
            Lev12_Score smallint(6) null,
            Lev13_Wert decimal(6,2) null,
            Lev13_Score smallint(6) null,
            primary key (AktienURI, Datum),
            constraint Levermannscores_Aktie_ISIN_fk
                foreign key (AktienURI) references Aktien (URI)
            );
        
        create table Unternehmensdaten (
            AktienURI varchar(255) not null,
            Kalenderwoche varchar(8) null,
            Datum date not null,
            Marktkapitalisierung decimal(16,2) null,
            Indizes varchar(1024) null,
            Branchen varchar(1024) null,
            Ergebnis_nach_Steuern decimal(16,2) null,
            Operatives_Ergebnis decimal(16,2) null,
            Umsatzerloese decimal(16,2) null,
            Bilanzsumme decimal(16,2) null,
            Eigenkapital decimal(16,2) null,
            EPS_minus_3 decimal(5,2) null,
            EPS_minus_2 decimal(5,2) null,
            EPS_minus_1 decimal(5,2) null,
            EPS_0 decimal(5,2) null,
            EPS_plus_1 decimal(5,2) null,
            Analysten_Buy int null,
            Analysten_Hold int null,
            Analysten_Sell int null,
            primary key (AktienURI, Datum),
            constraint Unternehmensdaten_Aktie_ISIN_fk
                foreign key (AktienURI) references Aktien (URI)
            );
        """
        )
    return True


def insert_test_data():
    with dataset.connect(cst.TEST_DATABASE) as db:
        db.query(
            """
        insert into Aktien (ISIN, Name, URI, Handelsplatz, Aktiv) 
            values
            ('DE000A1EWWW0', 'adidas', 'adidas-Aktie', 'FSE', 1),
            ('US1912161007', 'Coca-Cola', 'coca-cola-Aktie', 'FSE', 1),
            ('GB00B1YW4409', '3i', '3i-Aktie', 'FSE', 1),
            ('US88579Y1010', '3M', '3m-Aktie', 'FSE', 1);
            
        insert into Aktien (Name, URI, Handelsplatz, Aktiv) 
            values
            ('AB InBev SA-NV (Anheuser-Busch InBev)', 'ab_inbev-Aktie', 'FSE', 1),
            ('Bechtle', 'bechtle-Aktie', 'FSE', 1),
            ('Cellcom Israel', 'cellcom_israel-Aktie', 'FSE', 1),
            ('Africa-Israel Investments', 'africa-israel_investments-Aktie', 'NASO', 1);
            
        insert into Aktien (Name, URI, Aktiv) 
            values
            ('Afyon Cimento Sanayii TAS', 'afyon_cimento_sanayii_tas-Aktie', 1);
            
        
        insert into Aktienindizes 
            values 
            ('CAC_40', 'Frankreich', 'CAC 40', 1, 1, '08:00:00', '20:00:00'),
            ('dax', 'Deutschland', 'DAX', 1, 1, '08:00:00', '20:00:00'),
            ('dow_jones', 'USA', 'Dow Jones', 1, 1, '15:30:00', '22:00:00'),
            ('tecdax', 'Deutschland', 'TecDAX', 0, 1, '08:00:00', '20:00:00'),
            ('s&p_500', 'USA', 'S&P 500', 0, 1, '08:00:00', '20:00:00'),
            ('FTSE_100', 'United Kingdom', 'FTSE 100', 1, 1, '09:00:00', '17:30:00');
         
        insert into Indexinhalte
            values 
            ('FTSE_100', '3i-Aktie', '2018-11-30'),
            ('dow_jones', '3m-Aktie', '2019-01-17'),
            ('s&p_500', '3m-Aktie', '2019-01-17');
        
        insert into Indexhistorien 
            values 
            ('CAC_40', '2019-03-07', '5267.92', '5282.14'),
            ('CAC_40', '2019-03-08', '5231.22', '5233.97'),
            ('dax', '2019-03-07', '11517.80', '11546.42'),
            ('dax', '2019-03-08', '11457.84', '11429.77'),
            ('dow_jones', '2019-03-07', '25473.23', '25645.45'),
            ('dow_jones', '2019-03-08', '25450.24', '25347.38');
        
        insert into Aktienhistorien 
            values
            ('adidas-Aktie', '2019-01-28', '203.10', '202.80'),
            ('adidas-Aktie', '2019-01-29', '203.20', '204.90'),
            ('adidas-Aktie', '2019-01-30', '204.10', '205.90'),
            ('adidas-Aktie', '2019-01-31', '206.90', '207.40'),
            ('adidas-Aktie', '2019-02-01', '202.30', '199.40');
            
        insert into Unternehmensdaten 
            (AktienURI, Datum, Marktkapitalisierung, 
             Indizes, Branchen, 
             Ergebnis_nach_Steuern, Operatives_Ergebnis, 
             Umsatzerloese, Bilanzsumme, Eigenkapital, 
             EPS_minus_3, EPS_minus_2, EPS_minus_1, EPS_0, EPS_plus_1, 
             Analysten_Buy, Analysten_Hold, Analysten_Sell)
            values 
            ('ab_inbev-Aktie', '2019-03-09', '121540.00',
             '["EURO STOXX 50", "STOXX 50", "BEL 20", "EURONEXT 100", "EURO STOXX", 
             "Next CAC 70", "BX Swiss -  EMEA"]', '["Getränke / Tabak"]', 
             '3702.48', '14520.88', 
             '46297.11', '204558.46', '62899.88', 
             '0.65', '3.60', '1.87', '4.11', '4.49', 
             '6', '2', '0'),
            ('ab_inbev-Aktie', '2019-03-16', '119980.00', 
            '["STOXX 50", "EURO STOXX 50", "BEL 20", "EURONEXT 100", "EURO STOXX", 
            "Next CAC 70", "BX Swiss -  EMEA"]', '["Getränke / Tabak"]', 
            '3702.48', '14520.88', 
            '46297.11', '204558.46', '62899.88', 
            '0.65', '3.60', '1.87', '4.11', '4.49', 
            '6', '2', '0'),
            ('bechtle-Aktie', '2019-03-16', '3230.00', 
            '["TecDAX", "MDAX", "Prime All Share", "LMDAX", "Technology All Share", 
            "HDAX", "LTecDAX", "CDAX", "MDAX Kursindex", "TecDAX Kursindex", 
            "BX Swiss -  EMEA", "DAXglobal Sarasin Sustainability Germany Index EUR", 
            "QIX Deutschland", "DAXglobal Sarasin Sustainability Germany", 
            "Schatten-Index-SDAX", "Schatten-Index-TecDAX"]', 
            '["IT-Dienstleister", "IT-Beratung Hardware", "Dienstleistungen", 
            "Internethandel (B2B, B2C)", "Informationstechnologie"]', 
            '114.56', '154.41', 
            '3570.12', '1462.63', '777.28', 
            '2.21', '2.46', '2.73', '3.84', '4.27',
            '4', '4', '1'),
            ('3i-Aktie', '2019-03-16', '10970.00', 
            '["FTSE 100", "FTSE Allshare"]', 
            '["Finanzdienstleister"]', 
            '1463.00', '1445.00', 
            '398.00', '7899.00', '7024.00', 
            '0.86', '1.64', '1.52', '0.01', '0.01',
            '0', '0', '0'),
            ('cellcom_israel-Aktie', '2019-03-16', '440.21', 
            '["TA-100"]', 
            '["Telekommunikation", "Mobilkommunikation", "Netzbetreiber (Carrier)", 
            "IT-Dienstleister"]', 
            '112.00', '286.00', 
            '3871.00', '6087.00', '1441.00', 
            '0.94', '1.47', '1.11', '0.62', '0.91',
            '0', '0', '0');
                      
        """
        )

    return True


def delete_test_data():
    with dataset.connect(cst.TEST_DATABASE) as db:
        db.query(
            """
        delete from Indexhistorien;
        delete from Aktienhistorien;
        delete from Unternehmensdaten;
        delete from Indexinhalte;
        delete from Aktientermine;
        delete from Aktien;
        delete from Aktienindizes;
        """
        )
    return True


def drop_test_tables():
    with dataset.connect(cst.TEST_DATABASE) as db:
        db.query(
            """
        drop table if exists Aktienauswahl;
        drop table if exists Aktienhistorien;
        drop table if exists Indexhistorien;
        drop table if exists Aktientermine;
        drop table if exists Indexinhalte;
        drop table if exists Levermannscores;
        drop table if exists Unternehmensdaten;
        
        drop table if exists Aktien;
        drop table if exists Aktienindizes;
        """
        )
    return True
