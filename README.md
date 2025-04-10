🏥 Find_Med
Find_Med is a Django web application that helps users find nearby medical facilities using the Google Maps API.

🚀 Features
🔍 Search for medical facilities within a specified radius

📍 Display distance to selected hospital or clinic

🗺️ Interactive map with location markers

💡 Simple and user-friendly interface

🛠️ Tech Stack
Python 3.x

Django

Google Maps API

HTML/CSS

(Optional) JavaScript

⚙️ Installation
Clone the repository:


git clone https://github.com/Imper4ik/Find_Med
cd Find_Med
Create and activate a virtual environment:


python -m venv venv
source venv/bin/activate     # for macOS/Linux
venv\Scripts\activate        # for Windows
Install dependencies:


pip install -r requirements.txt
Add your Google Maps API key
Add it to your settings.py or use a .env file with python-dotenv.

Run migrations and start the server:


python manage.py migrate
python manage.py runserver


🧪 Example Use Case
Enter your location or use geolocation → choose a search radius → view the closest hospitals/clinics on the map → check the distance and choose where to go.

🗂️ File Structure

Find_Med/
├── medsearch/         # Main Django app
├── Find_Med/          # Project settings
├── db.sqlite3         # SQLite database
├── manage.py          # Django manager
├── requirements.txt
├── .gitignore
└── README.md
🔒 Security Tips
Never upload your .env or API keys to the repo

Add db.sqlite3 and other sensitive files to .gitignore

📜 License
MIT License

👤 Author
Created by imper4iik

