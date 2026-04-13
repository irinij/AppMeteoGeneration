# App Meteo Corso

## Panoramica del progetto
Questa è una semplice applicazione meteo sviluppata in Python che permette agli utenti di ottenere informazioni sul tempo attuale per una città specifica. L'app è composta da due componenti principali:
- Uno script a riga di comando (`weather_script.py`) per ottenere la temperatura attuale via terminale.
- Un'applicazione web basata su FastAPI che fornisce un'interfaccia utente grafica per visualizzare i dati meteo, inclusi temperatura, velocità del vento e codice meteo.

L'applicazione utilizza API esterne gratuite per recuperare i dati geografici e meteorologici in tempo reale.

## Sicurezza
Non sono state integrate API che richiedono chiavi API. Se aggiungi API con chiavi, dovrai gestire le chiavi tramite il file .env come configurato, in modo da gestirle in modo sicuro utilizzando variabili d'ambiente. Le chiavi saranno memorizzate in un file `.env` (non incluso nel repository Git per motivi di sicurezza) e caricate automaticamente tramite `python-dotenv`. Questo garantirà che le chiavi non siano mai esposte in chiaro nel codice sorgente.

## API utilizzate
L'applicazione utilizza le seguenti API esterne gratuite:

### Open-Meteo API
- **Scopo**: Recupera dati meteorologici attuali (temperatura, vento, umidità, precipitazioni)
- **URL**: https://open-meteo.com/
- **Nessuna chiave API richiesta**

### Nominatim (OpenStreetMap)
- **Scopo**: Converte nomi di città in coordinate geografiche
- **URL**: https://nominatim.openstreetmap.org/
- **Nessuna chiave API richiesta**

## Istruzioni di installazione
1. **Clona o scarica il progetto**: Assicurati di avere il codice sorgente nella tua directory locale.
2. Da Powershell: git clone https://github.com/irinij/AppMeteoGeneration.git
3. cd AppMeteoGeneration

4. **Crea un ambiente virtuale** (opzionale ma raccomandato): da riga di comando, digita:
   ```
   python -m venv .venv
   # Su Windows:
   .venv\Scripts\activate
   # Su macOS/Linux:
   source .venv/bin/activate
   ```

5. **Installa le dipendenze**:
   ```
   pip install -r requirements.txt
   ```

6. **Verifica l'installazione**:
   ```
   python -c "import fastapi, requests; print('Dipendenze installate correttamente')"
   ```

## Guida all'utilizzo

### Script a riga di comando
Per utilizzare lo script CLI:
```
python weather_script.py
```
Quando richiesto, inserisci il nome della città (ad esempio: "Roma", "Milano", "New York").

### Applicazione web
1. **Attiva l'ambiente virtuale** (se non già attivo):
   ```
   # Su Windows:
   .venv\Scripts\activate
   # Su macOS/Linux:
   source .venv/bin/activate
   ```

2. **Verifica che uvicorn sia installato**:
   ```
   uvicorn --version
   ```
   Se ricevi un errore, assicurati di aver installato le dipendenze con `pip install -r requirements.txt`.

3. **Avvia il server**:
   ```
   uvicorn app.main:app --reload
   ```
   - L'opzione `--reload` riavvia automaticamente il server quando modifichi il codice (utile durante lo sviluppo).
   - Se ricevi un messaggio di errore, verifica:
     - Che l'ambiente virtuale sia attivato.
     - Che tutte le dipendenze siano installate.
     - Che sei nella directory principale del progetto (dove si trova `app/main.py`).

4. **Apri il browser**:
   Vai all'indirizzo `http://127.0.0.1:8000` (o `http://localhost:8000`).

5. **Utilizzo**:
   - Nella pagina principale vedrai un form semplice con un campo di testo per inserire il nome della città.
   - Inserisci il nome di una città (ad esempio: "Roma", "Milano", "New York") e premi "Invia" o invio.
   - L'app elaborerà la richiesta e mostrerà una nuova pagina con i dati meteo attuali, inclusi:
     - Temperatura in °C
     - Velocità del vento in km/h
     - Umidità relativa in %
     - Precipitazioni in mm
     - Codice meteo (con legenda integrata nella pagina)
   - Se inserisci una città non valida o si verifica un errore, vedrai un messaggio di errore sulla pagina.

6. **Ferma il server**:
   Premi `Ctrl+C` nel terminale dove è in esecuzione uvicorn per fermare il server.

