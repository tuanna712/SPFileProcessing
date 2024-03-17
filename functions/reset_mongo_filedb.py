import json
from functions.core.connectors import Connector
from functions.core.mongodb import MGCollection

def update_urls_dict():
    SPConnector = Connector().to_sharepoint()
    MAIN_SITE = "/sites/Eptesting/Shared Documents/General/DATABASE/Song Hong Basin/"
    TARGET_FOLDER = ["Block 103-107", "Block 105", "Block 108", "Block 111", "Block 112", "Block 113", "Block 114", "Block 115"]
    
    file_links, _ = SPConnector._get_all_files_links()

    _all_urls = []
    for folder in TARGET_FOLDER:
        print(f"Processing folder {folder}...")
        TARGET_FOLDER_URL = MAIN_SITE + folder
        _urls = [url for url in file_links if url.startswith(TARGET_FOLDER_URL)]
        _all_urls.extend(_urls)
        print(f"Found {len(_all_urls)} files.\n")

    _urls_dict = {}
    for i in range(len(_all_urls)):
        _urls_dict[i] = _all_urls[i]
    with open(f"data/urls.json", "w") as f:
        json.dump(_urls_dict, f)

def save_files_info_to_db():
    with open("data/urls.json", "r") as f:
        _urls = json.load(f)
    
    SPConnector = Connector().to_sharepoint()
    
    MGC = MGCollection(db_name="SharePointManager", collection_name="files_database")
    # Delete collection
    MGC.delete_collection("files_database")

    # Re-create collection
    for i in range(len(_urls)):
        print(f"Processing file {i} ...", _urls[str(i)])
        data = SPConnector.get_metadata(_urls[str(i)])
        del data['ListItemAllFields']
        _list_of_field = ['ReportName', 'YearOfPublication', 'Basin', 'Block', 'WellName', 'ReportAuthor', 'Contractors', 'TypeofFormat', 'TypesOfReport', 'StatusOfReport', 'Fields']
        for field in _list_of_field:
            # How to check a field is a dict or not
            if isinstance(data[field], dict):
                _dict = data[field]
                data[field] = list(_dict.values())
                
        # data = {str(key): {str(k): v for k, v in value.items()} if isinstance(value, dict) else value for key, value in data.items()}

        #Update to MongoFileManager
        MGC.insert_one(data)
        print('Done!')

if __name__ == "__main__":
    update_urls_dict()
    save_files_info_to_db()
    print("Done!")


from functions.core.mongodb import MGCollection
MGC = MGCollection(db_name="SharePointManager", collection_name="files_database")
r = MGC.get_docs_by_multiple_key_values({"$text": {"$search": 'Biostratigraphy'}})
for i in r:
    print(i)
    print('\n')