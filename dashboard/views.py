from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.http import Http404
from django.utils import timezone

from listings.models import Property
from messaging.models import Inquiry, Reservation, ContactMessage, InquiryMessage


def get_dashboard_context(user):
    """
    Helper function to get dashboard counter context for any user.
    Used across all dashboard views to ensure counters are consistent.
    
    Counter logic:
    - count inquiries where user is RECEIVER (to_user) and unread
    - count inquiries where user is SENDER (from_user) and unread (meaning other person replied)
    """
    # User's listings stats
    my_listings = Property.objects.filter(owner=user).exclude(status__in=['refused', 'deleted'])
    
    # Inquiries stats - count NEW UNREAD INQUIRIES (first message from someone)
    unread_inquiries = Inquiry.objects.filter(
        to_user=user,
        to_user_read=False
    ).count()
    
    # Messages stats - count UNREAD MESSAGES in existing conversations
    # Count messages sent TO you that you haven't read yet
    unread_messages = InquiryMessage.objects.filter(
        inquiry__in=Inquiry.objects.filter(Q(to_user=user) | Q(from_user=user))
    ).exclude(sender=user).filter(is_read=False)
    
    # Total count = new inquiries + new messages
    total_unread = unread_inquiries + unread_messages.count()
    
    # Total inquiries and messages stats
    total_messages = InquiryMessage.objects.filter(
        inquiry__in=Inquiry.objects.filter(Q(to_user=user) | Q(from_user=user))
    ).count()
    
    # Reservations stats
    pending_reservations = Reservation.objects.filter(to_user=user, status='pending')
    
    # Made reservations: include all except cancelled and soft-deleted
    # (User keeps seeing rejected until they manually delete)
    made_reservations = Reservation.objects.filter(
        from_user=user
    ).exclude(
        status='cancelled'
    ).exclude(
        deleted_for_guest_at__isnull=False
    )
    
    # Received reservations: exclude rejected and cancelled
    # (Owner doesn't see rejected after rejection)
    received_reservations = Reservation.objects.filter(
        to_user=user
    ).exclude(
        status__in=['rejected', 'cancelled']
    )
    
    return {
        'my_listings_count': my_listings.count(),
        'active_listings_count': my_listings.filter(status='active').count(),
        'pending_listings_count': my_listings.filter(status='pending').count(),
        'unread_inquiries_count': total_unread,
        'total_inquiries_count': Inquiry.objects.filter(Q(to_user=user) | Q(from_user=user)).count(),
        'total_messages_count': total_messages,
        'pending_reservations_count': pending_reservations.count(),
        'total_reservations_count': made_reservations.count() + received_reservations.count(),
        'made_reservations_count': made_reservations.count(),
        'total_received_reservations_count': received_reservations.count(),
    }


class DashboardOverviewView(LoginRequiredMixin, TemplateView):
    """
    User dashboard overview showing stats and recent activity.
    """
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Add counters using helper function
        context.update(get_dashboard_context(user))
        
        # User's listings stats
        my_listings = Property.objects.filter(owner=user).exclude(status__in=['refused', 'deleted'])
        
        # Recent activity
        context['recent_listings'] = my_listings.order_by('-created_at')[:5]
        context['recent_inquiries'] = Inquiry.objects.filter(to_user=user).order_by('-created_at')[:5]
        context['recent_reservations'] = Reservation.objects.filter(to_user=user).order_by('-created_at')[:5]
        
        # Tab indicator
        context['active_tab'] = self.request.GET.get('tab', 'overview')
        
        return context


class MyListingsView(LoginRequiredMixin, ListView):
    """
    Show user's property listings with edit/delete options.
    """
    template_name = 'dashboard/my_listings.html'
    context_object_name = 'listings'
    paginate_by = 12

    def get_base_queryset(self):
        """
        Base queryset of all listings for the current user.
        Excludes refused and deleted properties.
        Used both for stats and for filtered results.
        """
        return Property.objects.filter(owner=self.request.user).exclude(status__in=['refused', 'deleted']).order_by('-created_at')

    def get_queryset(self):
        """
        Apply optional status filter (?status=active|pending|reserved|sold|rented)
        on top of the base queryset.
        """
        queryset = self.get_base_queryset()
        status_filter = self.request.GET.get('status')
        if status_filter in ['active', 'pending', 'reserved', 'sold', 'rented']:
            queryset = queryset.filter(status=status_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_qs = self.get_base_queryset()
        
        # Add counters using helper function
        context.update(get_dashboard_context(self.request.user))

        context['active_tab'] = 'listings'
        context['status_stats'] = {
            'active': base_qs.filter(status='active').count(),
            'pending': base_qs.filter(status='pending').count(),
            'reserved': base_qs.filter(status='reserved').count(),
            'sold': base_qs.filter(status='sold').count(),
            'rented': base_qs.filter(status='rented').count(),
        }

        # Expose current status filter to the template for button highlighting
        context['current_status'] = self.request.GET.get('status', '')

        return context
