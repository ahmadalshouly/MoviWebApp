# CineVault 🎬

A small Flask web app for tracking personal movie collections. Each user gets
their own list of movies; adding a movie automatically looks up its director,
release year, and poster via the [OMDb API](https://www.omdbapi.com/).

## Features

- Create users, each with their own movie collection
- Add a movie by title — director, year, and poster are fetched automatically
  from OMDb (falls back to manual entry if no API key is set or the title
  isn't found)
- Edit and delete movies
- Custom `404` and `500` error pages
- Robust error handling: database errors are caught, logged, and rolled back
  instead of crashing the app
- Ticket-stub styled UI (see `static/style.css`)

## Project structure

```
MovieWebApp/
├── app.py              # Flask routes
├── models.py            # SQLAlchemy models (User, Movie)
├── data_manager.py       # Database access layer
├── api/
    └── api_call.py           # OMDb API lookup
├── requirements.txt
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── users.html
│   ├── add_user.html
│   ├── add_movie.html
│   ├── movie_details.html
│   ├── success.html
│   ├── 404.html
│   └── 500.html
└── data/
    └── library.sqlite    # created automatically on first run
```

## Setup

1. **Clone/download the project** and open a terminal in its root folder.

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Set up your OMDb API key**, so movie details are looked up
   automatically instead of falling back to manual entry:

   - Get a free key at https://www.omdbapi.com/apikey.aspx
   - Create a file named `.env` in the project root:

     ```
     OMDB_API_KEY=your_key_here
     ```

   Without this step, the app still works — you just fill in director,
   year, and poster URL yourself when adding a movie.

5. **Run the app:**

   ```bash
   python app.py
   ```

   This creates `data/library.sqlite` on first run. Open
   http://127.0.0.1:5000 in your browser.