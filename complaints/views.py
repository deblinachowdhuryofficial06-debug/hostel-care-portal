from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Complaint, Comment
from .forms import StudentRegistrationForm, WardenRegistrationForm, ComplaintForm, CommentForm

# --- HOME & AUTH VIEWS ---

def home_portal(request):
    """
    Public Home Page: Choice portal to enter as Student or Warden.
    """
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('warden_dashboard')
        return redirect('dashboard')
    return render(request, 'complaints/home_portal.html')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False       # 🌟 GUARANTEE: Force student role
            user.is_superuser = False   # 🌟 GUARANTEE: Force non-admin
            user.save()
            
            login(request, user)
            return redirect('dashboard') # 🌟 Directs straight to Student Dashboard
    else:
        form = StudentRegistrationForm()
    return render(request, 'complaints/register_student.html', {'form': form})


def register_warden(request):
    """
    Registers wardens (is_staff = True automatically).
    """
    if request.method == 'POST':
        form = WardenRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('warden_dashboard')
    else:
        form = WardenRegistrationForm()
    return render(request, 'complaints/register_warden.html', {'form': form})


def login_view(request):
    """
    Handles login and routes users strictly based on their is_staff flag.
    """
    role = request.GET.get('role', 'student')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # SMART ROUTING: Staff/Warden -> Warden Dashboard, Student -> Student Dashboard
                if user.is_staff:
                    return redirect('warden_dashboard')
                return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'complaints/login.html', {'form': form, 'role': role})


def logout_view(request):
    """
    Logs out the user and redirects back to the main Homepage.
    """
    logout(request)
    return redirect('home_portal')


# --- DASHBOARDS ---

@login_required(login_url='login')
def dashboard(request):
    # Temporarily commented out to prevent ANY automatic redirection to Warden page:
    # if request.user.is_staff:
    #     return redirect('warden_dashboard')

    complaints = Complaint.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'complaints/dashboard.html', {'complaints': complaints})
@login_required(login_url='login')
def warden_dashboard(request):
    """
    Warden Dashboard: Shows ALL hostel complaints globally across all students.
    """
    # Guardrail: If a regular Student tries to access, send them back to Student Dashboard
    if not request.user.is_staff:
        return redirect('dashboard')

    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'complaints/warden_dashboard.html', {'complaints': complaints})


# --- COMPLAINT ACTIONS ---

@login_required(login_url='login')
def create_complaint(request):
    """
    Allows a student to file a new complaint.
    """
    if request.user.is_staff:
        return redirect('warden_dashboard')

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user
            complaint.save()
            return redirect('dashboard')
    else:
        form = ComplaintForm()

    return render(request, 'complaints/create_complaint.html', {'form': form})


@login_required(login_url='login')
def complaint_detail(request, pk):
    """
    Chat & Conversation page between Student and Warden for a specific complaint.
    """
    complaint = get_object_or_404(Complaint, pk=pk)

    # Security: Only the owner student OR a warden can view the conversation thread
    if not request.user.is_staff and complaint.student != request.user:
        return redirect('dashboard')

    comments = complaint.comments.all().order_by('created_at')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.complaint = complaint
            comment.author = request.user
            comment.save()
            return redirect('complaint_detail', pk=pk)
    else:
        comment_form = CommentForm()

    return render(request, 'complaints/complaint_detail.html', {
        'complaint': complaint,
        'comments': comments,
        'comment_form': comment_form
    })


@login_required(login_url='login')
def update_status(request, pk):
    """
    Allows Warden to update the status (Pending, In Progress, Resolved) directly.
    """
    if not request.user.is_staff:
        return redirect('dashboard')

    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'In Progress', 'Resolved']:
            complaint.status = new_status
            complaint.save()

    return redirect('warden_dashboard')