from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Post
from django.utils.crypto import get_random_string

def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + get_random_string(length=4)
    return unique_slug

@receiver(post_save, sender= Post)
def add_slug(sender, instance, created, **kwargs) : 
    if (instance and not instance.slug) : 
        slug = slugify(instance.title)
        instance.slug = unique_slugify(instance, slug)
        instance.save()
