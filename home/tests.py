from django.test import TestCase, override_settings
from django.urls import reverse


TEST_STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


@override_settings(STORAGES=TEST_STORAGES)
class OurStoryPageTests(TestCase):
    def test_our_story_page_renders_with_existing_static_image(self):
        response = self.client.get(reverse("home:our_story"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Driven by service, built on trust.")
        self.assertContains(response, "home/images/showroom/fleet.png")
        self.assertNotContains(response, "home/images/car3.jpg")
