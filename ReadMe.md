# Pluralsight Module Checker #
psmodulecheck

## Brief Description##
A module folder validator for Pluralsight authors. Check a module folder to see that it is ready for submission. This tool can also rename all the clips in a folder to match the specified course id. It will also rename the clips inside the meta file.

## Usage ##
Edit the settings.json file for your preferences. You'll want to specify the first five settings.
 
1. `path` - This is the parent folder of where your module folder to be tested can be found. 
2. `shortId` - If you don't name everything after your full course id, specify the short name you use; otherwise enter your full course id here.
3. `courseId` - the full courseId for your course.
4. author - your official Pluralsight author name
5. `createFullCourse` - true if you want to copy files to a deployment folder (like Dropbox). If shortId and courseId are different the renaming will take place when the files are copied. Enter `false` (lowercase f) if you don't want a copy/rename to take place.
6. `fullCourseDestinationPrefix` - The full path to parent folder where you want the module folder copied.

Nothing else in the settings should need changed. These are various values used by the program and if Pluralsight changes some things in the future we may need to modify these values. 

###Definitions###
- **root**: the folder that contains the psmodulecheck.py file  
- **package top**: the folder that contains the setup.py and this readme file

From the command line at the root:

	python -m psmodulecheck           # run the main program- get prompted 
	python -m psmodulecheck 01        #supply the module suffix
	python -m tests.test_filechecker  # run the file checker test 
or from the REPL

	>>>import psmodulecheck
	>>>psmodulecheck.main('01')

From the command line at the package top
	
	python -m psmodulecheck.psmodulecheck
	python -m psmodulecheck.psmodulecheck 01

This version will prompt you for the module suffix (i.e. 1, 01, 01-dist...) Alternately, you can specify it as a command line parameter.

    psmodulecheck.py 01

The command line argument will be used as the module suffix to check. For your first module this would be '1' '01' or '01-dist'. Just the entire string you use after the -m in the folder and clip names.


## Dependencies ##
1. Python 3.3
2. Colorama 0.2.7 
3. termcolor 1.1.0

## Long Description##

**A module folder has some invariant attributes. This program verifies that you have adhered to them. For example the folder must:**:

1. contain a  Demos folder or a no-demos.txt file
2. contain a questions.txt or no-questions.txt file
3. contain a meta file named after the enclosing folder
4. contain a slides.pdf or slides.pptx
5. not have *.wmv files that don't have an entry in the meta file
6. a file for every clip in the meta file

**The meta file should adhere to these rules**

1. It should be named the same as the enclosing folder
2. Every clip line has <clip href="some_clip_file.wmv"
   and some_clip_file.wmv should exist in the folder.
3. The author tag should match your author-id

**The question file should adhere to these rules**

1. the first non blank line should begin with Q)
2. the next line(s) should begin with - or *
3. finally there should be a line that begins with =
4. The next non-blank line after the = line should again begin with Q) again
5.	There must be exactly one line that starts with a *
6.	The line with = should contain a clip file name that exists in the folder.
(The program allows lines that start with a # symbol but that might not
 be allowed by Pluralsight )

### Creating the final folder ###
Optionally this program can create a new folder for submission of your module to Pluralsight. For example, you might work in your /user/MyDocuments directory. When you're ready to submit you want to copy the final module folder over to your DropBox. This program will perform the copy for you. Furthermore if an official course-id is long, it can be cumbersome to deal with in production. This program allows you to specify a short working name you use during production. When the new folder is created the course-id name in the settings will be used to replace all the working names. Specifically it will change the name of the module folder, the names of all the clip files, the names of the clip files in both the .meta file and the questions.txt file and the name of the meta file itself. In other words everything that needs to be renamed will be renamed and your module will be ready for submission. As a belts and suspenders kind of guy I re-run the validation tests again on the renamed and copied folder.

## Unit Tests##

1. All tests can be run from the root folder where the .py files live with this command

        python -m unittest discover -s tests

2. An individual test file can be run from the same location with
    
        python -m tests.test_filechecker

3. You can also run an individual test from the top of the package with

		python -m psmodulecheck.tests.test_filechecker

# DISCLAIMER #
I wrote this for my own use but thought others might find it useful. Please back up your work before running this tool on your folder. There is no warranty, please see the license for the full disclaimer. I've only tested this on Windows 7 but I tried to make it compatible with other platforms. 

I don't work for Pluralsight (well, other than as an author). This program was not commissioned or blessed by them.

If you find any problems or think of a feature that would be nice to have please use the [issue tracker on the bitbucket site] [2], or contact me through yammer. 

Tod Gentille

 [1]: http://www.jetbrains.com/pycharm/  "JetBrains site for PyCharm - free open source edition is available"
  
 [2]: https://bitbucket.org/tgentille/pluralsight-module-checker/issues?status=new&status=open