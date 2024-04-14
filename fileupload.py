import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api
from os import environ

cloudinary.config( 
  cloud_name = environ.get("CLOUDINARY_NAME"), 
  api_key = environ.get("CLOUDINARY_KEY"), 
  api_secret = environ.get("CLOUDINARY_SECRET") 
)


def upload_image(file_object, filename):
    cloudinary.uploader.upload(file_object,
                               public_id=filename,
                               unique_filename=False,
                               overwrite=True)
    src_url = CloudinaryImage(filename).build_url()
    print(src_url)
    return src_url

if __name__=="__main__":
    with open("/home/frost/Pictures/test.jpg","rb") as f:
        print(upload_image(f, "yash_pfp"))
