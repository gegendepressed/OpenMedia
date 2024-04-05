import os
from supabase import create_client, Client, StorageException
from mimetypes import guess_type

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Endpoint: https://lhebgmzvbaqyrvyxetaa.supabase.co/storage/v1/object/public/openmediabucket/Posts/example.jpg
# Endpoint: https://lhebgmzvbaqyrvyxetaa.supabase.co/storage/v1/object/public/openmediabucket/Profiles/example.jpg

def upload_post_image(file_object, filename):
    path_on_supastorage="Posts/"+filename
    
    try:
        supabase.storage.from_("openmediabucket").upload(file=file_object, path=path_on_supastorage,
            file_options={"content-type": guess_type(filename)[0]})
    except StorageException:
        None
        
    return url+"/storage/v1/object/public/openmediabucket/"+path_on_supastorage
    
def upload_profile_image(file_object, filename):
    path_on_supastorage="Profiles/"+filename
    
    try:
        supabase.storage.from_("openmediabucket").upload(file=file_object, path=path_on_supastorage,
            file_options={"content-type": guess_type(filename)[0]})
    except StorageException:
        None 
        
    return url+"/storage/v1/object/public/openmediabucket/"+path_on_supastorage

if __name__=="__main__":
    with open("test.jpg","rb") as f:
        print(upload_profile_image(f, "frostimage.jpg"))
