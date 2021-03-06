from flask_principal import Permission, RoleNeed
from .database import user_datastore, db
from app.settings import Config
# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))

def setup_permissions(app):
    with app.app_context():
        db.create_all()
        user_datastore.find_or_create_role(name='admin', description='Administrator')
        
        for admin in Config.ADMINS:
            if not user_datastore.get_user(admin):
                user_datastore.create_user(email=admin)
                user_datastore.add_role_to_user(admin, 'admin')
        db.session.commit()
    return app
