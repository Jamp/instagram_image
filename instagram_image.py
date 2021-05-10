rom os import environ, unlink
from os.path import join, exists
from random import choice
from string import ascii_lowercase, digits
from PIL import Image
from requests import get
from boto3 import client

__IMAGE_SIZE__ = (256, 256)
__AVATAR_SIZE__ = (32, 32)

__DIRECTORY_BASE__ = '/tmp/'
__HEADERS__ = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/_BuildID_) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36'
}


def get_image(url_image, id_post):
    original_uri = __download_image__(url_image)
    compressed_uri = None
    url_uploaded = None

    if original_uri:
        compressed_uri = __optimize_image__(original_uri)
        
        __cleanup__(original_uri)

    if  compressed_uri:
        url_uploaded = __upload_image__(compressed_uri, id_post)
        
        __cleanup__(compressed_uri)
    
    return url_uploaded
        

def get_avatar(url_image, id_user):
    original_uri = __download_image__(url_image)
    compressed_uri = None
    url_uploaded = None

    if original_uri:
        compressed_uri = __optimize_image__(original_uri, 'avatar')
        
        __cleanup__(original_uri)

    if  compressed_uri:
        url_uploaded = __upload_image__(compressed_uri, id_user)
        
        __cleanup__(compressed_uri)
    
    return url_uploaded


def __download_image__(image_url):
    new_file = __random_name__() + '.jpg'

    try:
        response = get(image_url, headers=__HEADERS__)

        filename_destiny = __get_path__(new_file)
        file = open(filename_destiny, 'wb')
        file.write(response.content)
        file.close()

        return new_file

    except Exception as e:
        print("Can't download image")
        print(e)

        return


def __optimize_image__(image_name, format='image'):
    filename = image_name.lower().replace('.jpg', '-compressed.jpg')
    original_path = __get_path__(image_name)
    compressed_path = __get_path__(filename)

    if format == 'avatar':
        size = __AVATAR_SIZE__

    else:
        size = __IMAGE_SIZE__
    
    try:
        im = Image.open(original_path)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(compressed_path, format='JPEG', quality=50, optimize=True)

        return filename

    except Exception as e:
        print("Can't resize image")
        print(e)

        return


def __upload_image__(image_name, final_name):
    filename = __get_path__(image_name)
    key = '%s.jpg' % final_name

    region = environ.get('REGION_S3')
    bucket = environ.get('BUCKET_S3')
    access_key = environ.get('ACCESS_KEY_S3')
    secret_key = environ.get('SECRET_KEY_S3')

    if not region:
        raise('I need environment variable for S3 Region named "REGION_S3"')

    if not bucket:
        raise('I need environment variable for S3 Bucket named "BUCKET_S3"')

    if not access_key:
        raise('I need environment variable for S3 Access Key named "ACCESS_KEY_S3"')

    if not secret_key:
        raise('I need environment variable for S3 Secret Access Key named "SECRET_KEY_S3"')

    s3 = client(
        's3',
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    try:
        data = open(filename, 'rb')
        s3.put_object(Bucket=bucket, Key=key, Body=data, ContentType='image/jpeg', ACL='public-read')

        return "https://{0}.s3.amazonaws.com/{1}".format(bucket, key)  # Public URL

    except Exception as e:
        print("Can't upload image")
        print(e)

        return


def __random_name__(size=32):
    chars = ascii_lowercase + digits
    return ''.join(choice(chars) for _ in range(size))


def __get_path__(filename):
    return join(__DIRECTORY_BASE__, filename)


def __cleanup__(image_name):
    image_path = __get_path__(image_name)

    if exists(image_path):
        unlink(image_path)
