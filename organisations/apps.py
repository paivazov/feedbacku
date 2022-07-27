from django.apps import AppConfig


class OrganisationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'organisations'

    def ready(self):
        # the module is imported in order to initialize signal handlers
        import organisations.signal_handlers  # noqa: F401
