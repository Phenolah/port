from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
# Create your models here.

class Home(models.Model):
    cv = models.FileField(blank=True, null=True, upload_to="cv")
    avatar = models.ImageField(blank=True,null=True, upload_to='avatar')
    email = models.EmailField(blank=True, null=True)

class About(models.Model):
    subject = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='about')
    description = models.TextField(blank=True, null=True)

class Skills(models.Model):
    class Meta:
        verbose_name_plural = "skills"
        verbose_name = 'skill'

    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    image = models.FileField(blank=True, null=True, upload_to="images")
    def __str__(self):
        return f"{self.name}"

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
    avatar = models.ImageField(blank=True,null=True, upload_to='avatar')
    skills = models.ManyToManyField(Skills, blank=True)
    about = models.TextField(blank=True, null=True)

#class Media(models.Model):
    #class Meta:
        #verbose_name_plural='media files'
        #verbose_name='media'
    #image = models.ImageField(blank=True, null=True, upload_to='media')
    #url = models.URLField(blank=True, null=True)
    #name = models.CharField(max_length=200,  blank=True, null=True)
    #is_image = models.BooleanField(default=True)

    #def save(self, *args, **kwargs):
        #if self.url:
            #self.is_image = False

     #def __str__(self):
         #return f'{self.name}'

class PortfolioProjects(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    brief_description = models.TextField(null=True, blank=True)
    body = RichTextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='portfolio')
    slug = models.SlugField(null=True, blank=True)
    tools = models.CharField(max_length=200, blank=False, null=False)
    demo = models.URLField()
    github = models.URLField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/portfolio/{self.slug}'

