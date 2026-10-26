# SwapShelf — Security Writeup

**Github repo:** https://github.com/PoshLizard/swapShelf

**Hosted Link:** _<add after deploying>_

---

## How a listing id becomes a row

When you post, the request goes to `listing_new()` in `market/views.py`. It
hands the POST to `ListingForm`, calls `form.save(commit=False)`, sets
`listing.owner = request.user`, then `.save()`. The Django ORM runs an
`INSERT INTO market_listing (...)` and SQLite hands back an auto-increment
`id`. That `id` is the primary key.

When someone later opens `/listings/5/`, the URL pattern
`listings/<int:pk>/` in `market/urls.py` captures `5` as `pk` and passes it to
`listing_detail(request, pk)`, which runs:

```
get_object_or_404(Listing, pk=pk)   ->   SELECT ... FROM market_listing WHERE id = 5
```

Match -> the row object is rendered. No match -> 404.

## Which pages a logged-out visitor can open

Anything without `@login_required`:

- `/` — the public board (`home`)
- `/listings/<pk>/` — a single listing's detail page (`listing_detail`)
- `/register/` and `/login/`

The detail page shows title, price, description, seller name, and status — it
does **not** show the private `seller_note`. Everything else (post, edit, mark
sold, delete, my stuff, message threads, profile, desk) is behind
`@login_required`, and `/admin/` additionally needs a staff account.

## What the profile form writes back to the user

`/profile/` binds `ProfileForm` to `request.user` and saves it, running an
`UPDATE auth_user ... WHERE id = <your id>`. After the patch the form writes
back **first name, last name, and email only**. (Before the patch it also
wrote `is_staff` — see the vulnerability below.)

## What the department desk is for, and who can open it

`/desk/` (`desk()` in `market/views.py`) is the department board's page. For a
staff account it shows a held note — the department hold-closet location and a
reimbursement code (`DESK-2290`) — not meant for the public board. The view
gates on a single check: `if not request.user.is_staff`. So only accounts with
`is_staff = True` can open it. Staff is meant to be granted out of band (by an
admin), the same way the seed's advisor-style account would be.

---

## Vulnerability: Privilege escalation via the profile form (mass assignment)

This is a **broken access control / mass-assignment** flaw.

`ProfileForm` (in `market/forms.py`) listed `is_staff` as an editable field and
hid it behind a friendly label:

```python
fields = ["first_name", "last_name", "email", "is_staff"]
labels = { "is_staff": "Show my name on the department board" }
```

But `is_staff` is not a cosmetic preference — it is Django's authorization
flag. The `desk()` view trusts it directly, and it is also what Django's
`/admin/` login checks. Because the profile view saves whatever the form
validates, any logged-in student could flip their own `is_staff` to `True`.
The checkbox that looks like a display toggle actually grants staff.

### How to trigger it

You only need a normal student account — no tools, no crafted requests.

1. Sign in as any student (e.g. `alex` / `campus123`), or register a fresh
   account.
2. Open `/desk/` -> denied: *"This page is for department board accounts."*
3. Open `/profile/`, tick the box **"Show my name on the department board"**,
   and click **Save profile**. (That box is the `is_staff` field.)
4. Open `/desk/` again -> it now shows the held note:
   *"Department hold closet, Hullihen basement cage B. Reimbursement code
   DESK-2290."*
5. The account can now also reach the `/admin/` login as a staff user.

Even if the checkbox were removed from the page, an attacker could POST
`is_staff=on` straight to `/profile/` and get the same result — the real bug is
that the field was writable at all.

### The patch

`is_staff` is removed from the form's editable fields, so the account holder can
no longer set it. Staff is granted out of band only (admin / `manage.py`).

```python
# market/forms.py
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]   # no is_staff
```

Normal posting and editing are untouched (`ListingForm` is unchanged).
Verified: `manage.py check` passes, and a POST that injects `is_staff=1` is now
ignored — the saved user stays `is_staff = False`.

---

## Architecture Sketch

```
                 SwapShelf  —  Django 5.1 + SQLite

   ┌───────────┐   HTTP request (+ session cookie)   ┌───────────────────────┐
   │  Browser  │  ────────────────────────────────►  │  swapshelf/urls.py    │
   │ student / │                                      │  URLconf, captures pk │
   │ visitor   │  ◄────────────────────────────────  └──────────┬────────────┘
   └───────────┘        rendered HTML template                   │
                                                                  ▼
       @login_required gate                          ┌───────────────────────┐
       (new, edit, sold, delete,  ──────────────────►│  market/views.py      │
        mine, thread, profile, desk)                 │  one function per page │
                                                      └───┬───────────────┬───┘
                                               forms:     │               │  render
                                          validate/save   ▼               ▼
                                              ┌──────────────────┐  ┌──────────────┐
                                              │ market/forms.py  │  │  templates/  │
                                              │ ListingForm      │  │  *.html      │
                                              │ ProfileForm      │  └──────────────┘
                                              └────────┬─────────┘
                                                       │  Django ORM
                                                       ▼
                                              ┌──────────────────┐
                                              │ market/models.py │
                                              └────────┬─────────┘
                                                       │  SQL
                                                       ▼
                                              ┌──────────────────┐
                                              │ SQLite            │
                                              │ data/swapshelf.db │
                                              └──────────────────┘

   Data model (one-to-many):

       User ──< Listing ──< Thread ──< Message
                (owner)    (buyer)    (sender)

       Listing.id  =  the <int:pk> in  /listings/<pk>/

   Public  vs  login-required:

       open to anyone :  /   /listings/<pk>/   /register/   /login/
       login required :  /listings/new /edit /sold /delete   /me
                         /threads/<pk>   /profile   /desk   (/admin needs staff)

   Request -> row:

       POST /listings/new  ->  ListingForm valid -> owner = you -> INSERT -> new id
       GET  /listings/5/   ->  SELECT * FROM market_listing WHERE id = 5 -> row / 404
```
