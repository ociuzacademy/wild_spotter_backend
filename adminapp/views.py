from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from .models import *
from .forms import *


# ------------------------
# Admin Authentication Views
# ------------------------

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdminProfile, ForestOfficer
def admin_officer_login(request):

    if request.method == "POST":

        login_type = request.POST.get("login_type")

        # ADMIN FIELDS
        admin_email = request.POST.get("email")
        admin_password = request.POST.get("admin_password")  # NEW FIELD NAME ✔

        # OFFICER FIELDS (unchanged)
        officer_id = request.POST.get("officer_id")
        officer_password = request.POST.get("password")      # SAME AS BEFORE ✔

        print("------ DEBUG ------")
        print("Login Type:", login_type)
        print("Admin Email:", admin_email)
        print("Admin Password:", admin_password)
        print("Officer ID:", officer_id)
        print("Officer Password:", officer_password)
        print("-------------------")

        # -------- ADMIN LOGIN --------
        if login_type == "admin":
            try:
                admin = AdminProfile.objects.get(
                    email__iexact=admin_email.strip(),
                    admin_password=admin_password.strip()
                )

                request.session["admin_id"] = admin.id
                request.session["admin_name"] = admin.name
                request.session["user_role"] = "admin"

                return redirect("admin_dashboard")

            except AdminProfile.DoesNotExist:
                messages.error(request, "Invalid admin email or password")
                return redirect("admin_officer_login")

        # -------- OFFICER LOGIN (UNCHANGED) --------
        elif login_type == "officer":
            try:
                officer = ForestOfficer.objects.get(
                    officer_id=officer_id.strip(),
                    password=officer_password.strip()
                )

                request.session["officer_id"] = officer.id
                request.session["officer_name"] = officer.name
                request.session["user_role"] = "forest_officer"

                return redirect("forest_dashboard")

            except ForestOfficer.DoesNotExist:
                messages.error(request, "Invalid officer ID or password")
                return redirect("admin_officer_login")

    return render(request, "login.html")

def admin_logout(request: HttpRequest) -> HttpResponse:
    """Logs out the admin and clears session."""
    request.session.flush()
    return redirect('admin_officer_login')

from django.shortcuts import render, redirect
from django.utils import timezone
from wildspotter_api.models import TblRegister
from adminapp.models import TblWildLifeSanctuary, WildAnimal,ForestOfficer
from wildspotter_api.models import Journal

from adminapp.models import Community, ForestOfficer
from wildspotter_api.models import RecentSighting, Journal

def admin_dashboard(request):
    if 'admin_id' not in request.session:
        return redirect('admin_officer_login')

    # Basic counts
    total_users = TblRegister.objects.count()
    total_sanctuaries = TblWildLifeSanctuary.objects.count()
    total_animals = WildAnimal.objects.count()

    # New report counts
    total_communities = Community.objects.count()
    total_sightings = RecentSighting.objects.count()
    total_officers = ForestOfficer.objects.count()
    total_journals = Journal.objects.count()
    published_journals = Journal.objects.filter(status="Published").count()
    pending_journals = Journal.objects.filter(status="Pending").count()

    # Last 3 journals
    recent_journals = Journal.objects.filter(status="Published").order_by('-created_at')[:3]

    return render(request, 'adminapp/admin_dashboard.html', {
        "admin_name": request.session.get('admin_name'),

        # OLD
        "total_users": total_users,
        "total_sanctuaries": total_sanctuaries,
        "total_animals": total_animals,

        # NEW REPORT DATA
        "total_communities": total_communities,
        "total_sightings": total_sightings,
        "total_officers": total_officers,
        "total_journals": total_journals,
        "published_journals": published_journals,
        "pending_journals": pending_journals,

        "recent_journals": recent_journals,
        "now": timezone.now(),
    })

