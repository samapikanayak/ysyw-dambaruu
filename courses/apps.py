from django.apps import AppConfig


class CoursesConfig(AppConfig):
    name = "courses"

    def ready(self) -> None:
        import courses.signals
