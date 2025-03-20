import requests
from bs4 import BeautifulSoup
import csv

# URL of the chapter
url = "https://www.bible.com/bible/3936/JUD.1.GNT"

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Fetch the page content
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the first `div` containing the Ibani text
    readers = soup.find_all("div", class_="ChapterContent_reader__Dt27r")

    if not readers:
        print("❌ Could not find the Ibani section!")
    else:
        ibani_section = readers[0]  # First div (Ibani)

        # Find all verses in the Ibani section
        ibani_verses = ibani_section.find_all("span", class_="ChapterContent_verse__57FIw")

        verse_data = []

        # Extract Ibani verses
        for verse in ibani_verses:
            verse_number = "Unknown"
            ibani_text = "Missing Text"

            verse_label = verse.find("span", class_="ChapterContent_label__R2PLt")
            if verse_label:
                verse_number = verse_label.text.strip()

            ibani_text_span = verse.find("span", class_="ChapterContent_content__RrUqA")
            if ibani_text_span:
                ibani_text = ibani_text_span.text.strip()

            verse_data.append([verse_number, ibani_text])

        # Save to a CSV file
        filename = "ibani_bible_verses.csv"
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter="\t")
            writer.writerow(["Verse", "Ibani Text"])  # Header
            writer.writerows(verse_data)

        print(f"✅ Ibani verses saved to {filename} successfully!")

else:
    print("❌ Failed to retrieve the page.")
