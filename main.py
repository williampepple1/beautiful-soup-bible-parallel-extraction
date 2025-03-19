import requests
from bs4 import BeautifulSoup
import csv

# URL of the chapter
url = "https://www.bible.com/bible/68/JHN.1.GNT?parallel=3936"

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Fetch the page content
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find both `div`s containing English and Ibani
    readers = soup.find_all("div", class_="ChapterContent_reader__Dt27r")

    if len(readers) < 2:
        print("❌ Could not find both English and Ibani sections!")
    else:
        english_section = readers[0]  # First div (English)
        ibani_section = readers[1]  # Second div (Ibani)

        # Find all verses in both sections
        english_verses = english_section.find_all("span", class_="ChapterContent_verse__57FIw")
        ibani_verses = ibani_section.find_all("span", class_="ChapterContent_verse__57FIw")

        verse_data = []

        # Step 1: Extract and store English verses first
        english_results = []
        for verse in english_verses:
            verse_number = "Unknown"
            english_text = "Missing English Text"

            verse_label = verse.find("span", class_="ChapterContent_label__R2PLt")
            if verse_label:
                verse_number = verse_label.text.strip()

            english_text_span = verse.find("span", class_="ChapterContent_content__RrUqA")
            if english_text_span:
                english_text = english_text_span.text.strip()

            english_results.append([verse_number, english_text])

        # Step 2: Extract and store Ibani verses separately
        ibani_results = []
        for verse in ibani_verses:
            verse_number = "Unknown"
            ibani_text = "Missing Ibani Text"

            verse_label = verse.find("span", class_="ChapterContent_label__R2PLt")
            if verse_label:
                verse_number = verse_label.text.strip()

            ibani_text_span = verse.find("span", class_="ChapterContent_content__RrUqA")
            if ibani_text_span:
                ibani_text = ibani_text_span.text.strip()

            ibani_results.append([verse_number, ibani_text])

        # Step 3: Combine English and Ibani correctly
        max_length = max(len(english_results), len(ibani_results))
        for i in range(max_length):
            english_verse_number, english_text = english_results[i] if i < len(english_results) else ["Missing", "Missing"]
            ibani_verse_number, ibani_text = ibani_results[i] if i < len(ibani_results) else ["Missing", "Missing"]

            verse_data.append([english_verse_number, english_text, ibani_text, ibani_verse_number])

        # Save to a CSV file
        filename = "bible_verses.csv"
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["English Verse", "English Text", "Ibani Text", "Ibani Verse"])  # Header
            writer.writerows(verse_data)

        print(f"✅ Verses saved to {filename} successfully!")

else:
    print("❌ Failed to retrieve the page.")
