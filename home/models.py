from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm, TextInput, TextArea, EmailField
from django.http import request
from django.utils.safestring import mark_safe

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10)
    status = models.BooleanField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
llist = Language.objects.filter(status=True)
list1 = []
for rs in llist:
    list1.append((rs.code, rs.name))
langlist = (list1)

class Setting(models.Model):
    STATUS = (
        ('True','Mavjud'),
        ('False','Mavjud emas'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(blank=True,max_length=255)
    address = models.CharField(blank=True, max_length=255)
    phone = models.CharField(blank=True, max_length=255)
    fax = models.CharField(blank=True, max_length=255)
    email = models.CharField(blank=True, max_length=255)
    icon = models.ImageField(upload_to='images',blank=True)
    facebook = models.CharField(blank=True, max_length=255)
    instagram = models.CharField(blank=True, max_length=255)
    twitter = models.CharField(blank=True, max_length=255)
    youtube = models.CharField(blank=True, max_length=255)
    telegram = models.CharField(blank=True, max_length=255)
    whatsapp = models.CharField(blank=True, max_length=255)
    skype = models.CharField(blank=True, max_length=255)
    aboutus = RichTextUploadingField()
    contact = RichTextUploadingField()
    status = models.CharField(max_length=15, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class SettingLang(models.Model):
    setting = models.ForeignKey(Setting,on_delete=models.CASCADE)
    lang = models.CharField(max_length=20,choices=langlist)
    title = models.CharField(blank=True, max_length=255)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    aboutus = RichTextUploadingField()
    contact = RichTextUploadingField()

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    STATUS = (
        ('New','Yangi'),
        ('Read','Uqilgan'),
        ('Closed','Yopilgan'),
    )
    name = models.CharField(blank=True, max_length=255)
    email = models.EmailField()
    subject = models.CharField(blank=True, max_length=255)
    message = models.CharField(blank=True, max_length=255)
    status = models.CharField(max_length=15,choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=25)
    note = models.CharField(blank=True, max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name','email','subject','message']
        widgets = {
            'name':TextInput(attrs={'class':'input','placeholder':'Name&Surname'}),
            'subject':TextInput(attrs={'class':'input','placeholder':'Subject'}),
            'email':EmailField(attrs={'class':'input','placeholder':'Email address'}),
            'message':TextArea(attrs={'class':'input','placeholder':'Your message','rows':'5'}),
        }
class FAQ(models.Model):
    STATUS = (
        ('True','Mavjud'),
        ('False','Mavjud emas'),
    )
    lang = models.CharField(max_length=20,choices=langlist,blank=True,null=True)
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = RichTextUploadingField()
    status = models.CharField(max_length=20,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class Post(models.Model):
    title = models.CharField(blank=True, max_length=255)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    detail = RichTextUploadingField()
    image = models.ImageField(upload_to='images',blank=True)
    author = models.CharField(blank=True, max_length=255)
    create_at = models.DateTimeField(auto_now_add=True) 
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    
class License(models.Model):
    title = models.CharField(blank=True, max_length=255)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    detail = RichTextUploadingField()
    image = models.ImageField(upload_to='images',blank=True)
    create_at = models.DateTimeField(auto_now_add=True) 
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50">'.format(self.image.url))
    image_tag.short_description = 'Image'

class PostImages(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='images', blank=True)
    def __str__(self):
        return self.title

class LicenseImages(models.Model):
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='images', blank=True)
    def __str__(self):
        return self.title
