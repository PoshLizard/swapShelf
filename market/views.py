from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from market.forms import ListingForm, ProfileForm
from market.models import Listing, Message, Thread


def home(request):
    listings = Listing.objects.select_related("owner").exclude(status="removed")
    category = request.GET.get("category") or ""
    if category:
        listings = listings.filter(category=category)
    return render(request, "market/home.html", {"listings": listings, "category": category})


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, "market/detail.html", {"listing": listing})


@login_required
def listing_new(request):
    form = ListingForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        listing = form.save(commit=False)
        listing.owner = request.user
        listing.save()
        return redirect("listing_detail", pk=listing.pk)
    return render(request, "market/form.html", {"form": form, "heading": "Post a listing"})


@login_required
def listing_edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    form = ListingForm(request.POST or None, instance=listing)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("listing_detail", pk=listing.pk)
    return render(request, "market/form.html", {"form": form, "heading": "Edit listing", "listing": listing})


@login_required
@require_POST
def listing_sold(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    listing.status = "sold"
    listing.save(update_fields=["status"])
    return redirect("listing_detail", pk=listing.pk)


@login_required
@require_POST
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    listing.status = "removed"
    listing.save(update_fields=["status"])
    return redirect("home")


@login_required
def mine(request):
    listings = Listing.objects.filter(owner=request.user).exclude(status="removed")
    threads = Thread.objects.filter(buyer=request.user) | Thread.objects.filter(listing__owner=request.user)
    threads = threads.select_related("listing", "buyer").distinct()
    return render(request, "market/mine.html", {"listings": listings, "threads": threads})


@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(Thread.objects.select_related("listing", "buyer", "listing__owner"), pk=pk)
    if request.method == "POST":
        body = (request.POST.get("body") or "").strip()
        if body:
            Message.objects.create(thread=thread, sender=request.user, body=body)
        return redirect("thread_detail", pk=thread.pk)
    return render(request, "market/thread.html", {"thread": thread, "messages": thread.messages.select_related("sender")})


@login_required
def start_thread(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    thread, _ = Thread.objects.get_or_create(listing=listing, buyer=request.user)
    return redirect("thread_detail", pk=thread.pk)


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")
    return render(request, "market/register.html", {"form": form})


def sign_in(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("home")
    return render(request, "market/login.html", {"form": form})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("profile")
    return render(request, "market/profile.html", {"form": form})


@login_required
def desk(request):
    if not request.user.is_staff:
        return render(request, "market/desk.html", {"allowed": False})
    return render(
        request,
        "market/desk.html",
        {
            "allowed": True,
            "note": "Department hold closet, Hullihen basement cage B. Reimbursement code DESK-2290. Not for the public board.",
        },
    )
