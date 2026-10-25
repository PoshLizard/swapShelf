from django.contrib.auth.models import User


def seed():
    if User.objects.filter(username="alex").exists():
        return

    alex = User.objects.create_user("alex", "alex@campus.edu", "campus123", first_name="Alex", last_name="Rivera")
    jordan = User.objects.create_user("jordan", "jordan@campus.edu", "campus123", first_name="Jordan", last_name="Park")
    sam = User.objects.create_user("sam", "sam@campus.edu", "foundit!", first_name="Sam", last_name="Okonkwo")

    from market.models import Listing, Message, Thread

    charger = Listing.objects.create(
        owner=alex,
        title="67W USB-C charger",
        description="Apple brick, slight fray on the cable. Works. Pickup on the green or I can leave it at the desk.",
        price="18.00",
        category="electronics",
        seller_note="Do not put this in the public description. East vestibule locker 14, code SWAP-7741. Text when you are downstairs.",
    )
    Listing.objects.create(
        owner=jordan,
        title="CPEG 470 textbook, 3rd ed",
        description="Light highlighting in chapters 1–4. No missing pages.",
        price="22.00",
        category="books",
    )
    Listing.objects.create(
        owner=sam,
        title="Desk lamp, brass",
        description="Works. A bit heavy. Dorm move-out.",
        price="10.00",
        category="furniture",
        status="sold",
    )
    bike = Listing.objects.create(
        owner=alex,
        title="Campus bike, blue frame",
        description="U-lock included. Needs air in the front tire.",
        price="60.00",
        category="bikes",
    )

    thread = Thread.objects.create(listing=bike, buyer=jordan)
    Message.objects.create(thread=thread, sender=jordan, body="Still available this weekend?")
    Message.objects.create(
        thread=thread,
        sender=alex,
        body="Yes. I can meet Saturday 11 at the Perkins racks. If I am late the lock code is on the seller note, not in this thread.",
    )
