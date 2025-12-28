from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals

        # Auto-create admin user for development
        from django.db.models.signals import post_migrate
        
        def create_default_admin(sender, **kwargs):
            from django.contrib.auth.models import User
            try:
                # Check if admin exists
                if not User.objects.filter(username='admin').exists():
                    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
                    print("Default superuser 'admin' created with password 'admin'.")
                else:
                    # Optional: Ensure password is 'admin' (uncomment if you want to force reset every time)
                    # u = User.objects.get(username='admin')
                    # u.set_password('admin')
                    # u.save()
                    pass
            except Exception:
                pass 
                
        post_migrate.connect(create_default_admin, sender=self)
