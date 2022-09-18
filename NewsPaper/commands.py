from django.contrib.auth.models import User

from NewsPaper.news.models import Author, Category, Post, PostCategory, Comment


# Создание пользователей

Alex_user = User.objects.create_user(username='Alex', email='Alex@gmail.com', password='Alex123')
Mike_user = User.objects.create_user(username='Mike', email='Mike@gmail.com', password='Mike123')

# Создание объектов

Alex = Author.objects.create(user = Alex_user)
Mike = Author.objects.create(user = Mike_user)

# Создание категорий

cat_music = Category.objects.create(name='Музыка')
cat_sport = Category.objects.create(name='Спорт')
cat_politics = Category.objects.create(name='Политика')
cat_cinema = Category.objects.create(name='Кино')

# Создание статей и новостей

article_Alex = Post.objects.create(author = Alex, post_info = Post.article, title = 'статья о музыке', text = 'о музыке')
article_Mike = Post.objects.create(author = Mike, post_info = Post.article, title = 'статья про кино', text = 'про кино')
news_Alex = Post.objects.create(author = Alex, post_info = Post.news, title = 'новости спорта', text = 'о спорте')
news_Mike = Post.objects.create(author = Mike, post_info = Post.news, title = 'новости политики', text = 'о политике')

# Присвоение категорий

PostCategory.objects.create(post = article_Alex, category = cat_music)
PostCategory.objects.create(post = article_Mike, category = cat_cinema)
PostCategory.objects.create(post = news_Alex, category = cat_sport)
PostCategory.objects.create(post = news_Mike, category = cat_politics)

# Создание комментариев

comment1 = Comment.objects.create(post = article_Alex, user = Mike.user, text = 'Коммент №1')
comment2 = Comment.objects.create(post = article_Mike, user = Alex.user, text = 'Коммент №2')
comment3 = Comment.objects.create(post = news_Alex, user = Mike.user, text = 'Коммент №3')
comment4 = Comment.objects.create(post = news_Mike, user = Alex.user, text = 'Коммент №4')

# Подсчет рейтинга

rating_Alex = (sum([post.rating*3 for post in Post.objects.filter(author=Alex)])+ sum([comment.rating for comment in Comment.objects.filter(user=Alex.user)])+ sum([comment.rating for comment in Comment.objects.filter(post__author=Alex)]))
Alex.update_rating(rating_Alex)

rating_Mike = (sum([post.rating*3 for post in Post.objects.filter(author=Mike)])+ sum([comment.rating for comment in Comment.objects.filter(user=Mike.user)])+ sum([comment.rating for comment in Comment.objects.filter(post__author=Mike)]))
Mike.update_rating(rating_Mike)


# чуток рейтинга

rating_Alex = 10
rating_Mike =15

# Лучший автор

best_author = Author.objects.all().order_by('-rating')[0]
print("Лучший автор")
print("username:", best_author.user.username)
print("Рейтинг:", best_author.rating)
print("")

# Лучшая статья

best_article = Post.objects.filter(post_info=Post.article).order_by('-rating')[0]
print("Лучшая статья")
print("Дата:", best_article.created)
print("Автор:", best_article.author.user.username)
print("Рейтинг:", best_article.rating)
print("Заголовок:", best_article.title)
print("Превью:", best_article.preview())
print("")

# Печать комментариев

print("Комментарии к ней")
for comment in Comment.objects.filter(post=best_article):
    print("Дата:", comment.created)
    print("Автор:", comment.user.username)
    print("Рейтинг:", comment.rating)
    print("Комментарий:", comment.text)
    print("")