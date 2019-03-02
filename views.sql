CREATE VIEW Aktien_Scraping_Queue AS
SELECT DISTINCT inh.AktienURI, inh.IndexURI, ind.Handelsschlusszeit, ind.Aktiv
FROM Indexinhalte inh
JOIN Aktienindizes ind
ON ind.URI = inh.IndexURI
HAVING ind.Aktiv = 1
ORDER BY Handelsschlusszeit, AktienURI;