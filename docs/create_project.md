Instructions for creating a REDCAP Project
==========================================

Prerequisites
-------------

Python, Selenium, Firefox, and PhantomJs(Optional) must be installed on your system to use these tools.  Check install_prerequisites.md file for detailed instructions:


Step 1:
------
Navigate to scripts folder

Step 2:
------

Run the below command with project name and data-dictionary location as your arguments

./install <project-name> <data-dictionary-path>

Step 3:
------

You will be prompted to enter username and password . If you have not set any username and password just press Enter.

Step 4:
------

If no errors have been displayed you project creation and data dictionary upload was successfull. Open REDCap home page in your browser and navigate to My Projects tab.
If errors skip to step 5 .

Step 5:
------
Debugging :

Case 1) The default url is http://127.0.0.1:8080/redcap/index.php. If by any chance your REDCap home page url is not this you can give your custom url as the 3rd argument while running the shell script in step 2

	./install <project-name> <data-dictionary-path> <redcap-url>

Case 2) There are chances that even if you have set username and password, the browser might redirect to homepage if you have an active session. Try to run the script as mentioned in step 2 with username and password as blank.
