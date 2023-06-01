# Looking for an expert in django (freelance or agencies welcome)

Here is a real life test I'm asking you to think about.
I'm using it to shortlist a django expert with whom I'd like to work with longer term.

As a deliverable, I would like to know :
- How much would you charge to code this project ?
- Short description of how you would handle the problem ? 
- Your hourly rate for future projects ?

# Project Description

On the django admin panel, I have a model (Company) that contains inlines (PricingPlan).

I have 2 groups of admin users : 
- superadmin (all access)
- vendor (limited access)

Each vendor is part of a model Vendor that has a unique list of VendorPricingPlans.

# Task 1

I would like to make the PricingPlan inline form dynamic based on : 

the user group (superadmin or vendor) and the Vendor object (if the user is part of group vendor)

A superadmin should see all 'product_name' PricingPlan choices (from mapping.py) for all companies

The vendor should see ONLY the 'product_name' of the PricingPlan attached to his Vendor (from the VendorPricingPlan object)

In the DB, the data saved should be keys of product so the view is the same for the admin and the vendor

# Task 2 

When a vendor is choosing a 'product_name' in the Company.PricingPlan admin inline, 
it should automatically update the 'fee' with the value 'suggest_fee' from the VendorPricingPlan DB.

# DB and base data

the DB is sqlite and is pushed with git for simple set up.

3 users were created : 

| username          | email             | passwd | role         |
|-------------------|-------------------|--------|--------------|
| admin             | admin@admin.com   | admin  | superadmin   |
| vendor            | vendor@vendor.com | vendor | vendor group |
| client@client.com | client@client.com | client | client       |


1 company was created :

| name         | user              | vendor            |
|--------------|-------------------|-------------------|
| demo company | client@client.com | vendor@vendor.com |

group vendor was created and add vendor user to group vendor