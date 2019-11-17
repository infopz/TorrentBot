# TorrentBot

Telegram Bot per automatizzare il dowload di Serie TV.

Prendendo le nuove release dal feed RSS di IlCorsaroNero, mette in download su Transmission solo quelle che l'utente guarda o e' intenzionato a guardare prendendo l'elenco dal profilo TVTime.
Attraverso il comando /torrent e' possibile visualizzare lo stato attuale dei download su Transmission e con il comando /add e' possibile aggiungere nuovi torrent

Utilizza [pzgram](https://github.com/infopz/pzgram) 

E' richiesto un database SQLite e un file config.py con i dati per il bot, di TVTime e di Transmission
