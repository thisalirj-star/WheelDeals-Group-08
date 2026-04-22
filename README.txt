=====================================
   WHEELDEALS - GROUP 08
   Car Bidding Web Application
=====================================

PROJECT OVERVIEW
-----------------
WheelDeals is a web-based car selling platform built on a bidding system.
Buyers can browse, search and bid on vehicles listed by verified sellers.

TECH STACK
-----------
- Backend  : Django 6.0.3 (Python)
- Frontend : HTML, CSS, Bootstrap 5
- Database : SQLite3
- Version Control : Git & GitHub

TEAM MEMBERS & RESPONSIBILITIES
---------------------------------
1. Dinali   - Home Page, Search & Filters, Summary Cards
2. Amashi   - Login, Register, Add Car Form
3. Sithmi   - Car Details Page, Seller Dashboard
4. Thisali  - Bidding System, Project Merging & Testing

=====================================
   HOME PAGE (Dinali - Member 4)
=====================================

PAGES HANDLED
--------------
- Home Page (main landing page)

FEATURES IMPLEMENTED
---------------------
- Hero section with background image and animated text
- Search bar to search vehicles by brand, model or year
- Filter sidebar (Brand, Vehicle Type, Year, Max Price)
- Car listings grid showing:
    * Vehicle image
    * Title
    * Starting price (LKR)
    * Year
    * Mileage
- Summary cards (Total Cars, Active Auctions, Sellers, Cars Sold)
- Responsive navbar with WheelDeals logo
- Footer with contact details and background image
- Scroll position preserved when applying filters
- Count up animation on summary cards
- Hero text slide-in animation
- Base template (base.html) shared with all teammates

APP FOLDER
-----------
home/

HOW TO SET UP AND RUN THE PROJECT
-----------------------------------
1. Clone the repository:
   git clone https://github.com/thisalirj-star/WheelDeals-Group-08.git
   cd WheelDeals-Group-08

2. Switch to your branch:
   git checkout Homepage

3. Create and activate virtual environment:
   python -m venv venv
   source venv/Scripts/activate  (Windows)
   source venv/bin/activate      (Mac/Linux)

4. Install dependencies:
   pip install -r requirements.txt

5. Run migrations:
   python manage.py migrate

6. Run the server:
   python manage.py runserver

7. Open browser:
   http://127.0.0.1:8000/

GITHUB REPOSITORY
------------------
https://github.com/thisalirj-star/WheelDeals-Group-08.git

=====================================