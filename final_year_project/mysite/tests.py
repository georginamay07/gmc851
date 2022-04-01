
from queue import Empty
from django.test import TestCase
from django.urls import reverse
from django.test import TestCase
from pyparsing import empty
from .models import Post, Article, Event, Donation, BarberTile, LikedTag, Comment, Image, User
from django.utils import timezone
from django.db.models.query_utils import Q
from django.db.models import Count

from django.contrib.auth import login, authenticate, logout


#models test
class PostModelTest(TestCase):
    
    def setUp(self):
        Post.objects.create(artist="Test Artist",content="Test Content")
        
    def test_artist(self):
        post = Post.objects.get(id=1)
        field_label = post.artist
        self.assertEqual(field_label, 'Test Artist')
            
    def test_content(self):
        post = Post.objects.get(id=1)
        field_label = post.content
        self.assertEqual(field_label, 'Test Content') 

class DonationModelTest(TestCase):
    
    def setUp(self):
        Donation.objects.create(amount=5,first_name="Test Name", last_name="Last Name")
        
    def test_amount(self):
        donation = Donation.objects.get(id=1)
        field_label = donation.amount
        self.assertEqual(field_label, 5)
            
    def test_fname(self):
        donation = Donation.objects.get(id=1)
        field_label = donation.first_name
        self.assertEqual(field_label, 'Test Name') 
        
    def test_lname(self):
        donation = Donation.objects.get(id=1)
        field_label = donation.last_name
        self.assertEqual(field_label, 'Last Name') 
        
class BarberTileTest(TestCase):
    
    def setUp(self):
        BarberTile.objects.create(amount=5,first_name="Test Name", last_name="Last Name")
        
    def test_amount(self):
        tile = BarberTile.objects.get(id=1)
        field_label = tile.amount
        self.assertEqual(field_label, 5)
            
    def test_fname(self):
        tile = BarberTile.objects.get(id=1)
        field_label = tile.first_name
        self.assertEqual(field_label, 'Test Name') 
        
    def test_lname(self):
        tile = BarberTile.objects.get(id=1)
        field_label = tile.last_name
        self.assertEqual(field_label, 'Last Name') 
        
class LikedTagTest(TestCase):
    
    def setUp(self):
        liked_tags_instance = LikedTag.objects.create()
        liked_tags_instance.tags.add('test')
        liked_tags_instance.tags.add('test1')
        liked_tags_instance.tags.add('test2')

    def test_tags(self):
        tags = LikedTag.objects.get(id=1).tags.all()
        i=0
        tag_list=[]
        for item in tags:
            tag = str(tags[i])
            tag_list.append(tag)
            i+=1        
        self.assertEqual(tag_list, ['test','test1','test2'])

#views test

