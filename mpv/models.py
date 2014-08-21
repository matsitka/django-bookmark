from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager

#user
from accounts.models import User
from django.conf import settings

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
# Create your models here.

#beautiful soup
from bs4 import BeautifulSoup, Tag
import requests
import lxml

#save new image
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import ContentFile

#save new image url to db
from PIL import Image
import urllib2
from StringIO import StringIO

#embed
import urlparse as ups


class Tagged(TaggedItemBase):
    content_object = models.ForeignKey('Share')

class Share(models.Model):
    author = models.ForeignKey(User, related_name='shares')
    #author = models.ForeignKey(settings.AUTH_USER_MODEL)
    ### date and time stuff
    created_at = models.DateTimeField(auto_now_add=True)

    ### generate random string  http://stackoverflow.com/questions/4884584/django-generate-default-slug
    def __str__(self):
        return self.random

    def randomString():
        um = UserManager()
        return um.make_random_password(length=10)

    random = models.CharField(max_length=10, default=randomString)

    taggit = TaggableManager(through=Tagged)




class Text(Share):
    comment = models.TextField(max_length=1000, default="")
    def __unicode__(self):
        return self.comment

    #taggit = TaggableManager(blank=True)

#This method only works on calling the Link Model
def image_width(self, url, width, height, output_name, output_image):
        input_file = StringIO(urllib2.urlopen(url).read())

        output_file = StringIO()
        # create PIL Image instance
        img = Image.open(input_file)
        img.load()

        #if img.mode == "RGB":
        #    img = img.new("RGB")

        #http://stackoverflow.com/a/9459208/2942942
        # if .png???
        #if img.mode == "RGBA":
        #    background = img.new("RBG", img.size, (255, 255, 255))
        #    background.paste(img, mask=img.split()[3])

        ### http://stackoverflow.com/a/5184053/2942942

         # if not RGB, convert
        if img.mode not in ("L", "RGB"):
            img = img.convert("RGB")

        #define file output dimensions (ex 60x60)
        x = width
        y = height

        #get orginal image ratio
        img_ratio = float(img.size[0]) / img.size[1]

        # resize but constrain proportions?
        if x==0.0:
            x = y * img_ratio
        elif y==0.0:
            y = x / img_ratio

        # output file ratio
        resize_ratio = float(x) / y
        x = int(x); y = int(y)

        # get output with and height to do the first crop
        if(img_ratio > resize_ratio):
            output_width = x * img.size[1] / y
            output_height = img.size[1]
            originX = img.size[0] / 2 - output_width / 2
            originY = 0
        else:
            output_width = img.size[0]
            output_height = y * img.size[0] / x
            originX = 0
            originY = img.size[1] / 2 - output_height / 2

        #crop
        cropBox = (originX, originY, originX + output_width, originY + output_height)
        img = img.crop(cropBox)

        # resize (doing a thumb)
        img.thumbnail([x, y], Image.ANTIALIAS)

        img.save(output_file, "JPEG", quality=90)
        output_image.save(self.title + output_name + ".jpg", ContentFile(output_file.getvalue()), save=False)


