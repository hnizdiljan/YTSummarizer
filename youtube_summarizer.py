import os
import re
import glob
from typing import List
import yt_dlp
import requests
from dotenv import load_dotenv
import argparse

# Načtení proměnných prostředí
load_dotenv()

def get_video_id(url: str) -> str:
    """Získá ID videa z URL."""
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['id']

def find_subtitle_file(video_id: str) -> str:
    """Najde existující soubor s titulky pro dané video ID."""
    pattern = f"{video_id}.*.vtt"
    matching_files = glob.glob(pattern)
    return matching_files[0] if matching_files else None

def download_subtitles(url: str) -> str:
    """Stáhne automatické titulky z YouTube videa, pokud ještě neexistují."""
    video_id = get_video_id(url)
    existing_subtitle_file = find_subtitle_file(video_id)
    
    if existing_subtitle_file:
        print(f"Soubor s titulky {existing_subtitle_file} již existuje. Používám existující soubor.")
        return existing_subtitle_file
    
    ydl_opts = {
        'writeautomaticsub': True,
        'subtitlesformat': 'vtt',
        'skip_download': True,
        'outtmpl': '%(id)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Hledáme nově stažený soubor
    new_subtitle_file = find_subtitle_file(video_id)
    if new_subtitle_file:
        return new_subtitle_file
    else:
        raise FileNotFoundError(f"Nepodařilo se najít nebo stáhnout titulky pro video {url}")

def extract_text_from_vtt(vtt_file: str) -> str:
    """Extrahuje čistý text z VTT souboru."""
    try:
        with open(vtt_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Soubor {vtt_file} nebyl nalezen. Zkontrolujte, zda video má titulky.")
        return ""
    
    # Odstranění časových značek a metadat
    lines = content.split('\n')
    text_lines = [line for line in lines if not re.match(r'\d{2}:\d{2}:\d{2}', line) and line.strip()]
    
    return ' '.join(text_lines)

def summarize_text(text: str, api_key: str) -> str:
    """Pošle text do OpenAI API pro sumarizaci."""
    if not text:
        return "Nepodařilo se získat text pro sumarizaci."
    
    if not api_key:
        return "OpenAI API klíč není nastaven. Prosím, zadejte jej pomocí parametru --APIKEY."
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Jsi asistent, který vytváří stručné shrnutí a vypisuje nejzajímavější informace z poskytnutého textu."},
            {"role": "user", "content": f"Shrň následující text a vypiš nejzajímavější informace: {text}"}
        ]
    }
    
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()  # Vyvolá výjimku pro HTTP chyby
        response_data = response.json()
        
        if 'choices' in response_data and len(response_data['choices']) > 0:
            return response_data['choices'][0]['message']['content']
        else:
            print("Neočekávaná odpověď od API:")
            print(response_data)
            return "Nepodařilo se získat shrnutí z API."
    
    except requests.exceptions.RequestException as e:
        print(f"Chyba při komunikaci s API: {e}")
        return "Došlo k chybě při komunikaci s API."

def process_video(url: str, api_key: str) -> str:
    """Zpracuje jedno video - stáhne titulky, extrahuje text a vytvoří shrnutí."""
    subtitle_file = download_subtitles(url)
    text = extract_text_from_vtt(subtitle_file)
    summary = summarize_text(text, api_key)
    
    return summary

def save_summary(url: str, summary: str, output_file: str):
    """Uloží shrnutí do výstupního souboru."""
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f"URL: {url}\n")
        f.write("Shrnutí:\n")
        f.write(summary)
        f.write("\n\n" + "="*50 + "\n\n")

def main(urls: List[str], api_key: str):
    """Hlavní funkce pro zpracování seznamu URL."""
    output_file = "video_summaries.txt"
    for url in urls:
        print(f"Zpracovávám video: {url}")
        summary = process_video(url, api_key)
        print("Shrnutí:")
        print(summary)
        save_summary(url, summary, output_file)
        print(f"Shrnutí bylo uloženo do souboru: {output_file}")
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Video Summarizer")
    parser.add_argument("--URL", required=True, help="URL adresy videí oddělené čárkou")
    parser.add_argument("--APIKEY", required=True, help="OpenAI API klíč")
    
    args = parser.parse_args()
    
    video_urls = [url.strip() for url in args.URL.split(",")]
    api_key = args.APIKEY
    
    main(video_urls, api_key)
