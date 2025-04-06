import streamlit as st # type: ignore                               # For creating the web app interface
import folium # type: ignore                                        # For creating interactive maps
import pandas as pd
from streamlit_folium import folium_static # type: ignore           # To display the Folium map inside the Streamlit app
from folium import IFrame # type: ignore                            # To embed HTML content (like images) inside map popups

# App Title
st.title("🌍 Our Memory Map")                                       # Adds a big, bold title to app.

# Create the memory map
memory_map = folium.Map(location=[47.5289, 21.6254], zoom_start=5)
    #folium.Map() → This function creates a new map.
    #location=[47.5289, 21.6254] → This sets the center of the map (latitude & longitude coordinates). In this case, it centers on Debrecen, Hungary.
    #zoom_start=5 → Controls how zoomed in the map is when it loads. (Higher values like 10-12 mean a closer view./Lower values like 3-5 show a wider region.)

# Add memory markers of the places we have been to and have memories in (imgs must be .jpg / .png)
memories = [
#creates a list of dictionaries
    {
        "location": [47.5371, 21.6408],
        "title": "University of Debrecen, Engineering Building - The Beginning of it All",
        "description": "It would be unreal if I forget this spot. Our university building is thrown somewhere in the nowhere, but this is where I found my everywhere.",
        "photo_url": "https://www.debrecensun.hu/media/24/05/20/The-building-complex-of-the-Faculty-of-Engineering-is-being-renewed-and-expanded.jpg",
        "icon": "university",
        "color":"beige"
    },
    {
        "location": [47.5550, 21.6183],
        "title": "Learning Center - The First Long Walk",
        "description": "Do you remember this day? I wonder. It was the first time you told me about Faia, and it was the first time I scrolled through your phone. I was looking at your Anghami list and could barely find a song or two that I knew.",
        "photo_url": "https://basiccollection.com/wp-content/uploads/2023/02/lc_22-1536x1024.jpg",
        "icon": "book",
        "color": "beige"
    },
    {
        "location": [47.5522, 21.6261],
        "title": "Nagyerdei Park - The Long Talks, The First Walks",
        "description": "Isn't this the start of it all? All our first conversations, all the little talks, and a bunch of firsts.",
        "photo_url": "https://www.trfihi-parks.com/images/parks/VRk8zd_1586967343_qccccccccccccccccc.jpg",
        "song_url": "https://cdn.jsdelivr.net/gh/hna-hisham/memory_map_songs/AnaBashaaNagat.mp3",
        "icon": "leaf",
        "color": "green"
    },
    {
        "location": [47.5522, 21.6261],
        "title": "Burger King Date Night - The Late Night Walk Throughs",
        "description": "It will remain one of my favorite spots, and one of the most places we've been to as a date spot. I love you, and I hope one day we can have another meal here together.",
        "photo_url": "https://www.trfihi-parks.com/images/parks/VRk8zd_1586967343_qccccccccccccccccc.jpg",
        "icon": "leaf",
        "color": "green"
    },
    #{
    #    "location": [ ],
    #    "title": " ",
    #    "description": " ",
    #    "photo_url": " ",
    #    "icon": " ",
    #    "color": " "
    #}
]

# Add markers for each memory
    # Start building the popup with the description

# Add the photo if available
for memory in memories: #Creates an HTML string to embed the image.
    popup_html = f"<b>{memory['title']}</b><br>{memory['description']}<br>"

    if memory.get("photo_url"):
        popup_html += f'<img src="{memory["photo_url"]}" width="250"><br>'

    if "song_url" in memory:
        popup_html += f"""
        <audio controls>
          <source src="{memory['song_url']}" type="audio/mpeg">
          Your browser does not support the audio element.
        </audio>
        """


    folium.Marker(
        location=memory["location"],
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color=memory['color'], icon=memory['icon'])
    ).add_to(memory_map)





# Create the List of Dictionaries of the Surprise Notes (Funny Places and Stuff)
surprise_notes = [
    {
        "location": [48.8566, 2.3522],  # Paris
        "title": "Paris - The 'Fancy Date' Dream",
        "note": "If we go here, I'm making you try escargot... Good luck. 🐌"
    },
    {
        "location": [52.5200, 13.4050],  # Berlin
        "title": "Berlin - The Tech Geek City",
        "note": "This is where you'll probably explain every gadget we pass by. 🤓"
    },
    {
        "location": [35.6762, 139.6503],  # Tokyo
        "title": "Tokyo - Anime Overload",
        "note": "I’m warning you... I WILL drag you into every anime shop here. 🎌"
    }
]

# Adding Surprise Love Notes
for note in surprise_notes:
    folium.CircleMarker(
        location=note["location"],
        radius=3,  # Smaller size for "hidden" effect
        color='gray',
        fill=True,
        fill_color='gray',
        fill_opacity=0.5,
        popup=folium.Popup(f"<b>{note['title']}</b><br>{note['note']}", max_width=300)
    ).add_to(memory_map)




#The Pop Up Questions Section
# Sample questions
questions = [
    "Me or Me?",
    "Coffee or tea?",
    "Favorite childhood memory?",
    "If you could visit one place tomorrow, where would it be?"
]

# Load or create a spreadsheet
try:
    answers_df = pd.read_csv('answers.csv')
except FileNotFoundError:
    answers_df = pd.DataFrame(columns=['Question', 'Answer'])

# Ask a random question
import random
random_question = random.choice([q for q in questions if q not in answers_df['Question'].tolist()])

st.sidebar.write("❓ **Memory Quest Question**")
answer = st.sidebar.text_input(random_question)

if answer:
    new_entry = pd.DataFrame({'Question': [random_question], 'Answer': [answer]})
    answers_df = pd.concat([answers_df, new_entry], ignore_index=True)
    answers_df.to_csv('answers.csv', index=False)
    st.sidebar.success("Answer saved!")


# Display the map
folium_static(memory_map)

# Closing Message
st.markdown("""
💌 Every marker holds a memory, a promise, or a dream we’ll make come true.  
I can’t wait to create even more memories with you. ❤️
""")