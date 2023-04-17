from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.urls import reverse
# Create your models here.

class Home(models.Model):
    #cv = CloudinaryField('cv')
    cv = models.FileField(upload_to='cv/', storage=RawMediaCloudinaryStorage())
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Home {self.pk}"




class About(models.Model):
    subject = models.CharField(max_length=50, blank=True, null=True)
    image = CloudinaryField('images')
    description = models.TextField(blank=True, null=True)
    languages = models.CharField(max_length=200, blank=True, null=True)
    frameworks = models.CharField(max_length=200, blank=True, null=True)
    other = models.CharField(max_length=200, blank=True, null=True)

class Skills(models.Model):
    class Meta:
        verbose_name_plural = "skills"
        verbose_name = 'skill'

    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    image = CloudinaryField('images' )

    def __str__(self):
        return self.name


class Contact(models.Model):
    class Meta:
        verbose_name_plural = "contacts"
        verbose_name = "contact"
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=100, blank=True, null=True )
    message = models.TextField(null=True, blank=True)
    send_time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject}"

class PortfolioProfile(models.Model):
    class Meta:
        verbose_name_plural = 'portfolio profiles'
        verbose_name = 'portfolio profile'

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = CloudinaryField('images')
    skills = models.ManyToManyField(Skills, blank=True)
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user}'

class Media(models.Model):
    class Meta:
        verbose_name_plural='media files'
        verbose_name='media'
    image = CloudinaryField('images')
    url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=200,  blank=True, null=True)
    is_image = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if self.url:
            self.is_image=False

    def __str__(self):
        return f'{self.name}'

class PortfolioProjects(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    brief_description = models.TextField(null=True, blank=True)
    body = RichTextField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    tools = models.CharField(max_length=200, blank=False, null=False)
    demo = models.URLField()
    github = models.URLField()
    snap = CloudinaryField('images', null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(PortfolioProjects, self).save(args, **kwargs)

    def get_absolute_url(self):
        return f'/portfolio/{self.slug}'

class Certificate(models.Model):
    class Meta:
        verbose_name_plural = 'Certificates'
        verbose_name ='Certificate'

    name=models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    class Meta:
        verbose_name_plural = 'Blog profiles'
        verbose_name = 'Blog'

    author = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    body = RichTextField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    image = CloudinaryField('images')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Blog, self).save(args, **kwargs)

    def __str__(self):
        return self.name

    def get_blog_url(self):
        return f'/blog/{self.slug}'
    
    class Measurement(models.Model):
    location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Distance from {self.location} to {self.destination} is {self.distance} km"


