# sfmetadatamanage
Python code for creating &amp; managing Salesforce metadata snapshot, environment comparison &amp; change tracking.

Using the CLI tool:
So let’s assume you installed Python and you have created a folder named “salesforce_retreive” in C drive and placed the unzipped “src” folder and “code” folder inside this folder and completed all the setup steps in the word document attached above.

Please note: The following 4 metadata components won’t be pulled as of yet as they follow a different storage/retrieval pattern in Salesforce.
1.	Dashboard
2.	Document
3.	EmailTemplate
4.	Report

Step 1: Go to command prompt using (windows button + r) and entering cmd
Step 2: Go to the “code” folder by typing: cd <Code folder path> and hit ENTER
For the above scenario it will be  cd C:\salesforce_retreive\code

# For complete pull of a single environment
Step 2a: Type: python complete_pull_env.py <desired folder path> <environment_property_file_name> and hit ENTER
For the above setup let’s say you want to pull “test” environment, then it will be 
 python complete_pull_env.py “C:\salesforce_retreive” test
Please note: It will only pull the components which are provided through “use” parameter in the “component_list.txt” inside the reference folder.
Step 3: Once it is done, the retrieve output will be saved in a folder name as today’s date inside in complete_pull folder which will be inside the folder you had created in step 1 of the “Setting up Salesforce retrieve folder” section
For the above scenario it will be stored under
 C:\salesforce_retrieve\complete_pull


# For complete pull & compare of two different environments
Step 2a: Type: python compare_retrieve_envs.py <desired folder path> <source_env> <target_env>
For the above setup let’s say you want to pull and compare between “test” and “dev” environments, then it will be 
 python compare_retrieve_envs.py “C:\salesforce_retreive” test dev
Please note: It will only pull & compare the components which are provided through “use” parameter in the “component_list.txt” inside the reference folder.
Step 3: Once it is done, the retrieve and compare output will be saved in a folder name as today’s date inside in retrieve_compare folder which will be inside the folder you had created in step 1 of the “Setting up Salesforce retrieve folder” section
For the above scenario it will be stored under
 C:\salesforce_retrieve\retrieve_compare