# ------------------------
# Wild Animal Category Views
# ------------------------
def add_animal_category(request: HttpRequest) -> HttpResponse:
    """Add a new wild animal category."""
    if 'admin_id' not in request.session:
        messages.warning(request, "Please log in first.")
        return redirect('admin_officer_login')

    if request.method == 'POST':
        form = WildAnimalCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Animal category added successfully!')
            return redirect('list_animal_category')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = WildAnimalCategoryForm()

    return render(request, 'adminapp/category/add_animal_category.html', {'form': form})


def list_animal_category(request: HttpRequest) -> HttpResponse:
    """List all animal categories."""
    if 'admin_id' not in request.session:
        return redirect('admin_officer_login')

    categories = WildAnimalCategory.objects.all()
    return render(request, 'adminapp/category/list_animal_category.html', {'categories': categories})


def edit_animal_category(request: HttpRequest, category_id: int) -> HttpResponse:
    """Edit existing animal category."""
    if 'admin_id' not in request.session:
        return redirect('admin_officer_login')

    category = get_object_or_404(WildAnimalCategory, id=category_id)
    form = WildAnimalCategoryForm(request.POST or None, instance=category)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Category updated successfully!')
        return redirect('list_animal_category')

    return render(request, 'adminapp/category/add_animal_category.html', {'form': form, 'edit_mode': True})


def delete_animal_category(request: HttpRequest, category_id: int) -> HttpResponse:
    """Delete a category."""
    if 'admin_id' not in request.session:
        return redirect('admin_officer_login')

    category = get_object_or_404(WildAnimalCategory, id=category_id)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('list_animal_category')



# ------------------------
# Wild Animal  Views
# ------------------------
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import WildAnimalForm

def add_animal(request):
    """View to add a new wild animal."""
    if request.method == "POST":
        form = WildAnimalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Animal added successfully!")
            return redirect('add_animal')  # Redirect to same page or another if you prefer
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = WildAnimalForm()
    
    return render(request, 'adminapp/animal/add_animal.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import WildAnimal, WildAnimalCategory

from django.core.paginator import Paginator

def view_animals(request):
    """Show animal gallery with search, filter and pagination."""
    
    query = request.GET.get('q')
    category_filter = request.GET.get('category')

    animals = WildAnimal.objects.select_related('category').order_by('-created_at')
    categories = WildAnimalCategory.objects.all().order_by('name')

    # Search filter
    if query:
        animals = animals.filter(name__icontains=query)

    # Category filter
    if category_filter and category_filter != 'all':
        animals = animals.filter(category__id=category_filter)

    # PAGINATION (20 per page)
    paginator = Paginator(animals, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'animals': page_obj,     # paginated list
        'page_obj': page_obj,    # pagination object
        'categories': categories,
        'selected_category': category_filter,
        'query': query,
    }
    return render(request, 'adminapp/animal/view_animals.html', context)


def view_animal_details(request, animal_id):
    """Show full details of a single wild animal."""
    animal = get_object_or_404(WildAnimal, id=animal_id)
    return render(request, 'adminapp/animal/view_animal_details.html', {'animal': animal})

from django.shortcuts import get_object_or_404

def edit_animal(request, animal_id):
    """Edit an existing wild animal."""
    animal = get_object_or_404(WildAnimal, id=animal_id)
    if request.method == "POST":
        form = WildAnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, "Animal updated successfully!")
            return redirect('view_animals')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = WildAnimalForm(instance=animal)
    return render(request, 'adminapp/animal/edit_animal.html', {'form': form, 'animal': animal})


def delete_animal(request, animal_id):
    """Delete a wild animal after confirmation."""
    animal = get_object_or_404(WildAnimal, id=animal_id)
    if request.method == "POST":
        animal.delete()
        messages.success(request, "Animal deleted successfully!")
        return redirect('view_animals')
    return render(request, 'adminapp/animal/confirm_delete_animal.html', {'animal': animal})






