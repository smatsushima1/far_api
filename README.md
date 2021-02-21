# Federal Acquisition Regulation API

## 1.0 - Overview
This project will attempt to convert the FAR into separate database entries, each ontaining HTML text for each of its' respective sections. This way, regulation information can be pulled whenever required, centrally stored in one secure location, and updated securely as a result.

## 2.0 - Possibilities
The main reason I wanted to create an API for the FAR was to implement a web app that will allow users to search for any number of regulations simultaneously. Acquisition professional must do this everyday anyway, and the way the regulations are currently established online, only one regulation can be viewed at a same time. People have been doing this for years, so I guess this isn't too big of a problem, but there is room for at least some improvement.

Having an API for the FAR will allow the web app to automatically detect when a selected reference from the FAR is available in another reference. Viewing regulations side-by-side can greatly help with the day-to-day searching and reading since all verbiage pertaining to the users' desired subject can now be had quicker in one tab, instead of having to find it in multiple tabs.

In theory, if the FAR were stored in a database and referenced at ease, the system will be able to tell if a supplemental regulation further implements the FAR. Even if it doesn't apply, at least the API will allow the user to view the text (HTML) conveniently in front of them regardless. Utilizing proper hyperlinks will allow for faster and easier browsing (see problem [below](#3.3.hyperlinks-with-arbitrary-names)) as well as faster, easier, and more accurate analyzing of the regulations.

## 3.0 - Problems With the Current System
In addition to creating a web app, the current regulations posted on
[acquisition.gov](acquisition.gov) have several problems.

### 3.1 - Paragraphs and Lists
The HTML structure of the FAR is not consistent among each regulation. Here is a table of how each regulation indents their paragraphs:

|REGULATION|STYLE|
|---|---|
|FAR|`<span class="ph autonumber">`|
|DFARS|`<p class= "p List1">`<br>`<p class="p List3.>`<br>...|
|DFARS PGI|`<p class="p List1">`<br>`<p class="p List3.>`<br>...|
|AFFARS|`<p align="left" style="margin-left: 0.3in"...>`|
|DARS|`<p style="margin-left: 0.57in">`<br>`<p style="margin-left: 0.89in">`<br>...|
|DLAD|`<p style="margin-left: 0.3.in;">`<br>`<p style="margin-left: 0.50in;">`<br>...|
|NMCARS|`<p class="p List1">`<br>`<p class="p List3.>`<br>...|"
|SOFARS|Uses a combination of `<li>` and `<p>`|
|TRANSFARS|Just uses `<p>`, no indentations|
|AGAR|Just uses `<p>`, no indentations|
|AIDAR|Just uses `<p>`, no indentations|
|CAR|Just uses `<p>`, no indentations|
|DEAR|Just uses `<p>`, headings use `<li>`|
|DIAR|`<p class="p List1">`<br>`<p class="p List3.>`<br>...|
|DOLAR|Just uses `<p>`, no indentations|
|DOSAR|Just uses `<p>`, no indentations|
|DTAR|Just uses `<p>`, no indentations|
|EDAR|Just uses `<p>`, no indentations|
|EPAAR|`<p class="p List1">`<br>`<p class="p List3.>`<br>...|
|FEHBAR|Just uses `<p>`, no indentations|
|GSAM/R|`<span class="ph autonumber">`|
|HHSAR|Just uses `<p>`, no indentations|
|HSAR|`<p class="p List1">`<br>`<p class="p List3.>`<br>...|
|HUDAR|`<p class="p List1">`<br>`<p class="p List3.>`<br>...|
|IAAR|Just uses `<p>`, no indentations|
|JAR|Just uses `<p>`, no indentations|
|LIFAR|Just uses `<p>`, no indentations|
|NFS|Just uses `<p>`, no indentations|
|NRCAR|Just uses `<p>`, no indentations|
|TAR|Just uses `<p>`, no indentations|
|VAAR|`<p class="indenta">`<br>`<p class="indenti">`<br>`<p class="indent1">`<br>...|

As you can see, the vast majority of the regulations don't even have indents. Those that do never have their text line up with the indent itself and end up trail well past the indentation, which defeats the purpose of showing a list.

If all the regulation had the same formatting and structure, perusing their contents will easier and more efficient. The current version of the FAR isn't unreadable, but it could use some improvements.

