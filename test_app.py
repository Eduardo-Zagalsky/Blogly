from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blog'
app.config['SQLALCHEMY_ECHO'] = False
app.config['Testing'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class BlogTest(TestCase):

    def setUp(self):
        Post.query.delete()
        User.query.delete()
        user = User(first_name="Chris", last_name="Hemsworth",
                    image_url="https://images.squarespace-cdn.com/content/v1/5c9a6f50fb18202f00c10756/c2ebb970-7d78-41dc-8ac7-b0c13d1bfc42/THOR.png?format=1000w")
        db.session.add(user)
        db.session.commit()
        self.user = user
        post = Post(title="Thor Weapons",
                    content="Mjolnir/Jonathan, Stormbreaker, and Thunderbolt", user_id=self.user.id)
        db.session.add(post)
        db.session.commit()
        self.post = post

    def tearDown(self):
        db.session.rollback()

    def test_get_root(self):
        with app.test_client() as client:
            resp = client.get("/")
            self.assertEqual(resp.status_code, 302)

    def test_get_user(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f'<a href="/users/4">Chris Hemsworth</a>', html)

    def test_add_user(self):
        with app.test_client() as client:
            new_user = {'firstName': "Idris", 'lastName': "Elba",
                        'imgUrl': "https://upload.wikimedia.org/wikipedia/commons/0/0e/Idris_Elba-4580_%28cropped%29.jpg"}
            resp = client.post("/users/new", data=new_user,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f'<a href="/users/2">Idris Elba</a>', html)

    def test_post(self):
        with app.test_client() as client:
            posts = Post.query.all()
            for post in posts:
                resp = client.get(f"/posts/{post.post_id}")
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn(
                    "<h1>Thor Weapons</h1>\n            <p>Mjolnir/Jonathan, Stormbreaker, and Thunderbolt</p>\n            <i>By Chris Hemsworth", html)

    def test_new_post(self):
        with app.test_client() as client:
            new_post = {"title": "god what a bitch",
                        "content": "my boyfriend is a bitch, he didnt support my career in front of his boss"}
            resp = client.post(
                f"/users/{self.user.id}/posts/new", data=new_post, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/posts/5">god what a bitch</a>', html)
