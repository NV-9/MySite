from django.contrib import sitemaps
from django_hosts.resolvers import reverse as host_reverse
from django_hosts.resolvers import reverse_host
from django.conf import settings

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return ["", "tutor.tutor", "tutor.calendar", "blog.blog", ]

    def location(self, item):
        if item == "":
            return "home"
        return item
    
    def _urls(self, page, protocol, domain):
        urls = []
        latest_lastmod = None
        all_items_lastmod = True  # track if all items have a lastmod

        paginator_page = self.paginator.page(page)
        for item in paginator_page.object_list:
            if "." in item:
                host, name = item.split(".")
                try:
                    pathway = host_reverse(name, host = host)
                except Exception as e:
                    print(e)
                    host_path = reverse_host(host)
                    pathway = f"{host_path}/{name}"
                pathway = pathway[2:] if "//" in pathway else pathway
                loc = f"{protocol}://{pathway}"
            else: 
                pathway = self._location(item)
                domain = reverse_host("www") 
                loc = f"{protocol}://{domain}/{pathway}"
            priority = self._get("priority", item)
            lastmod = self._get("lastmod", item)

            if all_items_lastmod:
                all_items_lastmod = lastmod is not None
                if all_items_lastmod and (
                    latest_lastmod is None or lastmod > latest_lastmod
                ):
                    latest_lastmod = lastmod

            url_info = {
                "item": item,
                "location": loc,
                "lastmod": lastmod,
                "changefreq": self._get("changefreq", item),
                "priority": str(priority if priority is not None else ""),
                "alternates": [],
            }

            if self.i18n and self.alternates:
                item_languages = self.get_languages_for_item(item[0])
                for lang_code in item_languages:
                    loc = f"{protocol}://{domain}{self._location(item, lang_code)}"
                    url_info["alternates"].append(
                        {
                            "location": loc,
                            "lang_code": lang_code,
                        }
                    )
                if self.x_default and settings.LANGUAGE_CODE in item_languages:
                    lang_code = settings.LANGUAGE_CODE
                    loc = f"{protocol}://{domain}{self._location(item, lang_code)}"
                    loc = loc.replace(f"/{lang_code}/", "/", 1)
                    url_info["alternates"].append(
                        {
                            "location": loc,
                            "lang_code": "x-default",
                        }
                    )

            urls.append(url_info)

        if all_items_lastmod and latest_lastmod:
            self.latest_lastmod = latest_lastmod

        return urls
    