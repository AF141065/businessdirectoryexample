// search index for WYSIWYG Web Builder
var database_length = 0;

function SearchPage(url, title, keywords, description)
{
   this.url = url;
   this.title = title;
   this.keywords = keywords;
   this.description = description;
   return this;
}

function SearchDatabase()
{
   database_length = 0;
   this[database_length++] = new SearchPage("Home.html", "Zapoo! | The World's Most Creative Business Directory!", "A capstone project by Adam Dural  Here on Zapoo, we encourage YOU to add every single of your business locations here  What are you waiting for? Click the button below to go to our sign up page and get started!   ", "Zapoo is a business directory!");
   this[database_length++] = new SearchPage("Search.html", "Zapoo | Search", "A capstone project by Adam Dural   ", "");
   this[database_length++] = new SearchPage("Signinup.html", "Zapoo | Sign Up/In", "Email  Password  A capstone project by Adam Dural   ", "");
   this[database_length++] = new SearchPage("Contact.html", "Zapoo | Contact", " Name   Adam Fraser         Title   CEO         Phone Number   555-555-5555        A capstone project by Adam Dural   ", "");
   this[database_length++] = new SearchPage("About.html", "Zapoo | About", "Zapoo is a simple business directory that allows the user to submit a listing for SEO purposes What makes this website different from the other business directories out there is its DIY features The user is able to stylize their content by selecting a variety of CSS/Javascript features to make their business listing stand out when a customer visits the listing page Most business directories usually have one layout that they use for all business listings, and Zapoo aims to be creative and unique with their business listing pages  A capstone project by Adam Dural   ", "");
   this[database_length++] = new SearchPage("CategoryPage.html", "Untitled Page", "                                                                                          A capstone project by Adam Dural   ", "");
   this[database_length++] = new SearchPage("Account.html", "Zapoo | Your Account", "A capstone project by Adam Dural  Email   email here  Listing   listing link here  Edit Listing  Delete Listing  Are you sure you want to delete your listing? Everything saved will be lost!   ", "");
   this[database_length++] = new SearchPage("ListingPage.html", "Zapoo | LISTING HERE", "A capstone project by Adam Dural                               Address  Hours  Email  Website  Phone          Desc here  Payment Methods         ", "");
   this[database_length++] = new SearchPage("SubmitListingPage.html", "Zapoo | Submit Listing", "A capstone project by Adam Dural   ", "");
   this[database_length++] = new SearchPage("emailconfirmsuccess.html", "Zapoo | Email Sent!", "A capstone project by Adam Dural  Confirmation email has been sent Please check your inbox   ", "");
   this[database_length++] = new SearchPage("NewPasswordPage.html", "Zapoo | Enter New Password", " ", "");
   return this;
}