class published_posts(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        Post.objects.create(artist="Test Artist",content="Test Content", published_on=timezone.now(), cover_image = 'test.jpg')
        Post.objects.create(artist='Test Artist 1', content ="Test Content 1", published_on=timezone.now(),cover_image = 'test.jpg')
        Post.objects.create(artist="Test Artist 2", content = "Test Content 2", published_on=timezone.now(),cover_image = 'test.jpg')
        
    def test_post_filter_published(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        posts = Post.objects.filter(published_on__lte=timezone.now()).order_by('published_on')
        self.assertQuerysetEqual(posts, Post.objects.all())

        
class most_liked_posts(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        Post.objects.create(artist="Test Artist",content="Test Content", published_on=timezone.now(), cover_image = 'test.jpg', number_of_likes=1)
        Post.objects.create(artist='Test Artist 1', content ="Test Content 1", published_on=timezone.now(),cover_image = 'test.jpg', number_of_likes=2)
        Post.objects.create(artist="Test Artist 2", content = "Test Content 2", published_on=timezone.now(),cover_image = 'test.jpg', number_of_likes=3)
        
    def test_post_filter_most_liked(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('home_like')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        posts = Post.objects.filter(published_on__lte=timezone.now()).order_by('-number_of_likes')
        self.assertEqual(posts[0].number_of_likes, 3)
        self.assertEqual(posts[1].number_of_likes, 2)
        self.assertEqual(posts[2].number_of_likes, 1)
    
        
class recommended_posts(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        post1 = Post.objects.create(artist="Test Artist",content="Test Content",cover_image = 'test.jpg')
        post2 = Post.objects.create(artist='Test Artist 1', content ="Test Content 1",cover_image = 'test.jpg')
        post3 = Post.objects.create(artist="Test Artist 2", content = "Test Content 2",cover_image = 'test.jpg')
        post1.tags.add('test','other')
        post2.tags.add('test1','other')
        post3.tags.add('test2','other')
        liked_tags_instance = LikedTag.objects.create(user_id = test_user)
        liked_tags_instance.tags.add('test1')
                
    def test_recommended_filtering(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('home_recommended')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        user = User.objects.get(id=1)
        user_tags = LikedTag.objects.get(user_id=user).tags.all()
        tag_list=[]
        i = 0
        for item in user_tags:
            tag = str(user_tags[i])
            tag_list.append(tag)
            i+=1
        posts = Post.objects.filter(~Q(like=user)).annotate(similar_tags=Count('tags', filter=Q(tags__in=user_tags))).order_by('-similar_tags')
        self.assertEqual(posts[0].artist, 'Test Artist 1')
        self.assertEqual(posts[1].artist, 'Test Artist')
        self.assertEqual(posts[2].artist, 'Test Artist 2')
        
class events_posts(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        Event.objects.create(title="Test Title",content="Test Content", date = timezone.now(),cover_image = 'test.jpg')
        Event.objects.create(title='Test Title 1', content ="Test Content 1", date = timezone.now(),cover_image = 'test.jpg')
        Event.objects.create(title="Test Title 2", content = "Test Content 2", date = timezone.now(),cover_image = 'test.jpg')
        
    def test_events_filter(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('events')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        events = Event.objects.order_by('date')
        self.assertQuerysetEqual(events, Event.objects.all())            

class news_posts(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        Article.objects.create(title="Test Title",content="Test Content", published_on=timezone.now(), cover_image = 'test.jpg')
        Article.objects.create(title='Test Title 1', content ="Test Content 1", published_on=timezone.now(),cover_image = 'test.jpg')
        Article.objects.create(title="Test Title 2", content = "Test Content 2", published_on=timezone.now(),cover_image = 'test.jpg')
        
    def test_news_filter(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('news')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        news = Article.objects.filter(published_on__lte=timezone.now()).order_by('published_on')
        self.assertQuerysetEqual(news, Article.objects.all()) 

class donate(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1', first_name = "Test Name", last_name = "Last Name")
        test_user.save()
        
    def test(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('donate')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        user = User.objects.get(id=1)
        json1 = {'amount':'1', 'fave_image':'test_image.jpg'}
        json2 = {'amount':'5', 'fave_image':''}
        json3 = {'amount':'10', 'fave_image':'test_image1.jpg'}
        if json1['amount'] == '1':
                Donation.objects.create(amount=1, user_id=user, first_name=user.first_name, last_name=user.last_name)
                if json1['fave_image'] != '':
                    url = "images/tiles/" + json1['fave_image']
                    BarberTile.objects.create(fave_image=url,first_name=user.first_name, last_name=user.last_name, amount=1)

        if json1['amount'] == '5':
            Donation.objects.create(amount=5, user_id=user, first_name=user.first_name, last_name=user.last_name)
            if json1['fave_image'] != '':
                url = "images/tiles/" + json1['fave_image']
                BarberTile.objects.create(fave_image=url,first_name=user.first_name, last_name=user.last_name, amount=5)

        if json1['amount'] == '10':
            Donation.objects.create(amount=10, user_id=user, first_name=user.first_name, last_name=user.last_name) 
            if json1['fave_image'] != '':
                url = "images/tiles/" + json1['fave_image']
                BarberTile.objects.create(fave_image=url,first_name=user.first_name, last_name=user.last_name, amount=10)
        if json2['amount'] == '1':
                Donation.objects.create(amount=1, user_id=user, first_name=user.first_name, last_name=user.last_name)
                if json2['fave_image'] != '':
                    url = "images/tiles/" + json2['fave_image']
                    BarberTile.objects.create(fave_image=url,first_name=user.first_name, last_name=user.last_name, amount=1)

        if json2['amount'] == '5':
            Donation.objects.create(amount=5, user_id=user, first_name=user.first_name, last_name=user.last_name)
            if json2['fave_image'] != '':
                url = "images/tiles/" + json2['fave_image']
                BarberTile.objects.create(fave_image=url,first_name=user.first_name, last_name=user.last_name, amount=5)

        if json2['amount'] == '10':
            Donation.objects.create(amount=10, user_id=user, first_name=user.first_name, last_name=user.last_name) 
            if json2['fave_image'] != '':
                url = "images/tiles/" + json2['fave_image']
                BarberTile.objects.create(fave_image=url,first_name=user.first_name, last_name=user.last_name, amount=10)    
        if json3['amount'] == '1':
                Donation.objects.create(amount=1, user_id=user, first_name=user.first_name, last_name=user.last_name)
                if json3['fave_image'] != '':
                    url = "images/tiles/" + json3['fave_image']
                    BarberTile.objects.create(fave_image=url,first_name=user.first_name, last_name=user.last_name, amount=1)

        if json3['amount'] == '5':
            Donation.objects.create(amount=5, user_id=user, first_name=user.first_name, last_name=user.last_name)
            if json3['fave_image'] != '':
                url = "images/tiles/" + json3['fave_image']
                BarberTile.objects.create(fave_image=url,first_name=user.first_name, last_name=user.last_name, amount=5)

        if json3['amount'] == '10':
            Donation.objects.create(amount=10, user_id=user, first_name=user.first_name, last_name=user.last_name) 
            if json3['fave_image'] != '':
                url = "images/tiles/" + json3['fave_image']
                BarberTile.objects.create(fave_image=url,first_name=user.first_name, last_name=user.last_name, amount=10)
        tiles = BarberTile.objects.prefetch_related().all()
        self.assertEqual(tiles[0].amount, 1)
        self.assertEqual(tiles[1].amount, 10)
        self.assertEqual(tiles[0].fave_image, "images/tiles/test_image.jpg")
        self.assertEqual(tiles[1].fave_image, "images/tiles/test_image1.jpg")       
        
class donate_history(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        Donation.objects.create(user_id = test_user, amount="1", first_name = "Test Name", last_name = "Last Name",date=timezone.now())
        Donation.objects.create(user_id = test_user, amount="5", first_name = "Test Name 1", last_name = "Last Name 1",date=timezone.now())
        Donation.objects.create(user_id = test_user, amount="10", first_name = "Test Name 2", last_name = "Last Name 2",date=timezone.now())

        
    def test_donation_history(self):
        self.client.force_login(User.objects.get(id=1))
        user = User.objects.get(id=1)
        url = reverse('donate_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        donations = Donation.objects.prefetch_related().all()
        for i in donations:
            user_donations = Donation.objects.filter(user_id = user)
        self.assertEqual(user_donations[0].amount, 1)
        self.assertEqual(user_donations[1].amount, 5)
        self.assertEqual(user_donations[2].amount, 10)

class liked_posts(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        post1 = Post.objects.create(artist="Test Artist",content="Test Content",cover_image = 'test.jpg')
        post2 = Post.objects.create(artist='Test Artist 1', content ="Test Content 1",cover_image = 'test.jpg')
        post3 = Post.objects.create(artist="Test Artist 2", content = "Test Content 2",cover_image = 'test.jpg')
        post1.like.add(test_user)
        post3.like.add(test_user)
        
    def test(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('liked_posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        user = User.objects.get(id=1)
        posts = Post.objects.all()
        liked_posts = None
        for i in posts:
            liked_posts = Post.objects.filter(like = user)
        self.assertEqual(liked_posts[0].artist, 'Test Artist')
        self.assertEqual(liked_posts[1].artist, 'Test Artist 2')
     
class test_news_functions(TestCase):
    
    def setUp(self):
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        Article.objects.create(title="Test Article",content="Test Content")
        Comment.objects.create(comment='test comment', user_id = test_user)

    def test_news_comment(self):
        this_article = Article.objects.get(id=1)
        comment = Comment.objects.get(id=1)
        this_article.comments.add(comment)
        self.assertEqual(this_article.comments.all()[0], comment)
        
    def test_news_comment_delete(self):
        this_article = Article.objects.get(id=1)
        comment = Comment.objects.get(id=1)
        this_article.comments.add(comment)
        comment.delete()
        self.assertQuerysetEqual(this_article.comments.all(), Comment.objects.all())  
       
class test_post_functions(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        Post.objects.create(artist="Test Artist",content="Test Content")
        Comment.objects.create(comment='test comment', user_id = test_user)

    def test_comment(self):
        this_post = Post.objects.get(id=1)
        comment = Comment.objects.get(id=1)
        this_post.comments.add(comment)
        self.assertEqual(this_post.comments.all()[0], comment)
        
    def test_comment_delete(self):
        this_post = Post.objects.get(id=1)
        comment = Comment.objects.get(id=1)
        this_post.comments.add(comment)
        comment.delete()
        self.assertQuerysetEqual(this_post.comments.all(), Comment.objects.all())
        
    def test_like_post(self):
        this_post = Post.objects.get(id=1)
        user = User.objects.get(id=1)
        this_post.number_of_likes += 1
        this_post.save()
        this_post.like.add(user)
        self.assertEqual(this_post.like.all()[0], user)
        self.assertEqual(this_post.number_of_likes, 1)

    def test_unlike_post(self):
        this_post = Post.objects.get(id=1)
        user = User.objects.get(id=1)
        this_post.number_of_likes += 1
        this_post.save()
        this_post.like.add(user)
        self.assertEqual(this_post.like.all()[0], user)
        self.assertEqual(this_post.number_of_likes, 1)
        this_post.number_of_likes -= 1
        this_post.save()
        this_post.like.remove(user)
        self.assertQuerysetEqual(this_post.like.all(), this_post.like.none())
        self.assertEqual(this_post.number_of_likes, 0)
        
    def test_liked_tags(self):
        this_post = Post.objects.get(id=1)
        user = User.objects.get(id=1)
        this_post.tags.add('test')
        this_post.tags.add('test1')
        this_post.tags.add('test2')
        post_tags = this_post.tags.all()
        instance = LikedTag.objects.create(user_id = user)
        i = 0
        for item in post_tags:
            tag = str(post_tags[i])
            instance.tags.add(tag)
            i+=1
        a = 0
        liked_tags = LikedTag.objects.get(id=1).tags.all()
        liked_tag_list=[]
        for item in liked_tags:
            tag = str(liked_tags[a])
            liked_tag_list.append(tag)
            a+=1   
        x = 0
        post_tag_list=[]
        for item in post_tags:
            tag = str(post_tags[x])
            post_tag_list.append(tag)
            x+=1   
        self.assertEqual(post_tag_list, liked_tag_list)

    def test_unliked_tags(self):
        this_post = Post.objects.get(id=1)
        user = User.objects.get(id=1)
        this_post.tags.add('test')
        this_post.tags.add('test1')
        this_post.tags.add('test2')
        post_tags = this_post.tags.all()
        instance = LikedTag.objects.create(user_id = user)
        i = 0
        for item in post_tags:
            tag = str(post_tags[i])
            instance.tags.add(tag)
            i+=1
        a = 0
        liked_tags = LikedTag.objects.get(id=1).tags.all()
        liked_tag_list=[]
        for item in liked_tags:
            tag = str(liked_tags[a])
            liked_tag_list.append(tag)
            a+=1   
        x = 0
        post_tag_list=[]
        for item in post_tags:
            tag = str(post_tags[x])
            post_tag_list.append(tag)
            x+=1   
        self.assertEqual(post_tag_list, liked_tag_list)
        y = 0
        for item in post_tags:
            tag = str(post_tags[y])
            instance.tags.remove(tag)
            y+=1 
        p=0
        liked_tags1 = LikedTag.objects.get(id=1).tags.all()
        liked_tag_list1=[]
        for item in liked_tags1:
            tag = str(liked_tags1[p])
            liked_tag_list1.append(tag)
            p+=1  
        self.assertNotEqual(post_tag_list, liked_tag_list1)
