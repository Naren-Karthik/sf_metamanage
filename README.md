# sfmetadatamanage
Python based windows CLI tool for creating &amp; managing Salesforce metadata snapshot, environment comparison &amp; change tracking.

Do you have multiple lower level sandboxes and each of its metadata is slipping away from every other sandbox due to one or all of the below reason
- Incremental changes across sandboxes are not aligned due to multiple developers working on changes in different sandboxes
- Direct defect fixes to higher sandoxes are not getting synced back to all of your lower sandboxes
- Vendor team is building new features in sandboxes different from those being used by the internal dev team for security or IP reasons

Be it as a company using Salesforce or as a Salesforce project manager or developer or admin, you would have come across this scenario quite a few times.

This python based tool is built to address that and even more in future as new features are rolled out.

***With this tool you can***

- Take "date stamped" snapshot of a specific org and back it up 
- Take snapshot of specific metadata types like ApexClass, Profiles and many more from the org you want
- Compare between 2 orgs and get a complete list of matches & discrepancies listed out in a easy to understand way
- You can even compare specific list of metadata types between 2 orgs
- You can automate all this with just few lines of powershell scripts to run daily, weekly or based on required schedule

***Common uses***
- A date stamped snapshot will allow you to have a last set of working metadata to revert back to in case of inadhverent changes
- This tool also allows backing up of most commonly changing metadata types like ApexClass, ApexTrigger, ApexPages, ApexComponents, CustomObjects and Profiles can be selectively rather then the complete org which will have rarely changing metadata like Sites
- Now you can find real-time comparison of different org which will help in making key decisions like should we refresh a lower sandbox with production metadata by providing you with exactly what is the additional metadata is available in lower sandbox which will be lost due to the refresh.
- This will also help the other way around where you can use this information to decide what metadata which is additional in lower sandboxes should be promoted to higher sandbox or production.

***Prerequisites***

To start using this CLI tool the below setup needs to be completed in your laptop or server used for code management. These steps are detailed in the setup_instructions.docx in the [docs folder] (https://github.com/Naren-Karthik/sfmetadatamanage/tree/master/docs) above.
1. Installing Python
2. Setting up Salesforce retrieve folder
3. Setting up the code folder

***Using the CLI tool:***

So let’s assume you installed Python and you have created a folder named “salesforce_retreive” in C drive and placed the unzipped “src” folder and “code” folder inside this folder and completed all the setup steps in the word document attached above.

Step 1: Go to command prompt - (windows button + r) and `cmd`

Step 2: Go to the “code” folder 

`cd <Code folder path> and hit ENTER`

For the above scenario it will be 

`cd C:\salesforce_retreive\code`

## For complete pull of a single environment
Step 2a: Type: python complete_pull_env.py <desired folder path> <environment_property_file_name> and hit ENTER

For the above setup let’s say you want to pull “test” environment, then it will be 

`python complete_pull_env.py “C:\salesforce_retreive” test`

Please note: It will only pull the components which are provided through “use” parameter in the “component_list.txt” inside the reference folder.

Step 3: Once it is done, the retrieve output will be saved in a folder name as today’s date inside in complete_pull folder which will be inside the folder you had created in step 1 of the “Setting up Salesforce retrieve folder”

For the above scenario it will be stored under

`C:\salesforce_retrieve\complete_pull`

## For complete pull & compare of two different environments
Step 2a: Type: python compare_retrieve_envs.py <desired folder path> <source_env> <target_env>

For the above setup let’s say you want to pull and compare between “test” and “dev” environments, then it will be 

`python compare_retrieve_envs.py “C:\salesforce_retreive” test dev`

Please note: It will only pull & compare the components which are provided through “use” parameter in the “component_list.txt” inside the reference folder.

Step 3: Once it is done, the retrieve and compare output will be saved in a folder name as today’s date inside in retrieve_compare folder which will be inside the folder you had created in step 1 of the “Setting up Salesforce retrieve folder”

For the above scenario it will be stored under

`C:\salesforce_retrieve\retrieve_compare`

***Please note:***
The following 4 metadata components won’t be pulled as of yet as they follow a different storage/retrieval pattern in Salesforce.
1.	Dashboard
2.	Document
3.	EmailTemplate
4.	Report
