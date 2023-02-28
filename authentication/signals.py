def initialize_groups(sender, **kwargs):
    from django.apps import apps
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    _, created = Group.objects.get_or_create(name='Faculty')
    _, created = Group.objects.get_or_create(name='Student')