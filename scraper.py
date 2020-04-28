from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import pandas as pd

var = input("Please enter the number of pages you wish to scrape: ")
print("Scraping " + str(var) + " pages.")

driver = webdriver.Chrome(executable_path='chromedriver') # Chrome driver is located in the working directory

# website urls
urls = []
p_to_s = int(var) # Number of pages we wish to scrape

for i in range(1,p_to_s+1):
    urls.append("https://www.ultimate-guitar.com/explore?page=" + str(i) + "&")

page_link = []
song_name = []
for url in urls:
    driver.get(url) # Get the page

    link_element = driver.find_elements_by_css_selector('._1mes3') # Select the Song list element

    type_ = []
    chords_or_tab = driver.find_elements_by_css_selector('._1_CWK')
    for item in chords_or_tab:
        type_.append(item.text)


    for i in range(len(link_element)):
        if type_[i] != 'Chords':
            continue # Skip any songs that aren't of type Chord
        page_link.append(link_element[i].get_attribute('href')) # Retrieve the hyperlink element for each song
        song_name.append(link_element[i].text) # Retrieve the song name

print("Initial scrape complete. Scraping " + str(len(song_name)) + " songs.")

song_chords = []
for i in range(len(page_link)):
    driver.get(page_link[i]) # Get the song page
    chord_elements = driver.find_elements_by_css_selector('._3ffP6') # Select the Song list element
    chords = []
    for i in range(len(chord_elements)):
        chords.append(chord_elements[i].text) # Save the chord elements for each song to a vector
    song_chords.append(" ".join(chords)) # Turn the list of chords in to a single string
    print("Scraped " + str(len(song_chords)) + " out of " + str(len(link_element)))

to_df = list(zip(song_name,song_chords)) # Create a tuple of the song name with its chords
data = pd.DataFrame(to_df, columns=['Song Name','Chords']) # Create a data frame of the song with its chords

data.to_csv('./Data_OUT/songs_with_chords_' + str(p_to_s) + '_pages.csv')

print("Scrape completed.")
