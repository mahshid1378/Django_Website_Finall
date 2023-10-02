from django.db import models
from django.urls import reverse
from account.models import User
from django.utils.html import format_html
from django.utils import timezone
from extensions.utils import jalali_converter
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment

# my managers
class ArticleManager(models.Manager):
	def published(self):
		return self.filter(status='p')


class CategoryManager(models.Manager):
	def active(self):
		return self.filter(status=True)


# Create your models here.
class IPAddress(models.Model):
	ip_address = models.GenericIPAddressField(verbose_name="Ip Adress")


class Category(models.Model):
	parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name="subordinate")
	title = models.CharField(max_length=200, verbose_name="Category title")
	slug = models.SlugField(max_length=100, unique=True, verbose_name="Adress Category")
	status = models.BooleanField(default=True, verbose_name="Is it displayed?")
	position = models.IntegerField(verbose_name="position")

	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categoryes"
		ordering = ['parent__id', 'position']

	def __str__(self):
		return self.title

	objects = CategoryManager()


class Article(models.Model):
	STATUS_CHOICES = (
		('d', 'Draft'),		 
		('p', "publish"),		 
		('i', "investigation"),	 
		('b', "back"),  
	)
	author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles', verbose_name="Writer")
	title = models.CharField(max_length=200, verbose_name="Title")
	slug = models.SlugField(max_length=100, unique=True, verbose_name="Address")
	category = models.ManyToManyField(Category, verbose_name="Category", related_name="articles")
	description = models.TextField(verbose_name="content")
	thumbnail = models.ImageField(upload_to="images", verbose_name="Image")
	publish = models.DateTimeField(default=timezone.now, verbose_name="time")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	is_special = models.BooleanField(default=False, verbose_name="Article special")
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="Condition")
	comments = GenericRelation(Comment)
	hits = models.ManyToManyField(IPAddress, through="ArticleHit", blank=True, related_name="hits", verbose_name="Visits")

	class Meta:
		verbose_name = "Article"
		verbose_name_plural = "Articles"
		ordering = ['-publish']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("account:home")

	def jpublish(self):
		return jalali_converter(self.publish)
	jpublish.short_description = "time"

	def thumbnail_tag(self):
		return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.thumbnail.url))
	thumbnail_tag.short_description = "Picture"	

	def category_to_str(self):
		return "، ".join([category.title for category in self.category.active()])
	category_to_str.short_description = "Grouping"

	objects = ArticleManager()


class ArticleHit(models.Model):
	article = models.ForeignKey(Article, on_delete=models.CASCADE)
	ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)