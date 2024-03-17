#---SHAREPOINT-CONNECTION-------------------------------------------------------------------------------------------------------------
from openai import OpenAI
from openai import AzureOpenAI
import re, urllib.parse, os, nest_asyncio, warnings
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
# Disable all warnings
warnings.filterwarnings("ignore")
# Enable asyncio
nest_asyncio.apply()

def convert_sharepoint_url(original_url):
    if "Forms/AllItems" in original_url:
        # If the URL contains "Forms/AllItems", use regex to extract the desired path
        start_index = original_url.find('/sites/') + len('/sites/')
        end_index = original_url.find('/', start_index)
        # Extract the words before and after '/sites/'
        word_before_sites = original_url[:start_index]
        word_after_sites = original_url[start_index:end_index]

        # Merge the two words together to form the base URL
        site_url = f"{word_before_sites}{word_after_sites}"
        parsed_url = urllib.parse.urlparse(original_url)
        query = parsed_url.query
        match = re.search(r'id=([^&]+)', query)
        if match:
            target_url = urllib.parse.unquote(match.group(1))
            target_url = target_url.replace('%20', ' ')
            return site_url, target_url
    else:
        third_slash_index = original_url.find('/', original_url.find('/', original_url.find('/') + 1) + 1)
        # Extract the part before '/sites/'
        part_before_sites = original_url[:third_slash_index]
        # Find the index of the next '/' after '/sites/'
        sites_index = original_url.find('/sites/') + len('/sites/')
        next_slash_index = original_url.find('/', sites_index)
        # Extract the part after '/sites/'
        part_after_sites = original_url[sites_index:next_slash_index]
        # Merge the two parts together
        site_url = part_before_sites + "/sites/" + part_after_sites
        # For other URLs, use the path component and extract '/sites'
        parsed_url = urllib.parse.urlparse(original_url)
        path = parsed_url.path
        sites_index = path.find('/sites')
        if sites_index != -1:
            target_url = path[sites_index:]
            target_url = urllib.parse.unquote(target_url)
            return site_url, target_url
    return None  # Return None if the pattern is not found

def get_file(folderurl, site_url,client_id, client_secret): #get list of files under url
    try:
        site_url = site_url
        credentials = ClientCredential(client_id,client_secret)
        ctx = ClientContext(site_url).with_credentials(credentials)
        list_source = ctx.web.get_folder_by_server_relative_url(folderurl)
        files = list_source.files
        ctx.load(files)
        ctx.execute_query()
        return files
    except Exception as e:
        print(e)
        
def get_folder(folderurl, site_url,client_id, client_secret): #get list of folders under url
    try:
        site_url = site_url
        credentials = ClientCredential(client_id,client_secret)
        ctx = ClientContext(site_url).with_credentials(credentials)
        # file_url is the sharepoint url from which you need the list of files
        list_source = ctx.web.get_folder_by_server_relative_url(folderurl)
        folders = list_source.folders
        ctx.load(folders)
        ctx.execute_query()
        #return files
        folder_list=[]
        for folder in folders:
            folder_name = folder.properties["Name"]
            folder_url= folderurl + '/'+ folder_name
            folder_list.append(folder_url)
        return folder_list
    except Exception as e:
        print(e)

def download_file(file_url, filename, site_url,client_id, client_secret, localfolder): # file_url is the relative url of the file in sharepoint
    site_url = site_url
    credentials = ClientCredential(client_id, client_secret)
    ctx = ClientContext(site_url).with_credentials(credentials)
    localpath = localfolder + filename
    with open(localpath, "wb") as local_file:
        file = ctx.web.get_file_by_server_relative_url(file_url)
        file.download(local_file)
        ctx.execute_query()
    print(f" Your file is downloaded here: {localpath}")
    return localpath

def upload_file(file_path, target_url, site_url, client_id, client_secret):
    credentials = ClientCredential(client_id,client_secret)
    ctx = ClientContext(site_url).with_credentials(credentials)
    target_folder = ctx.web.get_folder_by_server_relative_url(target_url)                    
    with open(file_path, 'rb') as content_file:
        file_content = content_file.read()
        filename = os.path.basename(file_path)
        target_folder.upload_file(filename, file_content).execute_query()
    print('Done uploading file to', target_url)  

def rename_file(file_url, newname, site_url, client_id, client_secret):
    credentials = ClientCredential(client_id,client_secret)
    ctx = ClientContext(site_url).with_credentials(credentials)
    file = ctx.web.get_file_by_server_relative_path(file_url)
    file.rename(newname)
    ctx.execute_query()   
    print('Done renaming file!')
    
    
def get_file_extend_props(file_url, site_url, client_id, client_secret):
    """
    Retrieves file extended properties (accessible via associated ListItem)
    """
    ctx = ClientContext(site_url).with_credentials(ClientCredential(client_id, client_secret))

    file_item = (
        ctx.web.get_file_by_server_relative_url(file_url)
        .listItemAllFields.get()
        .execute_query()
    )
    return file_item

def clear_temp_folder(folder):
    # Delete all files in the temp folder
    import shutil
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            
def revise_text(text):
    text = " ".join(text.split("\n"))
    text = " ".join(text.split(" "))
    text = "".join(text.split("\t"))
    return text