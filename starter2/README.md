

--Introduction

Zapoo is a simple business directory that allows the user to submit a listing for SEO purposes. What makes this website different from the other business directories out there is its DIY features. The user is able to stylize their content by selecting a variety of CSS/Javascript features to make their business listing stand out when a customer visits the listing page. Most business directories usually have one layout that they use for all business listings, and Zapoo aims to be creative and unique with their business listing pages. Since this is a capstone project, there will be a select amount of features that will be added, with some new designs later down the road.

---How to Install

----Backend

----Frontend

---Backend Documentation
I'll be using the following dependencies/frameworks for this project:

-Flask (Backend development)
-Flask Email (for email handling)
-SQLAlchemy (for ORM and database manipulation)
-Google ReCaptcha (I completely hate this)
-bleach (HTML Sanitizer)
-bcrypt (encryption)
-unittest (testing API and functions)

---Controllers

Endpoint: '/'
Method: GET
Parameters: None
Returns: JSON with a "Hello world" message.
Description: This is a default endpoint. It should only be used to test the responsiveness of the website's API.

Endpoint: '/getCategories'
Method: GET
Parameters: None
Returns: JSON with the category name.
Description: Category page. It gets the category names.

Endpoint: '/<string:category_name>/listings'
Method: POST
Parameters: Category name
Returns: JSON with a list of Listing names that match the category.
Description: Search Page. returns a list of listings that match the category.

Endpoint: '/categories/<string:category_name>/listings/<string:listing_id>'
Method: GET
Parameters: Listing ID
Returns: JSON with Business Page, Address, Hours, Email, Website, Phone, Payment Methods, keywords, and description.
Description: Listing page. displays everything about the listing except state, city, category, layout id, style id, time of creation.

Endpoint: '/getEditListing'
Method: GET
Parameters: Edit
Returns: JSON with all listing information.
Description: Submit Listing Page. Used to fill in the form if the user wants to edit their listing.

Endpoint: '/getCatOfListings'
Method: GET
Parameters: CategoryName
Returns: JSON with a list of Listing names that are associated with the category.
Description: Search Page. Similar to "getRecentListings" endpoint.

Endpoint: '/getHomeListings'
Method: GET
Parameters: None
Returns: JSON with Business name, Short Description (approx. 20 characters), State, City, Time of Creation
Description: Search Page. Similar to "getRecentListings" endpoint.

Endpoint: '/search'
Method: POST
Parameters: Search Term String.
Returns: JSON with a list of Listing names.
Description: Navbar Search. returns a list of matching listing names that the search term matched against.

Endpoint: '/searchListing'
Method: POST
Parameters: Keyword, State, City
Returns: JSON with a list of Listing names.
Description: Search Page. returns a list of matching listing names that the search parameters matched against.

Endpoint: '/signup'
Method: POST
Parameters: None
Returns: None
Description: Using Flask Email, this endpoint sends an email to the corresponding email address and redirect the user to the email confirmation sent page.

Endpoint: '/signin'
Method: POST
Parameters: None
Returns: Success/failure on sign in.
Description: Allows the end user to sign in and manage their account.

Endpoint: '/submitlisting'
Method: POST
Parameters: None
Returns: Success/failure on submission.
Description: Adds a listing to the database. On success, the end user will be redirected to the listing page.

Endpoint: '/SetFTPassword'
Method: POST
Parameters: verification token
Returns: Success/failure on setting a password.
Description: First time password set up. If successful, the user will be redirected to their account page.

Endpoint: '/changePassword'
Method: UPDATE
Parameters: None
Returns: Success/failure on changing password.
Description: Allows the end user to change their password. They will receive a notification when they successfully changed it and an email.

Endpoint: '/categories/<string:category_name>/listings/<string:listing_id>'
Method: DELETE
Parameters: None
Returns: Success/failure on deletion.
Description: Allows the end user to change their password. They will receive a notification when they successfully changed it and an email.

----Models

Listing

Carries all information about the company listing.

-ID --> The ID of the listing. Unique Integer

-BUSINESSNAME --> The business name. Unique Varchar Length 100

-ADDRESS --> The physical address. Varchar Length 150

