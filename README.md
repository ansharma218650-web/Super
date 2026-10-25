# SuperTET PRT Practice App

A chalkboard-and-notebook styled practice app: subject-wise MCQs with instant explanations,
plus timed mock tests with a question palette, review flags and full solutions.

## Run

    pip install -r requirements.txt
    streamlit run app.py

## Admin

Password lives in `.streamlit/secrets.toml` (default `admin123`; change it before sharing).

## Add content

- Open **Admin** to add one question, bulk-upload CSV/JSON, or edit/delete existing ones.
- Or drop JSON files into `data/practice/<subject>.json` and
  `data/test_series/<series>/<test>.json`.
- First time? Click **Load demo questions** on the Home page (copies from `sample_data/`, never overwrites).

## Project layout

    app.py            pages + styling
    utils.py          JSON/CSV storage helpers
    .streamlit/       theme (config.toml) and admin password (secrets.toml)
    data/             your questions and results.csv (created automatically)
    sample_data/      optional demo questions