# ------------------------
# Wild Animal  Views
# ------------------------
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TblWildLifeSanctuary, TblSanctuaryImage
def add_wildlife_sanctuary(request):
    if request.method == "POST":
        name = request.POST.get('name')
        species_count = request.POST.get('species_count')
        hectare = request.POST.get('hectare')
        viewpoints = request.POST.get('viewpoints')
        visitors_per_month = request.POST.get('visitors_per_month')
        about = request.POST.get('about')
        images = request.FILES.getlist('images')

        if not (name and species_count and hectare and about):
            messages.error(request, "All fields are required!")
            return redirect('add_wildlife_sanctuary')

        sanctuary = TblWildLifeSanctuary.objects.create(
            name=name,
            species_count=species_count,
            hectare=hectare,
            viewpoints=viewpoints or 0,
            visitors_per_month=visitors_per_month or 0,
            about=about
        )

        for img in images:
            TblSanctuaryImage.objects.create(sanctuary=sanctuary, image=img)

        messages.success(request, f"Sanctuary '{name}' added successfully!")
        return redirect('list_wildlife_sanctuary')

    return render(request, 'adminapp/sanctuary/add_wildlife_sanctuary.html')

from django.shortcuts import render, get_object_or_404
from .models import TblWildLifeSanctuary

# List view
def list_wildlife_sanctuary(request):
    sanctuaries = TblWildLifeSanctuary.objects.all().order_by('-created_at')
    return render(request, 'adminapp/sanctuary/list_wildlife_sanctuary.html', {'sanctuaries': sanctuaries})


# Detail view
def view_sanctuary_details(request, sanctuary_id):
    sanctuary = get_object_or_404(TblWildLifeSanctuary.objects.prefetch_related('images'), id=sanctuary_id)
    return render(request, 'adminapp/sanctuary/view_sanctuary_details.html', {'sanctuary': sanctuary})

def delete_wildlife_sanctuary(request, id):
    sanctuary = get_object_or_404(TblWildLifeSanctuary, id=id)
    sanctuary.delete()
    messages.success(request, f"Sanctuary '{sanctuary.name}' has been deleted.")
    return redirect('list_wildlife_sanctuary')
def edit_wildlife_sanctuary(request, id):
    sanctuary = get_object_or_404(TblWildLifeSanctuary, id=id)

    if request.method == "POST":
        sanctuary.name = request.POST.get('name')
        sanctuary.species_count = request.POST.get('species_count')
        sanctuary.hectare = request.POST.get('hectare')
        sanctuary.viewpoints = request.POST.get('viewpoints')
        sanctuary.visitors_per_month = request.POST.get('visitors_per_month')
        sanctuary.about = request.POST.get('about')
        sanctuary.save()

        messages.success(request, "Sanctuary updated successfully!")
        return redirect('list_wildlife_sanctuary')

    return render(request, "adminapp/sanctuary/edit_wildlife_sanctuary.html", {
        "sanctuary": sanctuary
    })


# ------------------------
#  Community  Views
# ------------------------
from django.shortcuts import render, redirect
from .models import Community, TblWildLifeSanctuary
from django.contrib import messages

def add_community(request):
    sanctuaries = TblWildLifeSanctuary.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        sanctuary_id = request.POST.get('sanctuary')
        picture = request.FILES.get('picture')

        if not name or not sanctuary_id:
            messages.error(request, "Please fill all required fields.")
            return redirect('add_community')

        sanctuary = TblWildLifeSanctuary.objects.get(id=sanctuary_id)
        community = Community.objects.create(
            name=name,
            sanctuary=sanctuary,
            picture=picture
        )
        messages.success(request, f"Community '{community.name}' added successfully!")
        return redirect('add_community')

    return render(request, 'adminapp/community/add_community.html', {'sanctuaries': sanctuaries})


from django.shortcuts import render
from .models import Community

def list_community(request):
    """View all communities with sanctuary details."""
    communities = Community.objects.select_related('sanctuary').all()
    return render(request, 'adminapp/community/list_community.html', {'communities': communities})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Community, TblWildLifeSanctuary

