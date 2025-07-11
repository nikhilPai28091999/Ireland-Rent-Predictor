import requests
from bs4 import BeautifulSoup
import csv
import os
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Fixed amenity list to track
AMENITY_FEATURES = [
    "Parking", "Central Heating", "Washing Machine", "Dryer", 
    "Dishwasher", "Internet", "Garden / Patio / Balcony", "Microwave",
    "Gym", "Pets Allowed"
]

def scrape_daft(pages=3, output_file="/Users/nikhilpai2809/Desktop/Development/Rent-Predictor-App/Rent-Predictor/model/data/rentals-data-withAmenities.csv"):
    file_exists = os.path.isfile(output_file)
    sno = 1

    for page_num in range(1, pages + 1):
        print(f"\n📄 Scraping page {page_num}...")

        url = f"https://www.daft.ie/property-for-rent/ireland?page={page_num}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        cards = soup.find_all('li', class_='sc-b44c3a7b-3 kYcIow')

        listings = []

        for i, card in enumerate(cards):
            try:
                title_tag = card.find('p', class_='sc-4c172e97-0 gMInbX')
                title = title_tag.get_text(strip=True) if title_tag else "N/A"

                price_tag = card.find('p', class_='sc-4c172e97-0 jmFLnF')
                price = price_tag.get_text(strip=True) if price_tag and price_tag.get_text(strip=True) else None

                if not price:
                    price_tag = card.find('p', class_='sc-4c172e97-0 csEcJw')
                    price = price_tag.get_text(strip=True) if price_tag and price_tag.get_text(strip=True) else "N/A"

                span_tags = card.find_all('span')
                bed_bath = [s.get_text(strip=True) for s in span_tags if "Bed" in s.text or "Bath" in s.text]
                bed = next((item for item in bed_bath if "Bed" in item), "N/A")
                bath = next((item for item in bed_bath if "Bath" in item), "N/A")

                link_tag = card.find('a', href=True)
                listing_url = "https://www.daft.ie" + link_tag['href'] if link_tag else None

                # ⬇️ Amenity flags
                amenity_flags = {amenity: 0 for amenity in AMENITY_FEATURES}

                if listing_url:
                    try:
                        detail_res = requests.get(listing_url, headers=headers)
                        detail_soup = BeautifulSoup(detail_res.text, "html.parser")

                        # ✅ Get price if still missing
                        if price == "N/A":
                            price_container = detail_soup.find('p', class_='sc-76247ba6-2 hNFtOY')
                            if price_container:
                                price_span = price_container.find('span')
                                if price_span:
                                    price = price_span.get_text(strip=True)

                        # ✅ Extract amenities
                        amenity_tags = detail_soup.find_all('li', class_='sc-a1a4223a-1 kqvXqH')
                        found_amenities = [tag.get_text(strip=True) for tag in amenity_tags]

                        for feature in AMENITY_FEATURES:
                            if feature in found_amenities:
                                amenity_flags[feature] = 1

                        time.sleep(0.5)

                    except Exception as e:
                        print(f"⚠️ Error fetching detail page: {listing_url} — {e}")

                row_data = {
                    "Sno": sno,
                    "Title": title,
                    "Bed": bed,
                    "Bath": bath,
                    "Price": price,
                    **amenity_flags  # Unpack amenities into row
                }

                listings.append(row_data)

                print(f"{sno}. {title} | Bed: {bed} | Bath: {bath} | Price: {price} | Amenities: {amenity_flags}")
                sno += 1

            except Exception as e:
                print(f"❌ Error reading card {i+1} on page {page_num}: {e}")

        # Write to CSV
        fieldnames = ["Sno", "Title", "Bed", "Bath", "Price"] + AMENITY_FEATURES
        with open(output_file, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
                file_exists = True
            writer.writerows(listings)

    print(f"\n✅ Done scraping {pages} pages. Data saved to '{output_file}'")

# 🔧 Run
scrape_daft(pages=250)
