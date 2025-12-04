from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.forms import formset_factory
from .models import Requisition, LineItem, ApprovalLog, UserProfile
from .forms import LineItemForm, ApprovalForm, SignUpForm


def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            UserProfile.objects.create(user=user, role=role)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'requisitions/signup.html', {'form': form})

@login_required
def dashboard(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    status_filter = request.GET.get('status', None)
    
    if user_profile and user_profile.role == 'MANAGER':
        requisitions = Requisition.objects.all()
        # Manager stats
        stats = {
            'total': requisitions.count(),
            'pending': requisitions.filter(status='PENDING').count(),
            'approved': requisitions.filter(status='APPROVED').count(),
            'rejected': requisitions.filter(status='REJECTED').count(),
        }
        # Apply filter if provided
        if status_filter and status_filter in ['PENDING', 'APPROVED', 'REJECTED']:
            requisitions = requisitions.filter(status=status_filter)
    else:
        requisitions = Requisition.objects.filter(requester=request.user)
        stats = None
    
    context = {
        'requisitions': requisitions,
        'user_profile': user_profile,
        'stats': stats,
        'current_filter': status_filter,
    }
    return render(request, 'requisitions/dashboard.html', context)

@login_required
def create_requisition(request):
    LineItemFormSet = formset_factory(LineItemForm, extra=1, min_num=1, validate_min=True)
    
    if request.method == 'POST':
        formset = LineItemFormSet(request.POST, request.FILES)
        if formset.is_valid():
            requisition = Requisition.objects.create(requester=request.user)
            for form in formset:
                if form.cleaned_data:
                    line_item = form.save(commit=False)
                    line_item.requisition = requisition
                    line_item.save()
            messages.success(request, 'Requisition created successfully!')
            return redirect('dashboard')
    else:
        formset = LineItemFormSet()
    
    return render(request, 'requisitions/create_requisition.html', {'formset': formset})

@login_required
def requisition_detail(request, pk):
    requisition = get_object_or_404(Requisition, pk=pk)
    user_profile = UserProfile.objects.filter(user=request.user).first()
    
    # Check access
    if user_profile and user_profile.role == 'MANAGER':
        can_approve = True
    elif requisition.requester == request.user:
        can_approve = False
    else:
        messages.error(request, 'You do not have permission to view this requisition.')
        return redirect('dashboard')
    
    context = {
        'requisition': requisition,
        'can_approve': can_approve,
        'user_profile': user_profile,
    }
    return render(request, 'requisitions/requisition_detail.html', context)

@login_required
def approve_requisition(request, pk):
    requisition = get_object_or_404(Requisition, pk=pk)
    user_profile = UserProfile.objects.filter(user=request.user).first()
    
    # Only managers can approve
    if not user_profile or user_profile.role != 'MANAGER':
        messages.error(request, 'Only managers can approve requisitions.')
        return redirect('dashboard')
    
    # Cannot approve own request
    if requisition.requester == request.user:
        messages.error(request, 'You cannot approve your own requisition.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ApprovalForm(request.POST)
        if form.is_valid():
            approval_log = form.save(commit=False)
            approval_log.requisition = requisition
            approval_log.manager = request.user
            approval_log.save()
            
            # Update requisition status
            requisition.status = approval_log.action
            requisition.save()
            
            messages.success(request, f'Requisition {approval_log.action.lower()} successfully!')
            return redirect('dashboard')
    else:
        form = ApprovalForm()
    
    context = {
        'requisition': requisition,
        'form': form,
    }
    return render(request, 'requisitions/approve_requisition.html', context)
