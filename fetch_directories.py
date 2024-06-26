"""
Cretated on May 23,2024
@author: Muna Awel
Fetch directories and saves into a csv file containing the variables Directory,date created, date modified, script_name and owner.
Pandas used as a data frame
"""


import os
from datetime import datetime
import win32security
import pandas as pd

# win32security module allows to find the owners of the directories that were created.


def find_files_with_extension(directory, extensions):
    files = []
    for root, dirs, _ in os.walk(directory):
        for file in os.listdir(root):
            if file.endswith(tuple(extensions)):
                path = os.path.join(root, file)
                date_created = os.path.getctime(path)
                date_created = datetime.fromtimestamp(date_created).strftime('%Y-%m-%d %H:%M:%S')
                date_modified = os.path.getmtime(path)
                date_modified = datetime.fromtimestamp(date_modified).strftime('%Y-%m-%d %H:%M:%S')
                script_name = os.path.basename(path)
                sd = win32security.GetFileSecurity(path, win32security.OWNER_SECURITY_INFORMATION)
                owner_sid = sd.GetSecurityDescriptorOwner()
                name, _, _ = win32security.LookupAccountSid(None, owner_sid)
                files.append({'File Path': path, 'Date Created': date_created, 'Date Modified': date_modified, 'Script Name': script_name, 'Owner Name': name})
                
    return files
#----------------------------------------------------------------------------------------------------------------------------------------------------
# find_files_with_extensions functions creates and empty files variable adn with the os module it transverse through the giveen directiory looking for extensions.
# Once a match extenstion is found it creates variables and appends it to the files variable.


def export_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

directory_path = r"\\ad.sfwmd.gov\dfsroot\data\wsd\SUP\devel\source\Python"  ## update the directory that you need to access
extensions = [".py", ".r", ".docx", ".f", ".for", ".f77", ".f90", ".F", ".FOR", ".F77", ".F90", "m", ".cpp",".cc",".c++",".h",".bak",".inc",".sql",".zipx",".dssd",".dat",".par",".dscc",".stg",".lis",".norm"]
files_found = find_files_with_extension(directory_path, extensions)


export_to_csv(files_found, 'sup4.csv')  ## change the csv file name for every new directory


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
sql_code
SELECT apptype, scriptname, author, language,database, datecreated,
       datemodified, dependencies, instance, keyword, location,
       parentfile, documentation, project,schema, sql_standard, 
       description, recid 
  FROM KRODBERG.codeDocs 
 WHERE deleted IS NULL 
 ORDER BY RecID DESC
'''

