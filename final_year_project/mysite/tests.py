
from django.test import TestCase
from django.urls import reverse
from django.test import TestCase
from .models import Post, Article, Event, Donation, BarberTile, LikedTag, Comment, Image, User

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
        Post.objects.create(artist="Test Artist",content="Test Content")

        
    def test(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        #self.assertIn(posts, response.content)

class most_liked_posts(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        
    def test(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('home_like')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        
class recommended_posts(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        
    def test(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('home_recommended')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        
        
class news(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        
    def test(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('news')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        
class events(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        
    def test(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('events')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        
class donate(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        
    def test(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('donate')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        
class donate_tiles(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        
    def test(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('donate_tiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        
class donate_history(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        
    def test(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('donate_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        
class liked_posts(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create_user(username='testuser1')
        test_user.save()
        
    def test(self):
        self.client.force_login(User.objects.get(id=1))
        url = reverse('liked_posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
     
         
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
        
    def test_comment_delete(self):
        this_post = Post.objects.get(id=1)
        comment = Comment.objects.get(id=1)
        this_post.comments.add(comment)
        comment.delete()
        
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
