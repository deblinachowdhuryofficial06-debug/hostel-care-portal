from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Complaint, Comment
from .forms import ComplaintForm

from .forms import StudentRegistrationForm, WardenRegistrationForm

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'complaints/register_student.html', {'form': form})

def warden_register(request):
    if request.method == 'POST':
        form = WardenRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = WardenRegistrationForm()
    return render(request, 'complaints/register_warden.html', {'form': form})

def login_view(request):
    # Read whether the user clicked the student or warden button (defaults to student)
    role = request.GET.get('role', 'student')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Smart redirect based on who they are
                if user.is_staff:
                    return redirect('warden_dashboard')
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
        
    return render(request, 'complaints/login.html', {'form': form, 'role': role})
def logout_view(request):
    logout(request)
    return redirect('login')

# --- COMPLAINT CRUD VIEWS ---
@login_required(login_url='login')
def student_dashboard(request):
   my_complaints = Complaint.objects.filter(student=request.user).order_by('-created_at')
   return render(request, 'complaints/dashboard.html', {'complaints': my_complaints})

@login_required(login_url='login')
def create_complaint(request):
    # Create: Handle a student submitting a new complaint form
    if request.method == 'POST':
        # request.FILES handles the uploaded complaint images
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user # Lock this complaint to the logged-in student
            complaint.save()
            return redirect('dashboard')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/create_complaint.html', {'form': form})

@login_required(login_url='login')
def delete_complaint(request, pk):
    # Delete: Allow a student to cancel/delete their own complaint
    complaint = get_object_or_404(Complaint, pk=pk, student=request.user)
    if request.method == 'POST':
        complaint.delete()
        return redirect('dashboard')
    return render(request, 'complaints/delete_confirm.html', {'complaint': complaint})
@login_required(login_url='login')
def warden_dashboard(request):
    # Security Check: Redirect normal students away if they try to access this URL path
    if not request.user.is_staff:
        return redirect('dashboard')
        
    # Read: Fetch EVERY SINGLE complaint in the system
    all_complaints = Complaint.objects.all().order_by('-created_at')
    
    # Calculate simple statistics to show on the screen
    total = all_complaints.count()
    pending = all_complaints.filter(status='Pending').count()
    resolved = all_complaints.filter(status='Resolved').count()
    
    context = {
        'complaints': all_complaints,
        'total': total,
        'pending': pending,
        'resolved': resolved,
    }
    return render(request, 'complaints/warden_dashboard.html', context)

@login_required(login_url='login')
def update_status(request, pk, new_status):
    # Update: Let the warden quickly swap the status tag of a complaint
    if request.user.is_staff:
        complaint = get_object_or_404(Complaint, pk=pk)
        complaint.status = new_status
        complaint.save()
        return redirect('warden_dashboard')
    return redirect('dashboard')
def home_portal(request):
    # This view now always shows the choice landing page, even if you are logged in!
    return render(request, 'complaints/home_portal.html')
        
    # If they are not logged in, show them the choice landing page
    return render(request, 'complaints/home_portal.html')
@login_required(login_url='login')
def complaint_detail(request, pk):
    # Fetch the specific complaint
    if request.user.is_staff:
        # Wardens can view any student's complaint
        complaint = get_object_or_404(Complaint, pk=pk)
    else:
        # Students can only view their own private complaints
        complaint = get_object_or_404(Complaint, pk=pk, student=request.user)

    # Handle a new comment being submitted submitted
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            Comment.objects.create(
                complaint=complaint,
                author=request.user,
                text=comment_text
            )
            return redirect('complaint_detail', pk=complaint.pk)

    # Fetch all previous comments linked to this ticket
    comments = complaint.comments.all().order_by('created_at')
    
    return render(request, 'complaints/complaint_detail.html', {
        'complaint': complaint,
        'comments': comments
    })