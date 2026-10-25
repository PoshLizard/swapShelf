# SwapShelf

Campus buy/sell board. Students post textbooks, chargers, and dorm leftovers. Buyers message the seller. Sellers can mark a listing sold.

Django, templates, SQLite.

## Features

- Register, sign in, sign out
- Public board with a category filter
- Post, edit, and mark sold
- Message threads on a listing
- Profile page (name, email, department-board flag)
- Department desk for board accounts

## Run locally

Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver 0.0.0.0:3000
```

Open http://localhost:3000. The database is `data/swapshelf.db`.

## Run with Docker

```bash
docker compose up --build
```

The app listens on port 3000.

## Demo accounts

Sign in with the username, not the email.

| Username | Password | Notes |
|---|---|---|
| `alex` | `campus123` | Has a charger and a bike |
| `jordan` | `campus123` | Has a textbook and a message thread |
| `sam` | `foundit!` | Has a sold lamp |

## Project layout

```
market/models.py     Listing, thread, message
market/views.py      Board, edit, messages, profile, desk
market/forms.py      Listing form and profile form
market/seed.py       First-run demo data
swapshelf/settings.py
```

## Assignment notes

Host this somewhere your classmates and instructor can reach. Walk the running app until you can explain:

- how a listing id becomes a row
- which pages a logged-out visitor can open
- what the profile form writes back to the user
- what the department desk is for, and who can open it

Then look for a security defect in the running system, document how to trigger it, and patch it without breaking normal posting. Submit the hosted URL, a short architecture sketch, the writeup, and the patched repo.