def edit_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    sanctuaries = TblWildLifeSanctuary.objects.all()

    if request.method == 'POST':
        community.name = request.POST.get('name')
        sanctuary_id = request.POST.get('sanctuary')
        community.sanctuary = TblWildLifeSanctuary.objects.get(id=sanctuary_id)
        community.members = request.POST.get('members', community.members)

        if request.FILES.get('picture'):
            community.picture = request.FILES['picture']

        community.save()
        messages.success(request, 'Community updated successfully!')
        return redirect('list_community')

    return render(request, 'adminapp/community/edit_community.html', {'community': community, 'sanctuaries': sanctuaries})


def delete_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    community.delete()
    messages.success(request, 'Community deleted successfully!')
    return redirect('list_community')



# ------------------------
# Topic for journal
# ------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from adminapp.models import Topic

def manage_topics(request):
    """Add, edit, delete and list topics in one function."""

    if 'admin_id' not in request.session:
        return redirect('admin_officer_login')

    topics = Topic.objects.all()

    # ---------- DELETE ----------
    delete_id = request.GET.get("delete")
    if delete_id:
        topic = get_object_or_404(Topic, id=delete_id)
        topic.delete()
        messages.success(request, "Topic deleted successfully!")
        return redirect('manage_topics')

    # ---------- EDIT MODE ----------
    edit_id = request.GET.get("edit")
    edit_topic = None
    if edit_id:
        edit_topic = get_object_or_404(Topic, id=edit_id)

    # ---------- ADD / UPDATE ----------
    if request.method == "POST":
        name = request.POST.get("name")

        if not name:
            messages.error(request, "Topic name cannot be empty.")
            return redirect('manage_topics')

        # If editing → update
        if edit_topic:
            edit_topic.name = name
            edit_topic.save()
            messages.success(request, "Topic updated successfully!")
        else:
            # Check duplicates
            if Topic.objects.filter(name__iexact=name).exists():
                messages.warning(request, "This topic already exists!")
            else:
                Topic.objects.create(name=name)
                messages.success(request, "Topic added successfully!")

        return redirect('manage_topics')

    return render(request, 'adminapp/topics/manage_topics.html', {
        "topics": topics,
        "edit_topic": edit_topic
    })




# ------------------------
# List and manage  journal
# ------------------------


from django.shortcuts import render
from django.contrib import messages
from wildspotter_api.models import TblRegister
from adminapp.models import Topic
from wildspotter_api.models import Journal  # if you placed Journal in userapp

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from wildspotter_api.models import Journal

def list_journals(request):

    pending_journals = Journal.objects.filter(status="draft").select_related('user', 'topic')
    approved_journals = Journal.objects.filter(status="Published").select_related('user', 'topic')
    rejected_journals = Journal.objects.filter(status="rejected").select_related('user', 'topic')

    return render(request, 'adminapp/journal/list_journals.html', {
        'pending_journals': pending_journals,
        'approved_journals': approved_journals,
        'rejected_journals': rejected_journals,
    })


def approve_journal(request, journal_id):
    if 'admin_id' not in request.session:
        return redirect('admin_officer_login')

    journal = get_object_or_404(Journal, id=journal_id)
    journal.status = "Published"
    journal.save()

    messages.success(request, "Journal approved successfully!")
    return redirect('list_journals')

def reject_journal(request, journal_id):
    if 'admin_id' not in request.session:
        return redirect('admin_officer_login')

    journal = get_object_or_404(Journal, id=journal_id)
    journal.status = "rejected"
    journal.save()

    messages.warning(request, "Journal rejected!")
    return redirect('list_journals')

# ------------------------
# View Users
# ------------------------
def view_users(request):
    users = TblRegister.objects.all()
    return render(request, 'adminapp/users/view_users.html', {'users': users})


# ------------------------
# Manage Forest officer
# ------------------------

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ForestOfficer

from adminapp.models import TblWildLifeSanctuary

