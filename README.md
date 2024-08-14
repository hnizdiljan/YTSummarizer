# YouTube Video Summarizer

YouTube Video Summarizer je Python aplikace, která automaticky stahuje titulky z YouTube videí, extrahuje z nich text a používá OpenAI API k vytvoření shrnutí obsahu videa.

## Funkce

- Stahování automatických titulků z YouTube videí
- Extrakce textu z titulků
- Generování shrnutí pomocí OpenAI API
- Podpora zpracování více videí najednou
- Ukládání shrnutí do textového souboru

## Požadavky

- Python 3.6 nebo novější
- pip (správce balíčků pro Python)

## Instalace

1. Naklonujte tento repozitář:
   ```
   git clone [https://github.com/your-username/youtube-video-summarizer.git](https://github.com/hnizdiljan/YTSummarizer.git)
   cd youtube-video-summarizer
   ```

2. Vytvořte virtuální prostředí (doporučeno):
   ```
   python -m venv venv
   source venv/bin/activate  # Na Windows použijte `venv\Scripts\activate`
   ```

3. Nainstalujte potřebné závislosti:
   ```
   pip install -r requirements.txt
   ```

## Použití

Aplikaci spustíte pomocí následujícího příkazu:

```
python youtube_summarizer.py --URL "URL1,URL2,URL3" --APIKEY "your-openai-api-key"
```

Kde:
- `URL1,URL2,URL3` jsou URL adresy YouTube videí oddělené čárkami (bez mezer)
- `your-openai-api-key` je váš OpenAI API klíč

Například:
```
python youtube_summarizer.py --URL "https://www.youtube.com/watch?v=dQw4w9WgXcQ,https://www.youtube.com/watch?v=9bZkp7q19f0" --APIKEY "sk-abcdefghijklmnopqrstuvwxyz123456"
```

## Výstup

Aplikace vytvoří soubor `video_summaries.txt` v aktuálním adresáři. Tento soubor bude obsahovat URL adresy zpracovaných videí a jejich shrnutí.

## Poznámky

- Ujistěte se, že máte platný OpenAI API klíč.
- Aplikace potřebuje připojení k internetu pro stahování titulků a komunikaci s OpenAI API.
- Respektujte autorská práva a podmínky použití YouTube a OpenAI při používání této aplikace.

## Přispívání

Příspěvky jsou vítány! Pokud chcete přispět, prosím:

1. Forkněte repozitář
2. Vytvořte novou větev (`git checkout -b feature/AmazingFeature`)
3. Commitněte své změny (`git commit -m 'Add some AmazingFeature'`)
4. Pushněte do větve (`git push origin feature/AmazingFeature`)
5. Otevřete Pull Request

## Licence

Distribuováno pod licencí MIT. Viz `LICENSE` soubor pro více informací.

## Kontakt

Jan Hnízdil - https://www.linkedin.com/in/jan-hn%C3%ADzdil-93689299/ - hnizdiljan@gmail.com
