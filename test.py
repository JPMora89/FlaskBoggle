from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def test_get_home(self):
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form id="guess-submit-form">', resp.get_data(as_text=True))


    def test_submit_guess(self):
        with app.test_client() as client:
            resp = client.get("/")

            resp = client.post("/guess", json={
                "guess": "pepperoni",
            })

            self.assertEqual(resp.status_code, 200)
            self.assertIn(resp.json["result"], ["ok", "not-on-board"])

        with app.test_client() as client:
            resp = client.get("/")

            resp = client.post("/guess", json={
                "guess": "aslkdmlkmsdfl"
            })

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json["result"], "not-word")


    def test_post_high_score(self):
        with app.test_client() as client:
            resp = client.get("/")

            resp = client.post("/high-score", json={
                "score": 5000
            })

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json["message"], "You set the new high score with 5000")
            self.assertIsNotNone(resp.json["games_played"])