from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape_booking_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    hotels_data = []

    while True:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        hotels = soup.findAll('div', {'data-testid': 'property-card'})

        for hotel in hotels:
            name_element = hotel.find('div', {'data-testid': 'title'})
            name = name_element.text.strip()

            location_element = hotel.find('span', {'data-testid': 'address'})
            location = location_element.text.strip()
     
            price_element = hotel.find('span', {'class': 'f6431b446c fbfd7c1165 e84eb96b1f'})
            price = price_element.text.strip() if price_element else "N/A"

            rating_element = hotel.find('div', {'class': 'a3b8729ab1 d86cee9b25'})
            rating = rating_element.text.strip() if rating_element else "N/A"

            review_element = hotel.find('div', {'class': 'abf093bdfe f45d8e4c32 d935416c47'})
            review = review_element.text.strip() if review_element else "N/A"

            comment_element = hotel.find('div', {'class': 'a3b8729ab1 e6208ee469 cb2cbb3ccb'})
            comment = comment_element.text.strip() if comment_element else "N/A"

            image_element = hotel.find('img', {'data-testid': 'image'})
            image = image_element.get('src') if image_element else "N/A"



            hotels_data.append({
                'name': name,
                'location': location,
                'price': price,
                'rating': rating,
                'review': review,
                'comment': comment,
                'image': image
            })
        return hotels_data

all_hotels_data = []
for offset in range(0, 925, 25):  # Adjust the range as needed
    url = f'https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1DCAEoggI46AdICVgDaFCIAQGYAQm4ARfIAQzYAQPoAQH4AQKIAgGoAgO4ArDuuaEGwAIB0gIkZmJhYjE4YzAtNDdhMy00MmY1LTk2NWItN2UzOTgyNTk1OWEx2AIE4AIB&aid=397594&ss=London&ssne=London&ssne_untouched=London&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-2601889&dest_type=city&checkin=2024-02-14&checkout=2024-02-16&ltfd=6%3A1%3A%3A%3A1&group_adults=2&no_rooms=1&group_children=0&selected_currency=USD&offset={offset}'
    page_data = scrape_booking_data(url)
    print(offset)
    all_hotels_data.extend(page_data)


# Create a DataFrame and save to CSV
hotels_df = pd.DataFrame(all_hotels_data)
hotels_df.to_csv('/home/pooja/Data-Engineer-1/notebook/BookingCom.csv', header=True, index=False)
print("Scarped data")
