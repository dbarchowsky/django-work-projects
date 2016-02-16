from django.test import TestCase
from work_projects.models import Project, ProjectType


class ProjectTestCase(TestCase):
    def test_project_is_design_related(self):
        """Projects are correctly identified as being design related."""

        t = ProjectType(name="Background Design")
        t.save()
        s = Project(name="My BG Design")
        s.type = t
        self.assertTrue(s.is_design_related(),
                        "Project is correctly identified as design related.")

    def test_project_is_not_design_related(self):
        """Projects are correctly identified as being not design related."""

        t = ProjectType(name="Web Development")
        t.save()
        s = Project(name="My Web App")
        s.type = t
        self.assertFalse(s.is_design_related(),
                         "Project is correctly identified as not design related.")
