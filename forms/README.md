# REDCap Forms

This directory contains REDCap forms developed for use in the REDCap systems.

## Using forms in this collection

To use a form, review its requirements in README.md included with the form.  Once the requirements are met, one generally need only import the associated .CSV file into a REDCap project.

Form requirements could specify a minimum REDCap version, specific REDCap add ons, or data sources.  MAke sure you review the dpcumentation included with each form to assure it will work correct once addedd to a REDCap Project.


## Adding forms to this collection

To add forms to this collection, make a new directory for your form or forms.  In the directory add one of more .CSV files for your form(s).  Please also add a file README.md, written in Markdown format (see http://daringfireball.net/projects/markdown/syntax).

The README should describe important details about the form(s).  It should include:

* A description of the form or forms
* Requirements
** Specifically the minimum REDCap version under which you expect this form to work
** Required REDCap extensions
** Required access to services like Bioportal or Vanderbilt's REDCap Server
* Acknowledgements of authors and contributors
* License - under what Open Source license is this content distributed. We recommend Apache 2.0 but respect that other license might already be in use.

The directory should include a test script for testing the form.  The form should at least load into REDCap. Other forms in this repo have example tests that can be copied and adapted for this purpose.
