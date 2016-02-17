from django.test import TestCase
from work_projects.models import Asset, Project, ProjectType


class ProjectTestCase(TestCase):
    def _project_is_design_related(self):
        """Projects are correctly identified as being design related."""

        t = ProjectType(name="Background Design")
        t.save()
        s = Project(name="My BG Design")
        s.type = t
        self.assertTrue(s.is_design_related(),
                        "Project is correctly identified as design related.")

    def _project_is_not_design_related(self):
        """Projects are correctly identified as being not design related."""

        t = ProjectType(name="Web Development")
        t.save()
        s = Project(name="My Web App")
        s.type = t
        self.assertFalse(s.is_design_related(),
                         "Project is correctly identified as not design related.")


class AssetTestCase(TestCase):
    """Tests Asset object methods"""

    def test_parent_name_of_uninitialized_parent_object(self):
        """Asset objects' parent_name routine doesn't throw error when parent object is not set."""

        a = Asset()
        self.assertEquals(a.parent_name(), "", "Parent name of uninitialized parent object returns empty string.")