def add_forest_officer(request):
    if 'admin_id' not in request.session:
        return redirect('admin_officer_login')

    sanctuaries = TblWildLifeSanctuary.objects.all().order_by('name')

    if request.method == "POST":
        officer_id = request.POST.get("officer_id")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        sanctuary_id = request.POST.get("sanctuary")

        profile_img = request.FILES.get("profile_image")
        idcard_img = request.FILES.get("id_card_image")

        sanctuary = TblWildLifeSanctuary.objects.get(id=sanctuary_id)

        ForestOfficer.objects.create(
            officer_id=officer_id,
            name=name,
            phone=phone,
            email=email,
            password=password,
            sanctuary=sanctuary,
            profile_image=profile_img,
            id_card_image=idcard_img,
        )

        messages.success(request, "Forest Officer added successfully!")
        return redirect("list_forest_officers")

    return render(request, "adminapp/officer/add_officer.html", {
        "sanctuaries": sanctuaries
    })

def list_forest_officers(request):
    if 'admin_id' not in request.session:
        return redirect('admin_officer_login')

    officers = ForestOfficer.objects.all()
    return render(request, "adminapp/officer/list_officers.html", {"officers": officers})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ForestOfficer

def edit_forest_officer(request, officer_id):
    if 'admin_id' not in request.session:
        return redirect('admin_officer_login')

    officer = get_object_or_404(ForestOfficer, id=officer_id)
    sanctuaries = TblWildLifeSanctuary.objects.all().order_by('name')

    if request.method == "POST":
        officer.officer_id = request.POST.get("officer_id")
        officer.name = request.POST.get("name")
        officer.phone = request.POST.get("phone")
        officer.email = request.POST.get("email")
        sanctuary_id = request.POST.get("sanctuary")
        officer.sanctuary = TblWildLifeSanctuary.objects.get(id=sanctuary_id)
        # Update password only if entered
        password = request.POST.get("password")
        if password:
            officer.password = password

        # Only replace images when uploaded
        if request.FILES.get("profile_image"):
            officer.profile_image = request.FILES["profile_image"]

        if request.FILES.get("id_card_image"):
            officer.id_card_image = request.FILES["id_card_image"]

        officer.save()

        messages.success(request, "Forest Officer updated successfully!")
        return redirect("list_forest_officers")

    return render(request, "adminapp/officer/edit_officer.html", {"officer": officer,"sanctuaries": sanctuaries})


def delete_forest_officer(request, officer_id):
    if 'admin_id' not in request.session:
        return redirect('admin_officer_login')

    officer = get_object_or_404(ForestOfficer, id=officer_id)
    officer.delete()

    messages.success(request, "Forest Officer deleted successfully!")
    return redirect("list_forest_officers")



#-------------------------
# View sightings by admin
#------------------------
from django.shortcuts import render
from wildspotter_api.models import RecentSighting

def admin_view_recent_sightings(request):
    if 'admin_id' not in request.session:
        return redirect('admin_officer_login')

    sightings = RecentSighting.objects.select_related(
        "user", "sanctuary"
    ).order_by("-created_at")

    return render(request, "adminapp/recent_sightings/admin_view_recent_sightings.html", {
        "sightings": sightings
    })




#-----------------------
# Forest Dashboard
#----------------------
from django.shortcuts import render, redirect
from adminapp.models import ForestOfficer, AwarenessPoster, EducationalVideo, WildlifeProtectionImage
from wildspotter_api.models import RecentSighting

def forest_dashboard(request):
    if 'officer_id' not in request.session:
        return redirect('admin_officer_login')

    officer = ForestOfficer.objects.select_related("sanctuary").get(id=request.session["officer_id"])

    # Count data added by officer
    poster_count = AwarenessPoster.objects.filter(officer=officer).count()
    video_count = EducationalVideo.objects.filter(officer=officer).count()
    protection_img_count = WildlifeProtectionImage.objects.filter(officer=officer).count()

    # Latest 3 recent sightings from HIS sanctuary
    recent_sightings = RecentSighting.objects.filter(
        sanctuary=officer.sanctuary
    ).select_related("user").order_by("-created_at")[:3]

    return render(request, "officer_module/officer_dashboard.html", {
        "officer": officer,
        "poster_count": poster_count,
        "video_count": video_count,
        "protection_img_count": protection_img_count,
        "recent_sightings": recent_sightings,
    })


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ForestOfficer

