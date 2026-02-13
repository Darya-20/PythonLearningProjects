from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    """Модель, содержащая объекты всех авторов."""
    user = models.OneToOneField(User, on_delete=models.CASCADE) #cвязь «один к одному» с встроенной моделью пользователей User
    rating = models.IntegerField(default=0) #рейтинг пользователя
    
    def update_rating(self):
        """Обновляет рейтинг текущего автора"""
        rating_posts = self.post_set.aggregate(Sum('rating'))['rating__sum'] or 0 #суммарный рейтинг всех статей автора, умножается на 3
        rating_comments = self.user.comment_set.aggregate(Sum('rating'))['rating__sum'] or 0 #суммарный рейтинг всех комментариев автора
        rating_comments_posts = Comment.objects.filter(post__author=self).aggregate(Sum('rating'))['rating__sum'] or 0 #суммарный рейтинг всех комментариев к статьям автора
        self.rating = rating_posts * 3 + rating_comments + rating_comments_posts
        self.save()
        
    def __str__(self):
        return f"{self.user.username} - {self.rating}"

class Category(models.Model):
    """Категории новостей/статей."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Модель, содержащая статьи и новости, которые создают пользователи."""
    article = 'AR'
    news = 'NE'
    TYPE_POST = [
        (article, 'статья'),
        (news, 'новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING) #связь «один ко многим» с моделью Author
    categories = models.ManyToManyField(Category, through='PostCategory') #связь «многие ко многим» с моделью Category
    type = models.CharField(max_length=2, choices=TYPE_POST, default=article) #поле с выбором — «статья» или «новость»
    datetime_creation = models.DateTimeField(auto_now_add=True) #автоматически добавляемая дата и время создания
    title = models.CharField(max_length=100) #заголовок статьи/новости
    text = models.TextField() #текст статьи/новости
    rating = models.IntegerField(default=0) #рейтинг статьи/новости

    def __str__(self):
        categories_names = [category.name for category in self.categories.all()]
        return f"""{self.datetime_creation.strftime('%d.%m.%y %H:%M')} {self.get_type_display()}
{', '.join(categories_names)}
{self.title}
{self.author}
{self.preview()}"""

    def preview(self):
        return self.text[:124] + '...'
    
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
    

class PostCategory(models.Model):
    """Промежуточная модель для связи «многие ко многим» Post и Category."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE) #связь «один ко многим» с моделью Post
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #связь «один ко многим» с моделью Category


class Comment(models.Model):
    """Модель комментариев к статьям"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE) #связь «один ко многим» с моделью Post
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING) #связь «один ко многим» со встроенной моделью User
    text = models.TextField() #текст комментария
    datetime_creation = models.DateTimeField(auto_now_add=True) #дата и время создания комментария
    rating = models.IntegerField(default=0) #рейтинг комментария

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
    
    def __str__(self):
        return f'''{self.post.title} {self.datetime_creation}
{self.user.username}
{self.text}'''
