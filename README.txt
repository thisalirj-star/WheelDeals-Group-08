```markdown
# WheelDeals - Car Bidding Platform

## 👥 Team Members & Contributions

| Member | Registration No | Responsibility |
|--------|----------------|----------------|
| Thisali Jayasundara | 236055B | Bidding System & Auction Management |
| S. S. Ranathunga | 236108R | Seller Dashboard, Buyer Dashboard & Car Detail Pages |
| Dinali Ranasinghe | 236107M | Base Template & Homepage |
| G. G. A. Adithya | 236005A | Authentication, Car Management & Bidding Integration |

**Repository:** https://github.com/thisalirj-star/WheelDeals-Group-08.git

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Backend | Django 6.0.4, Django ORM, SQLite |
| Frontend | Bootstrap 5.3, Bootstrap Icons, Chart.js, Vanilla JS |
| Version Control | Git, GitHub |

---

## 📁 Project Structure

```
wheeldeals/
├── accounts/          # User authentication
├── bidding/           # Bidding system & auction management
├── cars/              # Car listings & dashboards
├── home/              # Homepage
├── static/images/     # Logo, hero, footer images
├── templates/
│   ├── base.html
│   ├── accounts/      # login, register pages
│   ├── cars/          # add_car, dashboard, detail pages
│   └── home/home.html
└── wheeldeals/        # Project settings
```

---

## 🗄️ Database Models

| Model | App | Key Fields |
|-------|-----|------------|
| User | accounts | user_type (buyer/seller), company_name, phone |
| Car | cars | title, brand, model, year, mileage, starting_price, seller, is_sold, view_count |
| CarImage | cars | car, image, is_primary |
| Auction | bidding | car, end_time, status (ACTIVE/PAUSED/ENDED) |
| Bid | bidding | auction, buyer, amount, created_at |

---

## 👤 Thisali Jayasundara (236055B) — `biddingpage` branch

**Responsibility:** Bidding System & Auction Management

### Files

| File | Location |
|------|----------|
| apps.py | bidding/apps.py |
| models.py | bidding/models.py |
| views.py | bidding/views.py |
| urls.py | bidding/urls.py |
| buyer_bidding.html | templates/bidding/buyer_bidding.html |
| seller_bidding.html | templates/bidding/seller_bidding.html |

### What I Built

**models.py — Auction & Bid data structures**
- Auction model with duration choices (6h, 12h, 24h, 72h), status tracking (Active/Paused/Ended), and auto-generated end_time
- Bid model with ForeignKey to Auction and User, ordered by highest amount first
- save() override to automatically calculate end_time based on selected duration

**views.py — Complete bidding logic for buyers and sellers**

*Buyer Features:*
- buyer_bidding_page — Live auction view with countdown timer and bid history
- place_bid — Place new bid with validation (must exceed current highest bid)
- delete_bid — Remove your own bid from an active auction

*Seller Features:*
- seller_bidding_page — Dashboard showing auction status, bids, and profit calculation
- pause_auction / resume_auction — Temporarily freeze or restart bidding
- accept_highest_bid — End auction, mark car as sold, and associate with winning buyer
- extend_bidding_time — Add 3, 6, or 24 hours to active auction
- delete_auction — Permanently remove auction and all associated bids
- remove_bid_seller — Remove any bid from the auction (moderation)
- create_auction — Auto-create auction when seller lists a car

**urls.py — Route mapping**

| URL Pattern | View | Purpose |
|-------------|------|---------|
| /buyer/<auction_id>/ | buyer_bidding_page | Buyer live auction view |
| /buyer/place/<auction_id>/ | place_bid | Submit new bid |
| /buyer/delete/<bid_id>/ | delete_bid | Remove own bid |
| /seller/<id>/ | seller_bidding_page | Seller auction dashboard |
| /seller/pause/<id>/ | pause_auction | Pause active auction |
| /seller/resume/<id>/ | resume_auction | Resume paused auction |
| /seller/remove/<bid_id>/ | remove_bid_seller | Remove any bid |
| /seller/accept/<id>/ | accept_highest_bid | End auction & sell car |
| /seller/extend/<id>/ | extend_bidding_time | Add time to auction |
| /seller/delete/<id>/ | delete_auction | Delete auction |
| /create/<car_id>/ | create_auction | Auto-create auction |

**buyer_bidding.html — Buyer auction interface**
- Real-time countdown timer showing remaining auction time
- Current highest bid display with minimum next bid calculation
- One-click bid amount presets (+10k, +50k, +100k LKR)
- Live bid history feed with timestamps
- "Highest Bidder" popup notification when user takes the lead (shows only once per bid amount)
- Full car details with image carousel and spec grid
- Lightbox for image zoom
- Login modal for unauthenticated users
- Visual highlighting of user's own bids

**seller_bidding.html — Seller management dashboard**
- Auction status badge (Active/Paused) with color coding
- Pause/Resume controls for active auctions
- Extend bidding time buttons (3h, 6h, 24h) with login modal for unauthenticated
- Accept highest bid to finalize sale and mark car as sold
- Delete auction with confirmation modal (warning about permanent action)
- Post-auction completion card showing:
  - Accepted bid amount
  - Starting price comparison
  - Profit calculation
  - Winning buyer username
  - Total bids received
  - Auction duration display
- Full bid history ordered from highest to lowest
- Car details with thumbnail image gallery and specs

### Key Features

**Smart Bidding Validation**
- Bids automatically rejected if below current highest bid
- Sellers cannot bid on their own auctions
- Minimum next bid = current highest + LKR 10,000

**Auction State Management**
- Active → Paused → Ended lifecycle
- Paused auctions freeze countdown and block new bids
- Resumed auctions continue with original remaining time

**Sale Completion Flow**
- Accepting highest bid:
  - Deletes all lower bids
  - Marks car as sold with buyer and price
  - Deactivates car listing
  - Ends auction

**Security**
- All seller actions verify ownership (request.user == auction.car.seller)
- Bid deletion restricted to bid owner or seller
- Login required for placing bids and seller actions

**UI Polish**
- Glassmorphism card design with neon blue accents
- Responsive grid layout for car details and bidding panels
- Shimmer and glow effects on important elements
- Smooth popup animations for notifications

---

## 👤 S. S. Ranathunga (236108R) — `SellerDashboardPage` branch

**Responsibility:** Seller Dashboard, Buyer Dashboard & Car Detail Pages

### Files

| File | Location |
|------|----------|
| dashboard.html | cars/templates/cars/dashboard.html |
| buyer_dashboard.html | cars/templates/cars/buyer_dashboard.html |
| car_detail_seller.html | cars/templates/cars/car_detail_seller.html |
| car_detail_buyer.html | cars/templates/cars/car_detail_buyer.html |
| views.py | cars/views.py |
| urls.py | cars/urls.py |
| models.py | cars/models.py |

### What I Built

**dashboard.html — Seller Analytics Dashboard**

*KPI Metrics Cards*
- Total Listings counter with blue gradient accent
- Cars Sold count with green status indicator
- Total Revenue (LKR) with gold color scheme
- Average Listing Price with red accent
- Each card features hover animation and custom icon styling

*Chart Visualizations (Chart.js)*
- Sales trend line chart showing monthly car sales over 6 months
- Custom gradient fill with smooth curve (tension: 0.4)
- Inventory status doughnut chart (Available vs Sold)
- Dark-themed charts matching platform color scheme

*Most Viewed Listings Section*
- Top 3 most popular cars with rank indicators (#1, #2, #3)
- View count with eye icon
- Dynamic progress bars scaled to highest view count

*Complete Car Listings Table*
- Displays all seller's cars with thumbnails, prices, and status badges
- Visual status indicators (Available / Sold) with colored dots
- Live auction countdown timers for active listings
- Action buttons: View, Auction, Edit, Delete
- Responsive table with hover effects

*Performance Optimizations*
- Aggregated database queries using Count, Sum, Avg
- Sales data calculated per month using relativedelta
- View count tracking integrated into listing display

**buyer_dashboard.html — Buyer Bidding Dashboard**

*KPI Metrics Cards*
- Total Bids Placed across all auctions
- Currently Winning count (green success indicator)
- Outbid notifications (red alert indicator)
- Highest Bid amount (gold accent)

*Active Bids Section*
- Grid layout of cards showing all active bids
- Each card displays: car image, brand/model, bid amount
- Real-time status badges: Winning (green) / Outbid (red)
- Current highest bid comparison
- Live countdown timer for remaining auction time
- Clickable cards linking to auction page

*Past Bids Section*
- Historical bids from ended auctions
- Grayscale image filter for visual distinction
- Ended status badge with muted styling
- Bid date display with calendar icon

*Empty State Handling*
- Friendly "No Active Bids" message with Browse Cars CTA
- Clean UI for users with no bidding history

**car_detail_seller.html — Seller View of Listing**

*Quick Stats Bar*
- Status indicator (Active / Sold)
- Visual stat cards with icons

*Image Gallery*
- Primary image display with thumbnail strip
- Multiple image upload support
- Image switching via thumbnail click

*Car Information Panel*
- Complete specifications grid (Brand, Vehicle Type, Fuel, Condition, Year, Mileage)
- Starting price display with gold styling
- Availability badge with status dot
- Location information with map icon

*Auction Management Section*
- First active auction displayed with status badge
- Highest bid amount with gold highlight
- Total bids count
- Live pulse animation for active auctions

*Action Buttons*
- Edit Listing button (gradient blue)
- Delete Listing button (red outline) with confirmation modal
- Custom modal with warning styling for delete confirmation

*Description Section*
- Full car description below image gallery
- Empty state message when no description exists

**car_detail_buyer.html — Buyer View of Listing**

*Image Panel*
- Main car image with thumbnail gallery
- Image metadata pills (Year, Mileage, Fuel, Location)
- Meta-pill styling with Bootstrap Icons

*Vehicle Information*
- Car title with brand/model (Rajdhani font)
- Condition badge with checkmark icon
- Starting price prominently displayed
- Complete specifications grid with empty state handling

*Auction Timer Card*
- Live countdown timer in hours, minutes, seconds
- End time display with calendar icon
- Timer turns red when under 10 minutes remaining
- JavaScript interval updates every second

*Bid Action Section*
- "Place a Bid" button with hammer icon
- Disabled state for:
  - User's own listings (You own this listing)
  - Cars with no active auction
- Gradient button styling with hover effect

*Seller Information Card*
- Seller username with avatar icon
- Company name (if provided by seller)
- Phone number with telephone icon
- Location display
- Clean information layout for buyer confidence

*Description Panel*
- Full car description positioned below image
- Consistent styling with seller view

*View Count Tracking*
- Automatically increments when buyer views page
- Used for "Most Viewed" analytics in seller dashboard

---

## 👤 Dinali Ranasinghe (236107M) — `homepage` branch

**Responsibility:** Base Template & Homepage

### Files

| File | Location |
|------|----------|
| base.html | templates/base.html |
| home.html | templates/home/home.html |
| views.py | home/views.py |
| urls.py | home/urls.py |

### What I Built

**1. base.html — Shared Base Template**

The foundation layout used by all pages across the WheelDeals application. Every other template extends this file.

*Features:*
- Sticky navigation bar with a shimmer animation effect, built using Bootstrap 5
- Dynamic navbar that changes based on user authentication state:
  - Shows a personalised "Welcome back, username!" greeting for logged-in users
  - Displays Login button for unauthenticated visitors
  - Shows Dashboard (Seller or Buyer) and Logout buttons for authenticated users
  - Automatically routes sellers to seller_dashboard and buyers to their own dashboard
- Responsive hamburger menu for mobile screens
- A branded footer with background image overlay, office contact details (Head Office — Colombo, Kandy Branch), and email
- Bootstrap Icons integrated throughout the UI
- Block placeholders: title, extra_css, content, extra_js — allowing child templates to inject page-specific content and styles

**2. home.html — Homepage**

The main landing page of WheelDeals, extending base.html.

*Features:*
- **Hero Section** — Full-width background image with gradient overlay, animated headline ("The Ultimate Car Bidding Experience") with a slide-in-left CSS animation, and a tagline
- **Summary Stats Section** — Four animated counter cards showing live data:
  - Total Cars Listed
  - Active Auctions
  - Registered Sellers
  - Cars Sold
  - Numbers count up on scroll using an Intersection Observer
- **Filter Sidebar** — Left-side panel with:
  - Brand filter (Toyota, Honda, BMW, Mercedes, Nissan, Ford, Audi)
  - Vehicle Type filter (Sedan, SUV, Hatchback, Coupe, Truck, Van, Convertible, Wagon)
  - Year filter (2000–2026)
  - Max Price slider with real-time LKR display (formats into Millions/Billions)
  - Apply Filters and Clear Filters buttons
- **Car Listings Grid** — Right-side 3-column grid of car cards, each showing:
  - Car image (or placeholder if none uploaded)
  - Vehicle type badge, brand & model, starting price in LKR, year, and mileage
  - Clickable card that navigates to the car detail page
  - Empty state message if no vehicles match the filters
- **Search Bar** — Inline search by car title, brand, or model, integrated above the listings grid
- **Scroll Position Preservation** — Saves and restores scroll position after filter/search form submissions using sessionStorage, so the user stays near the listings section

**3. views.py — Homepage View Logic**
- Handles GET parameters for search (search), brand, vehicle_type, year, and max_price
- Queries the Car model (from the cars app) for active, unsold listings
- Applies all filters dynamically and orders results by newest first
- Calculates summary stats: total cars, active auctions, distinct sellers, and cars sold
- Falls back gracefully to an empty state if the cars app is not yet merged

**4. urls.py — URL Configuration**
- Maps the root URL (/) to the home view with the name 'home'

---

## 👤 G. G. A. Adithya (236005A) — `login` branch

**Responsibility:** Authentication, Car Management & Bidding Integration

### What I Built

**1. accounts/models.py — Custom User Model**

Extended Django's built-in AbstractUser to support buyer and seller roles.

*Features:*
- user_type field (buyer or seller) to distinguish between user roles
- company_name field for sellers (optional)
- phone, address, and profile_picture fields for all users
- Helper methods is_seller() and is_buyer() used across the app for role-based access control
- Set as the global AUTH_USER_MODEL in settings.py so all apps reference this model

**2. cars/models.py — Car & CarImage Models**

Defines the core data structure for car listings and their images.

*Car Model Fields:*
- title, description, brand, model, year, mileage
- vehicle_type, fuel_type, condition
- starting_price, sold_price
- location, image (legacy single image field)
- seller (ForeignKey to User), sold_to (ForeignKey to User)
- auction_end_time, is_sold, is_active
- created_at, updated_at timestamps

*CarImage Model:*
- Supports up to 5 images per car listing
- is_primary flag to mark the main display image
- Linked to Car via ForeignKey with related_name='images'

**3. Authentication Pages**

*Login Page (templates/accounts/login.html)*
- Split layout — benefits panel on the left, login card on the right
- Animated gradient bar at the top of the login card
- Password visibility toggle (eye icon)
- Error message display with 4-second auto-dismiss
- Auto-dismiss on typing in username or password field
- Stats strip (Cars Listed, Happy Users, Satisfaction Rate) centered with dividers
- Benefit cards with hover slide animation
- After login: sellers redirect to Seller Dashboard, buyers redirect to Home

*Register Selection Page (templates/accounts/register_select.html)*
- Two cards — Buyer and Seller — with hover lift animation
- Links to respective registration forms

*Buyer Registration Page (templates/accounts/register_buyer.html)*
- Full registration form with username, email, password, phone, address, profile picture
- Real-time password requirements checker:
  - Minimum 8 characters
  - At least one letter
  - At least one number
  - Not a commonly used password
  - Each requirement shows a green tick when met
- Password visibility toggle on both password and confirm password fields

*Seller Registration Page (templates/accounts/register_seller.html)*
- Same as buyer registration with additional optional company name field
- Password requirements checker and visibility toggles
- Company name clearly marked as optional

**4. Car Management Pages**

*Add Car Form (templates/cars/add_car.html)*
- Multi-section form layout:
  - Basic Information (title, brand, model, year)
  - Vehicle Details (type, fuel, condition, mileage, location, description)
  - Pricing & Auction (starting price, auction end time)
  - Car Images (up to 5 images)
- Live image preview before upload with "Main" badge on first image
- Automatic Auction object creation if auction end time is provided
- First uploaded image also saved to car.image for backward compatibility

*Edit Car Page*
- Pre-filled form with all existing car data
- Image replacement support — replaces all existing images on new upload
- Automatically creates an Auction if an auction end time is added to an existing listing that had none

*Delete Car (Confirmation Page)*
- Confirmation card before permanent deletion
- POST-based deletion to prevent accidental removal

---

## 🎨 Design System

| Color | Usage |
|-------|-------|
| #0a1628 / #0d1f3c | Backgrounds |
| #1a6fc4 / #00c6ff | Accents, buttons |
| #f5a623 | Prices, revenue |
| #22c55e | Winning, success |
| #ef4444 | Outbid, errors |

**Fonts:** Rajdhani (headings), DM Sans (body)

---

## 🚀 Quick Setup

```bash
git clone https://github.com/thisalirj-star/WheelDeals-Group-08.git
cd wheeldeals
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Access:** http://127.0.0.1:8000/