def forest_officer_profile(request):

    if 'officer_id' not in request.session:
        messages.error(request, "You must login first.")
        return redirect('admin_officer_login')

    try:
        officer = ForestOfficer.objects.get(id=request.session['officer_id'])
    except ForestOfficer.DoesNotExist:
        messages.error(request, "Officer not found.")
        return redirect('admin_officer_login')

    return render(request, 'officer_module/profile.html', {'officer': officer})


from django.shortcuts import render, redirect
from django.contrib import messages
from adminapp.models import ForestOfficer

def update_officer_profile(request):

    if "officer_id" not in request.session:
        messages.error(request, "Please login first.")
        return redirect("admin_officer_login")

    officer = ForestOfficer.objects.get(id=request.session["officer_id"])

    if request.method == "POST":

        officer.name = request.POST.get("name")
        officer.phone = request.POST.get("phone")
        officer.email = request.POST.get("email")

        # Profile Image
        if "profile_image" in request.FILES:
            officer.profile_image = request.FILES["profile_image"]

        # ID Card Image
        if "id_card_image" in request.FILES:
            officer.id_card_image = request.FILES["id_card_image"]

        officer.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("forest_officer_profile")

    return render(request, "officer_module/update_profile.html", {
        "officer": officer
    })





#----------------------------
#Forest view sanctary details
#---------------------------

from django.shortcuts import render, redirect
from wildspotter_api.models import RecentSighting
from adminapp.models import ForestOfficer

def officer_recent_sightings(request):

    # Check login
    if "officer_id" not in request.session:
        return redirect("admin_officer_login")

    officer = ForestOfficer.objects.select_related("sanctuary").get(id=request.session["officer_id"])

    # Get sightings only from HIS sanctuary
    sightings = RecentSighting.objects.filter(
        sanctuary=officer.sanctuary
    ).select_related("user", "sanctuary").order_by("-created_at")

    return render(request, "officer_module/recent_sightings.html", {
        "officer": officer,
        "sightings": sightings,
    })




from django.shortcuts import render, redirect
from django.contrib import messages
from adminapp.models import ForestOfficer
from .models import AwarenessPoster  # adjust import if needed

def add_awareness_poster(request):

    # Officer must be logged in
    if "officer_id" not in request.session:
        return redirect("admin_officer_login")

    officer = ForestOfficer.objects.get(id=request.session["officer_id"])

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        image = request.FILES.get("image")

        if not image:
            messages.error(request, "Poster image is required.")
            return redirect("add_awareness_poster")

        # Save poster
        AwarenessPoster.objects.create(
            officer=officer,
            title=title,
            description=description,
            category=category,
            image=image,
        )

        messages.success(request, "Awareness poster uploaded successfully!")
        return redirect("add_awareness_poster")

    return render(request, "officer_module/poster/add_poster.html", {
        "officer": officer
    })


def list_awareness_posters(request):

    if "officer_id" not in request.session:
        return redirect("admin_officer_login")

    officer = ForestOfficer.objects.get(id=request.session["officer_id"])

    posters = AwarenessPoster.objects.filter(officer=officer).order_by('-created_at')

    return render(request, "officer_module/poster/list_posters.html", {
        "posters": posters
    })



def edit_awareness_poster(request, poster_id):

    if "officer_id" not in request.session:
        return redirect("admin_officer_login")

    poster = get_object_or_404(AwarenessPoster, id=poster_id)

    if request.method == "POST":
        title = request.POST.get("title")
        category = request.POST.get("category")
        image = request.FILES.get("image")

        poster.title = title
        poster.category = category

        if image:
            poster.image = image  # replace old image

        poster.save()

        messages.success(request, "Poster updated successfully!")
        return redirect("list_awareness_posters")

    return render(request, "officer_module/poster/edit_poster.html", {
        "poster": poster
    })



