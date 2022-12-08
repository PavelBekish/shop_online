from django.db import models
from django.urls import reverse


class CategoryGroup(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='CategoryGroup/%Y/%m/%d', blank=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Группа категории'
        verbose_name_plural = 'Группы категорий'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('category_group', kwargs={'category_group_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    category_group = models.ForeignKey(CategoryGroup, related_name='categories', on_delete=models.PROTECT, default=1)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug, 'category_group_slug': self.category_group.slug})


class Manufacturer(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='manufacturer/%Y/%m/%d', blank=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT)
    category_group = models.ForeignKey(CategoryGroup, related_name='products', on_delete=models.PROTECT)
    manufacturer = models.ForeignKey(Manufacturer, related_name='products', on_delete=models.PROTECT)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        index_together = (('id', 'slug'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})