---

## 🔗 Key URLs

| Page | URL |
|------|-----|
| Home | / |
| Login | /accounts/login/ |
| Seller Dashboard | /cars/dashboard/ |
| Buyer Dashboard | /cars/buyer-dashboard/ |
| Add Car | /cars/add/ |
| Admin | /admin/ |

---

## 🌿 Branch Structure

| Branch | Description |
|--------|-------------|
| login | Base branch for login/logout, registration, and add car pages — built by 236005A |
| homepage | Base branch for the homepage and base template — built by 236107M |
| SellerDashboardPage | Base branch for the seller dashboard page — built by 236108R |
| Biddingpage | Base branch for the buyer and seller bidding pages — built by 236055B |
| TestMerge-Dashboard | Duplicate of seller dashboard, prepared for merging with the login branch |
| merge-test | Merge of the login and seller dashboard branches |
| login-dashboard-merge | Duplicate of merge-test, prepared for merging with the homepage branch |
| homepage-test | Merge of the login, seller dashboard, and homepage branches |
| login-dash-home-merge | Duplicate of homepage-test, prepared for merging with the bidding branch |
| bidding-test | Duplicate of Biddingpage, prepared for merging with homepage-test |
| login-dash-home-bid | Full merge of login, seller dashboard, homepage, and bidding branches |
| final_editings_draft1 | Duplicate of login-dash-home-bid — used for UI refinements and adding the buyer dashboard |
| final_editings_draft2 | Final edits and polish before submission |

**Note:** Base branches contain the original work by each member. Duplicate branches were created to safely merge features without affecting the original work.

---
