# Grok Usage Monitor for Linux / Zorin OS

En letvægts system tray-app der viser dit Grok-forbrug direkte i top-panelet på Zorin OS / Ubuntu.

## Features
- Farvede procenter og progress bar i menu baren (Grok Build / API / Chat)
- **Settings...** vindue: Manuel redigering af alle værdier (gemmes automatisk)
- Daglig brugsgraf i detaljeret visning
- "Refresh Now" + auto-refresh hvert 5. minut
- Dynamisk ikon der skifter efter forbrugsniveau (advarsel ved højt forbrug)
- About dialog
- Demo-data + fuld JSON-persistens (`~/.config/grok-usage-monitor/config.json`)

## Installation på Zorin OS

```bash
sudo apt update
sudo apt install python3-gi gir1.2-ayatanaappindicator3-0.1
```

## Kør appen

```bash
python3 main.py
```

## Start automatisk ved login (anbefalet)

1. Åbn "Startup Applications"
2. Tilføj ny entry med kommandoen til `main.py`

Eller brug `grok-usage-monitor.desktop` filen (ret stien og kopier til `~/.config/autostart/`).

## Sådan bruger du Settings
1. Højreklik på ikonet i top-panelet
2. Vælg **Settings...**
3. Rediger Overall %, Grok Build, API, Chat og Reset date
4. Tryk **Save** – værdierne opdateres live og gemmes til config-filen

Næste gang du starter appen, husker den dine indstillinger.

## Filer i repoet
- `main.py` – Hovedprogram (v1.1)
- `grok-usage-monitor.desktop` – Autostart
- `README.md`

## Vigtigt: Kodegennemgang
Denne version er gennemgået og forbedret:
- Oprindelige syntax-fejl rettet (`__init__`, `__name__`)
- Ny Settings-dialog + JSON-persistens
- Dynamisk ikon-håndtering
- Bedre struktur, fejlhåndtering og kommentarer

## Fremtidige forbedringer (TODO)
- Rigtig datahentning (når Grok tilbyder officiel usage API)
- Mulighed for at vælge custom ikon (PNG)
- Bedre grafer med Gtk.DrawingArea eller matplotlib
- Pakkefil (.deb / Flatpak)

Denne app er lavet med Grok (kode tjekket og udvidet).

## Licens
MIT License
