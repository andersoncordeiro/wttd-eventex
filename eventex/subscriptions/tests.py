from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SuscribeTest(TestCase):

    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        self.assertContains(self.resp,'<form')
        """
        self.assertContains(self.resp, '<input', 2)
        self.assertContains(self.resp, 'type="text"', 2)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')
        """

    def test_csrf(self):
        self.assertContains(self.resp,'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Anderson Cordeiro', cpf='12345678901',
                    email='andersoncordeironf@gmail.com', phone='(22)998757047')

        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
               self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmacao de Inscricao'

        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'andersoncordeironf@gmail.com']

        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]
        self.assertIn('Anderson Cordeiro', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('andersoncordeironf@gmail.com', email.body)
        self.assertIn('(22)998757047', email.body)


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/',{})


    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp,'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form,SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Anderson Cordeiro',
                    cpf='12345678901',
                    email='andersoncordeironf@gmail.com',
                    phone='(22)998757047')

        response = self.client.post('/inscricao/',data, follow=True)
        self.assertContains(response, 'Inscricao Realizada com sucesso!')