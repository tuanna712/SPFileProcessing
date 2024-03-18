#Sharepoint authentication settings
SP_URL = "https://viendaukhivn.sharepoint.com/sites/Eptesting"
CLIENT_ID = "2b8bc67b-26f2-4431-a208-a88d0bbf5396"
CLIENT_SECRET = "RPORi5qG9W28skRVbxbLrF/4oWPCaLkYULOscT62Mmk="

#Sharepoint settings
TENANT_URL = "https://viendaukhivn.sharepoint.com"
MAIN_SITE = "/sites/Eptesting/Shared Documents/General/DATABASE/Song Hong Basin/"
TARGET_FOLDER = ["1. Regional Studies",
                "Block 100-101",
                "Block 102-106",
                "Block 103-107",
                "Block 104",
                "Block 105",
                "Block 108",
                "Block 111",
                "Block 112",
                "Block 113",
                "Block 114",
                "Block 115",
                "Block 117",
                "Block 118",
                "Block 119",
                "Block 120",
                "Block 121",
                "MVHN 01 02KT",
                "MVHN 02",
                ]
TEMP_FILE_FOLDER = "./data/temp/processing"
TEMP_IMAGE_FOLDER = "./data/temp/images"

DEFAULT_URL_FILE = "data/urls.json"

#Local Path to save fetched all SITE's urls
FETCHED_SITE_FILE_URLS_JSON = "data/site_file_urls.json"

USER_NAME = "tuanna"
IMG_PROCESSING_FOLDER = "./data/temp/usercontent/" + USER_NAME 

#MongoDB settings
MONGODB_NAME = "SharePointManager"
MG_PROCESS_COLL = "processing_files_database"
MG_IMAGE_COLL = "processed_image_database"
MG_TABLE_COLL = "processed_table_database"

#Weaviate settings
WEAVIATE_URL = "https://vpivector-oucjj2y3.weaviate.network"
WEAVIATE_API_KEY = "cvyMuAFfHjP0ks4yijqPM1wYjrs6PhN74aLQ"
WEAVIATE_COLL_NAME = "MAIN_EnP_DATABASE"