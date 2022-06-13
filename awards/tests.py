from django.test import TestCase
from .models import Profile, User, Projects, Rating

# Create your tests here. 
class TestProfile(TestCase):
    def setUp(self):
        self.user = User(id=1, username='charles', password='wer2345uyq')
        self.user.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_save_user(self):
        self.user.save()

    def test_delete_user(self):
        self.user.delete() 

class ProjectsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='charles')
        self.project = Projects.objects.create(name = 'name', description = 'more stories', project_image = 'photo', url = 'url', pub_date = 'date', user = self.user)

    def test_instance(self):
        self.assertTrue(isinstance(self.project, Projects))

    def test_save_project(self):
        self.project.save_project()
        project = Projects.objects.all()
        self.assertTrue(len(project) > 0)

    def test_get_project(self):
        self.project.save()
        project = Projects.objects.all()
        self.assertTrue(len(project) > 0)

    def test_search_project(self):
        self.project.save()
        project = Projects.search_project('test')
        self.assertTrue(len(project) > 0)

    def test_delete_post(self):
        self.project.delete_project()
        post = Projects.search_project('test')
        self.assertTrue(len(post) < 1)

class RatingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='charles')
        self.project = Projects.objects.create(id=1, name='test post', project_image='photo', description='desc', user=self.user, url='http://ur.coml')
        self.rating = Rating.objects.create(id=1, design=6, usability=7, content=9, user=self.user, project=self.project)

    def test_instance(self):
        self.assertTrue(isinstance(self.rating, Rating))

    def test_save_rating(self):
        self.rating.save_rating()
        rating = Rating.objects.all()
        self.assertTrue(len(rating) > 0)

    def test_get_project_rating(self, id):
        self.rating.save()
        rating = Rating.get_ratings(project_id=id)
        self.assertTrue(len(rating) == 1)

       
        