def delete_awareness_poster(request, poster_id):

    if "officer_id" not in request.session:
        return redirect("admin_officer_login")

    try:
        poster = AwarenessPoster.objects.get(id=poster_id)
        poster.delete()
        messages.success(request, "Poster deleted successfully.")
    except AwarenessPoster.DoesNotExist:
        messages.error(request, "Poster not found.")

    return redirect("list_awareness_posters")

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from adminapp.models import EducationalVideo, ForestOfficer

def add_educational_video(request):
    officer_id = request.session.get("officer_id")
    officer = ForestOfficer.objects.get(id=officer_id)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        video = request.FILES.get("video")
        thumbnail = request.FILES.get("thumbnail")

        EducationalVideo.objects.create(
            officer=officer,
            title=title,
            description=description,
            category=category,
            video=video,
            thumbnail=thumbnail
        )

        messages.success(request, "Educational video uploaded successfully!")
        return redirect("list_educational_videos")

    return render(request, "officer_module/videos/add_video.html")


def list_educational_videos(request):
    officer_id = request.session.get("officer_id")
    videos = EducationalVideo.objects.filter(officer_id=officer_id)

    return render(request, "officer_module/videos/list_videos.html", {
        "videos": videos
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from adminapp.models import EducationalVideo, ForestOfficer

def edit_educational_video(request, video_id):
    officer_id = request.session.get("officer_id")
    officer = ForestOfficer.objects.get(id=officer_id)

    video = get_object_or_404(EducationalVideo, id=video_id, officer=officer)

    if request.method == "POST":
        video.title = request.POST.get("title")
        video.description = request.POST.get("description")
        video.category = request.POST.get("category")

        # Update Thumbnail if new file uploaded
        if request.FILES.get("thumbnail"):
            video.thumbnail = request.FILES.get("thumbnail")

        # Update Video if new file uploaded
        if request.FILES.get("video"):
            video.video = request.FILES.get("video")

        video.save()

        messages.success(request, "Educational video updated successfully!")
        return redirect("list_educational_videos")

    return render(request, "officer_module/videos/edit_video.html", {"video": video})





def delete_educational_video(request, video_id):
    video = get_object_or_404(EducationalVideo, id=video_id)
    video.delete()

    messages.success(request, "Video deleted successfully!")
    return redirect("list_educational_videos")







# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from adminapp.models import ForestOfficer
from .models import WildlifeProtectionImage

# Add protection image
def add_protection_image(request):
    officer_id = request.session.get("officer_id")
    if not officer_id:
        return redirect("admin_officer_login")

    officer = ForestOfficer.objects.get(id=officer_id)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        WildlifeProtectionImage.objects.create(
            officer=officer,
            title=title,
            description=description,
            image=image
        )

        messages.success(request, "Wildlife protection image uploaded successfully!")
        return redirect("list_protection_images")

    return render(request, "officer_module/protection_images/add_protection_image.html")


# List protection images
def list_protection_images(request):
    officer_id = request.session.get("officer_id")
    if not officer_id:
        return redirect("admin_officer_login")

    images = WildlifeProtectionImage.objects.filter(officer_id=officer_id)
    return render(request, "officer_module/protection_images/list_protection_images.html", {"images": images})


# Edit protection image
def edit_protection_image(request, image_id):
    image_obj = get_object_or_404(WildlifeProtectionImage, id=image_id)

    if request.method == "POST":
        image_obj.title = request.POST.get("title")
        image_obj.description = request.POST.get("description")

        if request.FILES.get("image"):
            image_obj.image = request.FILES.get("image")

        image_obj.save()

        messages.success(request, "Updated successfully!")
        return redirect("list_protection_images")

    return render(request, "officer_module/protection_images/edit_protection_image.html", {"image_obj": image_obj})


# Delete
def delete_protection_image(request, image_id):
    img = get_object_or_404(WildlifeProtectionImage, id=image_id)
    img.delete()
    messages.success(request, "Deleted successfully!")
    return redirect("list_protection_images")
