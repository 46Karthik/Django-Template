from django.db import models
from django.contrib.auth.models import User as AuthUser

class Profile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name or self.user.username

class CRM(models.Model):
    crm_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='crm')
    is_active = models.BooleanField(default=True)
    Status = models.CharField(max_length=255, blank=True, null=True)
    # Lead Deals
    enquiry_id = models.CharField(max_length=100, blank=True, null=True)
    date_of_enquiry = models.DateField()
    lead_source = models.CharField(max_length=255, blank=True, null=True)
    travel_advisor = models.CharField(max_length=255, blank=True, null=True)
    domestic_intl = models.CharField(max_length=100, blank=True, null=True)
    enquiry_type = models.CharField(max_length=255, blank=True, null=True)

    # Customer Details
    customer_first_name = models.CharField(max_length=255)
    customer_last_name = models.CharField(max_length=255, blank=True, null=True)
    customer_location = models.CharField(max_length=255, blank=True, null=True)
    customer_role = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    # Trip Details
    trip_from = models.CharField(max_length=255)
    trip_to = models.CharField(max_length=255)
    pax = models.IntegerField(default=1)
    adult = models.IntegerField(default=1)
    kid = models.IntegerField(default=0)
    duration = models.CharField(max_length=255, blank=True, null=True)
    other_destinations = models.TextField(blank=True, null=True)
    flight_class = models.CharField(max_length=50, blank=True, null=True)
    flight_stopovers = models.CharField(max_length=255, blank=True, null=True)
    hotel_type = models.CharField(max_length=255, blank=True, null=True)
    room_sharing = models.CharField(max_length=255, blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Landing Cost
    flight_name = models.CharField(max_length=255, blank=True, null=True)
    flight_cost_per_person = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    flight_total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    hotel_cost_per_person = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    hotel_total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    land_package_name = models.CharField(max_length=255, blank=True, null=True)
    land_cost_per_person = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    land_total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Margin
    flight_margin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    flight_margin_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    hotel_margin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hotel_margin_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    land_margin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    land_margin_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Customer Selling Price
    selling_flight_cost_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_flight_total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_hotel_cost_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_hotel_total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_land_cost_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_land_total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Cost Details
    total_cost_per_person = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_landing_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_price_per_person = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_package = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    margin_for_package = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    margin_per_person = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Working Space
    working_space_notes = models.TextField(blank=True, null=True)
    itinerary_file_base64 = models.TextField(blank=True, null=True)  
    trip_name = models.CharField(max_length=255, blank=True, null=True)
    next_follow_up_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Enquiry {self.enquiry_id} - {self.customer_first_name} {self.customer_last_name}"
