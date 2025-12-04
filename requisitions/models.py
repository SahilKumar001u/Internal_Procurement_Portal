from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('REQUESTER', 'Requester'),
        ('MANAGER', 'Manager'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='REQUESTER')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Requisition(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requisitions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"REQ-{self.id} by {self.requester.username}"

    class Meta:
        ordering = ['-created_at']

class LineItem(models.Model):
    CATEGORY_CHOICES = [
        ('OFFICE_SUPPLIES', 'Office Supplies'),
        ('ELECTRONICS', 'Electronics'),
        ('FURNITURE', 'Furniture'),
        ('SOFTWARE', 'Software'),
        ('OTHER', 'Other'),
    ]
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='line_items')
    item_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    purpose = models.TextField()
    def __str__(self):
        return f"{self.item_name} - {self.requisition}"

    @property
    def total_price(self):
        return self.quantity * self.unit_price

class ApprovalLog(models.Model):
    ACTION_CHOICES = [
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='approval_logs')
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    comments = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.manager.username} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