-STATE --> The state in the United States. Varchar Length 4

-CITY --> The city in the United States. Varchar Length 50

-HOURS --> Hours of the business in Text. Varchar Length 300

-PAYMENT_TYPE --> Credit Card, Debit Card, Cash, Check. Varchar Length 100

-WEBSITE_LINK --> The website URL. Varchar Length 300

-PHONE --> The phone number formatted in 0123456789. Varchar length 10

-CATEGORIES --> The type of business. Foreign Key of Categories.

-KEYWORDS --> They keywords to search for a particular business in the directory (up to 5 keywords). Varchar length 100

-BUSINESS_EMAIL --> The email address of the business. Varchar 100

-DESCRIPTION --> The description of the business. Varchar 1000

-TIME_OF_CREATION --> The date of when the listing was created. DateTime (format: yyyy-mm-dd hh:mm:ss)

-LAYOUTID --> The page layout. Integer

-STYLEID --> The page coloring. Integer


User

The registered user on Zapoo.

-ID --> The user id. Unique Integer

-USER_EMAIL --> The user's email to login. Varchar Length 140

-PASSWORD --> The user's password after hashing. Should be at least 8 characters in length. Varchar

-IS_ACTIVE --> Ensures that the user did confirm the email before they are able to add a listing, and if the user wishes to remain active on the website. Boolean.

-LISTING_ID --> The listing that the user created. Foreign Key Integer of Listing.

Categories

Separates and organizes business listings based on what they do.

-ID --> The category ID. Unique Integer

-CATEGORY_NAME --> The category name. Varchar 50

Email Confirmation Links

Ensures user verification and identity upon registration.
-ID --> The ECL ID (as a way to keep count).

-USER --> The User ID. Foreign Key of User ID.

-CODE --> The code needed to confirm verification when the user clicks on the email link. Unique Varchar 200

-IS_CONFIRMED --> A boolean value to confirm if the user has activated their account. Boolean



---Frontend Documentation
I will use the following extensions/frameworks to develop the frontend:
-JQuery

-CSS

-JavaScript

-Bootstrap

-flexbox

----SiteMap

-----Home
Endpoints: '/search'
Description: The homepage of the website. This should be the very first thing the end user sees.
Links to: Sign in/Account page, Categories, Contact, About, Three most recent listings

-----Search
Endpoints: '/search'
Description: The search page to look up listings. The end user can specify keywords, state, and/or city to query.
Links to: individual listing pages, Sign in/Account page, Categories, Contact, About, Home

-----Signinup
Endpoints: '/search'
Description: The Sign in/Sign up page for registering new users or logging in as an existing user.
Links to: Home, Categories, Contact, About, EmailSentSuccess Page (sign up form submission)

-----Contact
Endpoints: '/search'
Description: The contact page if an end user needs to contact someone.
Links to: Home, Sign in/Sign up, Categories, About

-----About
Endpoints: '/search'
Description: The about page on who we are.
Links to: Home, Sign in/Sign up, Categories, Contact

-----Categories
Endpoints: '/search'
Description: The categories page where the user can choose a category and find category-specific listings on the search page.
Links to: Home, Sign in/Sign up, Contact, About, individual category links.

-----Account
Endpoints: '/search'
Description: The account page where the user can view, edit, or delete a listing, or change their password.
Links to: Home, submit a listing, categories, Contact, About, user listing page

-----Listing Page
Endpoints: '/search'
Description: The listing page.
Links to: Home, Sign in/up, categories, Contact, About, external link to business website if applicable.

-----Submit Listing Page
Endpoints: '/search'
Description: The listing page.
Links to: Home, Sign in/up, categories, Contact, About, external link to business website if applicable.

-----Email Confirmation Sent Page
Endpoints: '/search'
Description: The Email Confirmation Sent Page. This page is displayed when the end user successfully signs up after they entered in their email.
Links to: Home, Sign in/up, categories, Contact, About

-----New Password Page
Endpoints: '/search'
Description: New Password Page after they verified their account through their email.
Links to: Home, Sign in/up, categories, Contact, About

--Thanks
Udacity for teaching me a lot of things about full stack web development.
Myself for being a blessed prestidigitator.
