    from ckeditor_uploader.fields import RichTextUploadingField
    from django.contrib.auth.models import User
    from django.db import models 
    from django.db.models import Avg,Count
    from django.forms import ModelForm
    from django.urls import reverse
    from django.utils.safestring import mark_safe
    from mptt.fields import TreeForeignKey
    from mptt.models import MPTTModel
    from home.models import Language

    class Category(MPTTModel):
        STATUS = (
            ('True','Mavjud'),
            ('False','Mavjud emas'),
        )
        parent = TreeForeignKey('self',blank=True, null=True,related_name='children', on_delete=models.CASCADE)
        title = models.CharField(max_length=50)
        keywords = models.CharField(max_length=250)
        description = models.CharField(max_length=250)
        image = models.ImageField(blank=True,upload_to='images/')
        status = models.CharField(max_length=15,choices=STATUS)
        slug = models.SlugField(null=False,unique=True)
        create_at = models.DateTimeField(auto_now_add=True)
        update_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.title
        
        class MPTTMeta:
            order_insertion_by = ['title']
        def get_absolute_url(self):
            return reverse('category_detail',kwargs={'slug':self.slug})
        
        def __str__(self):
            full_path  = [self.title]
            k = self.parent
            while k is not None:
                full_path.append(k.title)
                k = k.parent
            return '/'.join(full_path[::-1])
    class Product(models.Model):
        STATUS = (
            ('True','Mavjud'),
            ('False','Mavjud emas'),
        )
        VARIANTS = (
            ('None','None'),
            ('Size','Ulcham'),
            ('Color','Rangi'),
            ('Size-Color','Ulcham-rang'),
        )
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        title = models.CharField(max_length=150)
        keywords = models.CharField(max_length=250)
        description = models.CharField(max_length=250)
        image = models.ImageField(upload_to='images/',null=False)
        price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
        amount = models.IntegerField(default=0)
        minamount = models.IntegerField(default=1)
        variant = models.CharField(max_length=15,choices=VARIANTS,default='None')
        detail = RichTextUploadingField()
        slug = models.SlugField(null=False, unique=True)
        status = models.CharField(max_length=15,choices=STATUS)
        create_at = models.DateTimeField(auto_now_add=True)
        update_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.title
        def image_tag(self):
            if self.image.url is not None:
                return mark_safe('<img src="{}" heigth="50"/>'.format(self.image.url))
            else:
                return ""

        def get_absolute_url(self):
            return reverse('category_detail',kwargs={'slug':self.slug})

        def avaregereview(self):
            reviews = Comment.objects.filter(product=self,status='True').aggregate(avarage=Avg('rate'))
            avg = 0
            if reviews["avarage"] is not None:
                avg = float(reviews["avarage"])
            return avg 

        def countreview(self):
            reviews = Comment.objects.filter(product=self,status='True').aggregate(count=Count('id'))
            cnt = 0
            if reviews["count"] is not None:
                cnt = int(reviews["count"])
            return cnt

    class Images(models.Model):
        product = models.ForeignKey(Product,on_delete=models.CASCADE)
        title = models.CharField(max_length=50, blank=True)
        image = models.ImageField(blank=True,upload_to='images/')
        def __str__(self):
            return self.title
        
    class Comment(models.Model):
        STATUS = (
            ('New','Yangi'),
            ('True','Mavjud'),
            ('False','Mavjud emas'),

        )
        product = models.ForeignKey(Product,on_delete=models.CASCADE)
        user = models.ForeignKey(User,on_delete=models.CASCADE)
        subject = models.CharField(max_length=50,blank=True)
        comment = models.CharField(max_length=250, blank=True)
        rate = models.IntegerField(default=1)
        ip = models.CharField(max_length=50)
        status = models.CharField(max_length=15, choices=STATUS, default='New')
        create_at = models.DateTimeField(auto_now_add=True)
        update_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.subject

    class CommentForm(ModelForm):
        class Meta:
            model = Comment
            fields = ['subject','comment','rate']


    class Color(models.Model):
        name = models.CharField(max_length=50)
        code = models.CharField(max_length=50, blank=True,null=True)
        def __str__(self):
            return = self.name
        def color_tag(self):
            if self.code is not None:
                return mark_safe('<p style="background-color:{}">Color</p>'.format(self.code))
            else:
                return ""

    class Size(models.Model):
        name = models.CharField(max_length=50)
        code = models.CharField(max_length=50, blank=True,null=True)
        def __str__(self):
            return self.name

    class Variants(models.Model):
        title = models.CharField(max_length=100,blank=True,null=True)
        product = models.ForeignKey(Product,on_delete=models.CASCADE)
        color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
        size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
        image_id = models.IntegerField(blank=True,null=True, default=0)
        quantity = models.IntegerField(default=1)
        price = models.DecimalField(max_digits=12,decimal_places=2,default=0)

        def __str__(self):
            return = self.title
        
        def image(self):
            img = Images.object.get(id=self.image_id)
            if img.id is not None:
                varimage = img.image.url
            else:
                varimage = ""
            return varimage

        def image_tag(self):
            img = Images.objects.get(id=self.image_id)
            if img.id is not None:
                return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
            else:
                return ""
            
    llist = Language.objects.all()
    list1 = []
    for rs in llist:
        list1.append((rs.code,rs.name))
    langlist = (list1)

    class ProductLang(models.Model):
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        lang = models.CharField(max_length=20, choices=langlist)
        title = models.CharField(max_length=150)
        keywords = models.CharField(max_length=150)
        description = models.CharField(max_length=150)
        slug = models.SlugField(null=False,unique=True)
        detail = RichTextUploadingField()

        def get_absolute_url(self):
            return reverse('product_detail',kwargs={'slug':self.slug})

    class CategoryLang(models.Model):
        category = models.ForeignKey(Category, related_name='categorylangs',on_delete=models.CASCADE)
        lang = models.CharField(max_length=20,choices=langlist)
        title = models.CharField(max_length=150)
        keywords = models.CharField(max_length=150)
        slug = models.SlugField(null=False, unique=True)
        description = models.CharField(max_length=255)

        def get_absolute_url(self):
            return reverse('category_detail',kwargs={'slug':self.slug})