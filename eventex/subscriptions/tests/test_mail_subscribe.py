from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Anderson Cordeiro', cpf='12345678901',
                    email='andersoncordeironf@gmail.com', phone='(22)998757047')

        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmacao de Inscricao'

        self.assertEqual(expect, self.email.subject)


    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, self.email.from_email)


    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'andersoncordeironf@gmail.com']

        self.assertEqual(expect, self.email.to)


    def test_subscription_email_body(self):

        contents = ['Anderson Cordeiro',
                    '1234567890',
                    'andersoncordeironf@gmail.com',
                    '(22)998757047']

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)