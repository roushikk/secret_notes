import base64
import os

import nanoid
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.db import models
from django.shortcuts import reverse


def generate_slug():
    return nanoid.generate(size=12)


class Note(models.Model):
    slug = models.SlugField(default=generate_slug, unique=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    salt = models.CharField(max_length=32, blank=True, null=True)
    allowed_reads = models.IntegerField(default=1)
    times_read = models.IntegerField(default=0)
    display_confirmation = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note', kwargs={'slug': self.slug})

    def encrypt_content(self, password):
        self.salt = os.urandom(16).hex()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=bytes.fromhex(self.salt),
            iterations=390000
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

        f = Fernet(key)
        self.content = f.encrypt(self.content.encode()).decode()

    def decrypt_content(self, password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=bytes.fromhex(self.salt),
            iterations=390000
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

        f = Fernet(key)

        try:
            content = f.decrypt(self.content.encode()).decode()
            self.times_read += 1
            self.save()
        except InvalidToken:
            content = None

        return content
