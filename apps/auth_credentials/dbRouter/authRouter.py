class AuthRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """

    # to check app`s name labels
    route_app_labels = {"auth_credentials", "auth"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth model go to auth_db.
        """
        # check`s if app name == auth
        if model._meta.app_label in self.route_app_labels:
            # returns access to auth db
            return "auth_db"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth model go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            # returns access to auth db
            return "auth_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            # gives access to auth db
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appear in the
        'auth_db' database.
        """
        if app_label in self.route_app_labels:
            # returns access to auth db
            return db == "auth_db"
        return None
