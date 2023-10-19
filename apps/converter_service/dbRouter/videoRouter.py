class VideoRouter:
    """
    A router to control all database operations on models in the
    converter service application.
    """

    # to check app`s name labels
    route_app_labels = {"converter_service"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read converter_service model go to videos_db.
        """
        # check`s if app name == auth
        if model._meta.app_label in self.route_app_labels:
            # returns access to auth db
            return "videos_db"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write converter_service model go to videos_db.
        """
        if model._meta.app_label in self.route_app_labels:
            # returns access to auth db
            return "videos_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the converter_service app is
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
        Make sure the converter_service app only appear in the
        'videos_db' database.
        """
        if app_label in self.route_app_labels:
            # returns access to auth db
            return db == "videos_db"
        return None