### 3.3.- Hyperlinks with Arbitrary Names
Scoring through the HTML code, you can find numerous examples of hyperlink ID's that make no sense at all. Take HHSAR part 317: the contents of this has almost not a single id that makes logical sense. For example, what exactly is `P8_300` supposed to mean in a section that direcetly preceeds `P18_1718`?

Each section should have a hyperlink of course, but how about a more generalized format such as the actual reference of the text in the regulation? `P8_300` is the hyperlink ID for HHSAR 317.105-1. What if it was called `0317_105_1` so that we can parse this ID and easily get the part, section, and subsection? Having links like this in a more standardized format will allow setting up the webpage so much easier and more convenient. A solid foundation eases future edits.

### 3.3 - Separate HTML Files for Every Subsection
I believe that each subsection for every regulation deserves to be it's own object in some sort of database to be pulled or edited at will. However, each of these subsections absolutely does not need to be their own HTML file.

Individuals in the acquisition field are not trained to read just the specific verbiage of text that relates to their requirement: they are taught to 'zoom-out' to the prescription of said text, then to 'zoom-out' even further to see if it still applies. This 'zooming-out' is crucial to ensuring any and all text applies to the issues at hand, and having one HTML file per subsection is inefficient, unnecessary, and wasteful of space.

The good news is, much of the regulations are already strcutured this way. This problem isn't too big among the supplements, but when it gets to the DFARS, all the text pertaining to each section and subsection brings users to individual links for not only each text, but the Table of Contents for each section. Above all, this is annoying since 'zooming-out' entitles you to hit the back button about four or five times before you actually get to where you need to reference.

If every part of every regulation were just one HTML file, searching through contents will be so much easier. Once users find the paragraph they require, they simple just scroll up to read the prescription, scroll-up even more to read more prescriptions, and finally scroll to the top to insure everything complies. Again, this feature does exist but there are still separate HTML files lurking through the website waiting to catch users in a sticky web of inefficiency.

In conclusion, having separate HTML files for each subsection:
- makes it harder to manage code, since there would need to be a `#` in links to distinguish separate files
- increases file bloat and system capacity
- makes the users' jobs harder by spending more energy trying to find prescriptions
- is completely unnecessary

Why mention this with the API? The database will store the HTML for each subsection and generating the one HTML file for the regulation's part will just be a matter of combining all the appropriate objects together. This may even be how it is managed...

### 3.4 - Mobile Versions an Unneeded Luxury
The current system uses a DITA system to manage their content which seems perfect for this but in all honesty, a mobile version of the FAR is just not warranted. Users who routinely seach trough the FAR don't use it on mobile devices, but on computers. This may seem counterintuitive to today's society, but a mobile version is just not required for the vast majority of acquisitions professionals.

But in either case, a FAR API will be able to send information to any device which will reduce the need to have multiple formats for the same publication.

## 4.0 - Complications with an API
This project will not be without its problems. There are of course many things that could go wrong with this approach, which will be explained below for transparency.

### 4.1 - It won't be Searchable

Part of why having the FAR is valuable in HTML is that google can do its thing and search for exactly where a regulation is required. This puts [acquisition.gov](acquisition.gov) above the rest, as their layouts are very clean and obviously well taken care-of. Besides from both of the problems above, I don't see any other website taking the reigns off of them to house the FAR.

This supposed web app may be very useful and convenient, but it will lack the searching power of having these regs in HTML. This alone almost begs the question as to why even build this thing if you can't search in it? Maybe there is a way to integrate searching in this, which would make this even greater, but that's another project within this project.

So with all this said, this web app will primarily be a nice tool to supplement the FAR - meant for people who already know where to look for a specific reference and needing to see whether this reference is referenced in any number of regulations. Limited capablities, but convenient.

### 4.3.- Text Will Still Need to be Manually Updated
Either way, the FAR will need to be updated to reflect the many changes that update on a normal basis. This means that there will probably be more work involved with managing an API along with the text itself. Perhaps the DITA packages currently in use are perfect for the job already.

### 4.3 - Potentially Costly
Having an API with constant data calls could potentially be more costly than just having HTML sitting on a website. The traditional website design that isn't like a web app is tried and true and more than likely isn't generating heavy costs. An AWS account that gets charged by the click could rack up many expenses.

### 4.4 - Lack of Other Users
This goes with 4.3 above, but if the sole purpose of this API is to provide a more dynamic FAR, then it may not be as useful as we can imagine. What would be great is if there were many sources of information pulling the API to get text. Perhaps the contracting systems can pull this information to apply clauses, but there is no guarantee that this will even be a possibility among them.


