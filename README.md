# Grok Usage Monitor for Linux / Zorin OS

En letvægts system tray-app der viser dit Grok-forbrug direkte i top-panelet på Zorin OS / Ubuntu.

## Features
- Farvede procenter i menu baren (Grok Build / API / Chat)
- Weekly SuperGrok Limit + progress bar + breakdown
- Daglig brugsgraf i detaljeret visning
- "Refresh Now" knap
- Auto-refresh hvert 5. minut
- Demo-data indbygget (nemt at udskifte med rigtig data senere)

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

1. Åbn "Startup Applications" (Søg efter det i menuen)
2. Tilføj ny entry:
   - **Navn**: Grok Usage Monitor
   - **Kommando**: `python3 /fuld/sti/til/main.py`  (ret stien!)
   - **Kommentar**: Viser Grok forbrug i top-panelet

Eller brug .desktop-filen (se nedenfor).

## Filer i repoet
- `main.py` - Hovedprogrammet (rettet for syntax-fejl)
- `grok-usage-monitor.desktop` - Til autostart

## Vigtigt: Kodegennemgang
Denne version er gennemgået og rettet:
- `def init(self)` → `def __init__(self)`
- `if name == "main"` → `if __name__ == "__main__"`
- Fjernet stray tekst midt i koden
- Mindre forbedringer til labels og struktur

## Fremtidige forbedringer (TODO)
- Tilføj rigtig datahentning (erstat `get_usage_data()`)
- Bedre/brugerdefineret ikon i menu baren
- Indstillinger-vindue til manuel indtastning af værdier
- Pakkefil / .deb eller Flatpak

Denne app er lavet med Grok (og kode tjekket for fejl).

## Licens
MIT License - brug den som du vil!
