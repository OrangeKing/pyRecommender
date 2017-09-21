from django.test import TestCase
from maps.models import Post
from time import strftime
from django.contrib.auth.models import User
from .forms import *


class PostModelTest(TestCase):
    TIMESTAMP_AUTHOR = strftime("U%d%m%y%H%M%S")
    TIMESTAMP_TITLE = strftime("T%d%m%y%H%M%S")
    CONTENT = """Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer
    took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries,
    but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with
    the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software
    like Aldus PageMaker including versions of Lorem Ipsum."""
    LOCATION = "Warsaw"
    SLUG = "Mobica"

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(cls.TIMESTAMP_AUTHOR)
        test_id = test_user.id
        Post.objects.create(author_id=test_id, title=cls.TIMESTAMP_TITLE,
                            contents=cls.CONTENT, location=cls.LOCATION, slug=cls.SLUG)

    def test_author_id_value(self):
        author = User.objects.get(username=self.TIMESTAMP_AUTHOR)
        expected_id_value = author.id
        self.assertEquals(expected_id_value, 1)

    def test_title_value(self):
        post = Post.objects.get(id=1)
        expected_title_value = post.title
        self.assertEquals(expected_title_value, self.TIMESTAMP_TITLE)

    def test_title_label_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_was_published_recently(self):
        post = Post.objects.get(id=1)
        self.assertEquals(post.was_published_recently(), True)

    def test_get_contents_preview(self):
        post = Post.objects.get(id=1)
        short_contents = post.get_contents_preview()
        self.assertEquals(len(post.contents) > len(short_contents), True)

    def test_to_str(self):
        post = Post.objects.get(id=1)
        title = post.title
        self.assertEquals(title, post.__str__())

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        url = post.get_absolute_url()
        self.assertEquals(url, "/posts/{}/".format(self.SLUG))


class PostViewTest(TestCase):
    TIMESTAMP_AUTHOR = strftime("U%d%m%y%H%M%S")
    TIMESTAMP_TITLE = strftime("T%d%m%y%H%M%S")
    CONTENT = """Short test content value"""
    LOCATION = "Warsaw"
    SLUG = "Mobica"

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(cls.TIMESTAMP_AUTHOR)
        test_id = test_user.id
        Post.objects.create(author_id=test_id, title=cls.TIMESTAMP_TITLE,
                            contents=cls.CONTENT, location=cls.LOCATION, slug=cls.SLUG)

    def test_call_view_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_call_view_about(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_call_view_contact(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_call_view_denies_anonymous(self):
        response = self.client.get('/posts/add/')
        self.assertTemplateNotUsed(response)


    def test_call_view_loads(self):
        self.client.login(username=self.TIMESTAMP_AUTHOR, password=None)  # defined in fixture or with factory in setUp()
        response = self.client.get('/posts/?q={TIMESTAMP_AUTHOR}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_list.html')

    def test_call_view_fails_blank(self):
        self.client.login(username='user', password='test')
        response = self.client.post('/nonexistent')
        self.assertEqual(response.status_code, 404)


class PostValidatorsTest(TestCase):
    TIMESTAMP_AUTHOR = strftime("U%d%m%y%H%M%S")
    TIMESTAMP_TITLE = strftime("T%d%m%y%H%M%S")
    CONTENT = """Short test content value"""
    LOCATION = "Warsaw"
    SLUG = "Mobica"

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(cls.TIMESTAMP_AUTHOR)
        test_id = test_user.id
        Post.objects.create(author_id=test_id, title=cls.TIMESTAMP_TITLE,
                            contents=cls.CONTENT, location=cls.LOCATION, slug=cls.SLUG)

    def test_validate_post(self):
        author = User.objects.get(username=self.TIMESTAMP_AUTHOR)
        author_id = author.id
        valid_post = Post.objects.create(author_id=author_id)
        test_post_form = PostAddForm(instance=valid_post)
        self.assertEqual(test_post_form.is_valid(), False) # No data has been supplied yet.
        test_post_form = PostAddForm({'title': self.TIMESTAMP_AUTHOR, 'contents': "password", 'location': "Warsaw" }, instance=valid_post)
        self.assertEqual(test_post_form.is_valid(), True) # Now that you have given it data, it can validate.