**Nota**: Il server web rimane attivo finché non lo fermi manualmente. Puoi lasciarlo in esecuzione mentre sviluppi o testi l'app.

### Esecuzione dei test
Per eseguire i test automatizzati:
```
python -m pytest tests/ -v
```

## Output di esempio

### Output dello script CLI
```
Inserisci il nome della città: Roma
Meteo attuale a Roma:
Temperatura: 18.5°C
Velocità del vento: 12.3 km/h
Umidità: 65%
Precipitazioni: 0.0 mm
Codice meteo: 1 (vedi legenda WMO per descrizione)
```

### Interfaccia web
Dopo aver inserito "Roma" nell'applicazione web, vedrai qualcosa di simile:

```
Meteo per Roma

Temperatura: 18.5°C
Velocità del vento: 12.3 km/h
Umidità: 65%
Precipitazioni: 0.0 mm
Codice meteo: 1
```

## Funzionalità
- **Ricerca per città**: Inserisci il nome di qualsiasi città per ottenere i dati meteo.
- **Dati in tempo reale**: Recupera informazioni meteorologiche attuali utilizzando API esterne.
- **Interfaccia web**: Interfaccia utente intuitiva basata su HTML/CSS con sfondo dinamico che cambia in base alle condizioni meteo.
- **Script CLI**: Versione a riga di comando per uso rapido.
- **Gestione errori**: Gestisce input non validi e errori di rete in modo elegante.
- **Test automatizzati**: Suite di test per garantire la funzionalità.

## Sfondo Dinamico
L'applicazione web include uno sfondo dinamico che cambia automaticamente in base al codice meteo:
- **Immagini random**: Utilizza il servizio Unsplash per caricare immagini casuali relative alle condizioni meteo attuali.
- **Mappatura intelligente**: Ogni codice WMO è associato a parole chiave specifiche (es. "clear sky blue" per cielo sereno, "heavy rain weather" per pioggia intensa).
- **Fallback**: Se il caricamento dell'immagine fallisce, viene applicato un gradiente di default.
- **Design responsive**: Gli elementi della pagina hanno sfondi semi-trasparenti per garantire la leggibilità su qualsiasi immagine di sfondo.

## Gestione degli errori
L'applicazione gestisce diversi tipi di errori:
- **Città non trovata**: Se la città inserita non esiste o non può essere geocodificata, viene mostrato un messaggio di errore.
- **Errori di rete**: Timeout o problemi di connessione alle API vengono catturati e segnalati all'utente.
- **Input non valido**: Nomi di città vuoti o non stringhe vengono rifiutati.
- **Dati mancanti**: Se l'API non fornisce i dati richiesti, viene mostrato un messaggio appropriato.
- **Errori imprevisti**: Eccezioni generiche vengono catturate e loggate.

## Informazioni API
L'applicazione utilizza le seguenti API esterne gratuite:
- **Nominatim (OpenStreetMap)**: Per la geocodifica, converte i nomi delle città in coordinate geografiche (latitudine e longitudine).
  - URL: `https://nominatim.openstreetmap.org/search`
  - Utilizzo: Richiede un header `User-Agent` per identificare l'applicazione.
- **Open-Meteo**: API gratuita per dati meteorologici.
  - URL: `https://api.open-meteo.com/v1/forecast`
  - Parametri utilizzati: `latitude`, `longitude`, `current=temperature,windspeed,weathercode,relative_humidity_2m,precipitation`
  - Fornisce: Temperatura, velocità del vento, codice meteo (WMO weather codes), umidità relativa, precipitazioni.

**Nota**: Queste API sono gratuite ma hanno limiti di utilizzo. Per uso in produzione, considera l'implementazione di caching o l'uso di API a pagamento.

## Miglioramenti futuri
- **Previsioni a lungo termine**: Aggiungere previsioni meteo per i prossimi giorni.
- **Mappa interattiva**: Integrazione con una mappa per selezionare la posizione visivamente.
- **Notifiche**: Sistema di notifiche per condizioni meteorologiche estreme.
- **Cache dei dati**: Implementare caching per ridurre le chiamate API e migliorare le prestazioni.
- **Supporto multilingua**: Traduzioni per l'interfaccia utente.
- **API REST completa**: Esporre endpoint API per integrazioni esterne.
- **Database**: Salvataggio delle ricerche recenti o preferenze utente.
- **UI/UX migliorata**: Design più moderno con framework come Bootstrap o React.
