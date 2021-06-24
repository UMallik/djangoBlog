from django.db import models
from PIL import Image
# Create your models here.
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here
class Author(models.Model):

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    pp = models.ImageField(default = 'default/default.jpg', upload_to = 'profile_pics',verbose_name='Profile Picture')
    # additional fields
    activation_key = models.CharField(max_length=255, default=1)
    email_validated = models.BooleanField(default=False)



    def __str__(self,*args, **kwargs):
        return self.user.username

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.pp.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.pp.path)
            
        


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(help_text='Slug will be generated automatically', unique=True)
    author = models.ForeignKey(Author, null=True, blank=True, on_delete = models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'
    
    def get_absolute_url(self):
        return reverse('blog:post_by_category', args = [self.slug])


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Tags')
    slug = models.SlugField(help_text='Slug will be generated automatically', unique=True)
    author = models.ForeignKey(Author, null=True, blank=True, on_delete = models.CASCADE)

    def __str__(self):

        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_by_tag', args = [self.slug])


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text='Slug will be generated automatically')
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post,self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.id, self.slug])

class Feedback(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the sender")
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Feedback"

    def __str__(self):
        return self.name+ "-" + self.email

    def get_absolut_url(self):
        return reverse('blog:feedback')