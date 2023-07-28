from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = "daily"

    def items(self):
        return ["", "privacy", "tutor", "calendar", "auth", "login", "signup"]

    def location(self, item):
        if item == "":
            return reverse("home")
        return reverse(item)