class Link(Share):
    comment = models.TextField(max_length=1000, blank=True, default="")
    url = models.URLField(max_length=200, default="")
    #title = models.CharField(max_length=100, blank=True)
    def __unicode__(self):
        return self.url

    #taggit = TaggableManager(blank=True)

    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    keywords = models.TextField(blank=True)

    image_url = models.URLField(default="", blank=True)

    new_linkimage = models.ImageField(upload_to="link/", default="", blank=True)

    new_linkthumb = models.ImageField(upload_to="link/thumb/", default="", blank=True)

    ##embed
    youtube = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    vine = models.CharField(max_length=100, blank=True)
    vimeo = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    soundcloud = models.CharField(max_length=100, blank=True)


    def embed_get(self, url):
        #if "youtube.com" in self.url:
        #    self.youtube = "12345"

        ## get the youtube id: https://www.youtube.com/watch?v=42luHhrsNhg
        ## returns 42luHhrsNhg

        #http://stackoverflow.com/a/8816453/2942942

        ## fonctionne avec
        #https://www.youtube.com/watch?v=42luHhrsNhg
        #https://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
        if "youtube.com" in self.url:
            try:

                m = ups.urlparse(self.url)
                self.youtube = ups.parse_qs(m.query)['v']

            except KeyError:
                self.youtube = "none"

        else:
            self.youtube = "none"



        if "instagram.com/p/" in self.url:


            #self.instagram = "1223"
            #http://stackoverflow.com/a/15296847/2942942
            try:
                ups.urlparse(self.url)
                self.instagram = ups.urlparse(self.url).path.lstrip("/")
            except KeyError:
                self.instagram = "none"

        else:
            self.instagram = "none"

        if "vine.co/v/" in self.url:

            try:
                ups.urlparse(self.url)
                self.vine = ups.urlparse(self.url).path.lstrip("/")
            except KeyError:
                self.vine = "none"

        else:
            self.vine = "none"

        if "vimeo.com" in self.url:

            try:
                ups.urlparse(self.url)
                self.vimeo = ups.urlparse(self.url).path.lstrip("/")
            except KeyError:
                self.vimeo = "none"

        else:
            self.vimeo = "none"

        #m = ups.urlparse(self.url)
        #self.instagram = ups.parse_qs(m.query)['v']
        #self.instagram = "1223"


    #extract url title, description and keywords
    #http://stackoverflow.com/questions/11092192/extracting-values-from-meta-tags-and-img-url-having-only-url-of-website-written?rq=1

    #Scrap the url and extract its title, description, image_link from og image
    """
    sudo apt-get install libxml2-dev
    sudo apt-get install libxslt1-dev
    """



    def download_url(self, url):
        if self.url and not (self.title or self.keywords or self.description or self.image_url or self.new_linkimage):
            # optionally, use 'html' instead of 'lxml' if you don't have lxml installed
            soup = BeautifulSoup(requests.get(self.url).content, "lxml")

            try:
                self.title = soup.title.string #try to capture the title
            except AttributeError: #if no title found?

                #if AttributeError:
                #self.title = soup.find('meta', {"property":'og:title'}) #try to capture the og:title
                #else:
                self.title = "No Title Found"


                #self.title = "No Title Found"
                pass
            #self.title = soup.title.string
            meta = soup.find_all('meta')
            for tag in meta:
                if 'name' in tag.attrs and tag.attrs['name'].lower() in ['description', 'keywords']:
                    setattr(self, tag.attrs['name'].lower(), tag.attrs['content'])

            # extract fb og image
            try:
                self.image_url = soup.find('meta', {"property":'og:image'})['content']
            except TypeError: #if empty?
                self.image_url = "http://www.placehold.it/585x300/9995BE/ffffff" #make default image entry
                pass



            #finder = soup.find('meta', {"property":'og:image'})['content']
            #if finder == "":
            #    self.image_url = "http://matsitka.com/static/img/sitka_logo_fb.jpg" #if empty, assign empty or default entry
            #else:
            #    self.image_url = finder #if not empty, assign url image link



    #save the image url to the db ### http://stackoverflow.com/a/10297620/2942942
    """
    install libjpeg-dev with apt
    sudo apt-get install libjpeg-dev

    not sure about this one??? http://stackoverflow.com/a/12561906/2942942

    sudo apt-get install libpng12-dev
    """



    def save_image(self, url, new_linkimage):

        #read url image, resize and save
        image_width(self, url, 585, 300, "_original", new_linkimage)


    def save_thumb(self, url, new_linkthumb):

        #read url image, resize and save thumbnail
        image_width(self, url, 146, 146, "_thumb", new_linkthumb)


    def save(self, *args, **kwargs):
        self.download_url(self)
        self.embed_get(self)
        #self.instagram_get(self)
        self.save_image(self.image_url,  self.new_linkimage)
        self.save_thumb(self.image_url,  self.new_linkthumb)
        super(Link, self).save(*args, **kwargs)

#this global method only works on the Photo Model
def image_width_photo(self, url, width, height):
        #input_file = StringIO(urllib2.urlopen(url).read())

        output_file = StringIO()
        # create PIL Image instance
        img = Image.open(self.image_original)
        img.load()

        ### http://stackoverflow.com/a/5184053/2942942

         # if not RGB, convert
        if img.mode not in ("L", "RGB"):
            img = img.convert("RGB")

        #define file output dimensions (ex 60x60)
        x = width
        y = height

        #get orginal image ratio
        img_ratio = float(img.size[0]) / img.size[1]

        # resize but constrain proportions?
        if x==0.0:
            x = y * img_ratio
        elif y==0.0:
            y = x / img_ratio

        # output file ratio
        resize_ratio = float(x) / y
        x = int(x); y = int(y)

        # get output with and height to do the first crop
        if(img_ratio > resize_ratio):
            output_width = x * img.size[1] / y
            output_height = img.size[1]
            originX = img.size[0] / 2 - output_width / 2
            originY = 0
        else:
            output_width = img.size[0]
            output_height = y * img.size[0] / x
            originX = 0
            originY = img.size[1] / 2 - output_height / 2

        #crop
        cropBox = (originX, originY, originX + output_width, originY + output_height)
        img = img.crop(cropBox)

        # resize (doing a thumb)
        img.thumbnail([x, y], Image.ANTIALIAS)


        img.save(output_file, "JPEG", quality=90)

        #save the image resize
        self.image_crop.save(self.random+".jpg", ContentFile(output_file.getvalue()), save=False)

class Photo(Share):
    comment = models.TextField(max_length=1000, blank=True, default="")
    image_original = models.ImageField(upload_to="photo/%Y/%m/%d", default="")
    #image_original = models.FileField(upload_to="photo/%Y/%m/%d", default="")
    image_crop = models.ImageField(upload_to="photo/thumb/%Y/%m/%d/", default="", blank=True)


    def save_image(self, url):
        image_width_photo(self, url, 585, 420)

    def save(self, *args, **kwargs):

        self.save_image(self.image_original)
        #self.save_thumb(self.image_url)
        super(Photo, self).save(*args, **kwargs)


    #taggit = TaggableManager(blank=True)


