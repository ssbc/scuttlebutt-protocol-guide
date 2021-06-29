import os
import html.parser
import urllib.parse
import urllib.request
import json

# Checks for broken links, preemptively saving all linked pages
# to the Internet Archive's Wayback Machine.
# Requires Python 3.

self_dir = os.path.dirname(__file__)
html_path = os.path.join(self_dir, "index.html")

def extract_links_from_html_file(path):
    class LinkExtractParser(html.parser.HTMLParser):
        def __init__(self):
            super().__init__()
            self.links = []

        def handle_starttag(self, tag, attrs):
            if tag == "a":
                for (k, v) in attrs:
                    if k == "href":
                        self.links.append(v)

    parser = LinkExtractParser()

    with open(html_path) as file:
        parser.feed(file.read())

    def is_http_link(href):
        return href.startswith("https:") or href.startswith("http:")

    # Drop duplicates, filter out non-http-links, sort
    links = list(filter(is_http_link, sorted(set(parser.links))))
    return links

def try_fetch_webpage(url):
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            return {"error": str(e.code)}
        elif hasattr(e, 'reason'):
            return {"error": e.reason}
    else:
        if response.geturl() != url:
            return {"redirect": response.geturl()}
        else:
            return {"success": True}

def get_wayback_machine_archived_page(url):
    api_url = "https://archive.org/wayback/available?url=" + url
    response = urllib.request.urlopen(api_url)
    data = json.loads(response.read())
    if "closest" in data["archived_snapshots"]:
        if data["archived_snapshots"]["closest"]["available"]:
            return data["archived_snapshots"]["closest"]["url"]
    return None

def save_in_wayback_machine(url):
    api_url = "https://web.archive.org/save/" + url
    response = urllib.request.urlopen(api_url)
    if "Content-Location" in response.info() and response.info()["Content-Location"].startswith("/web/"):
        return "https://web.archive.org" + response.info()["Content-Location"]
    return None

urls = extract_links_from_html_file(html_path)
for url in urls:
    result = try_fetch_webpage(url)

    if "success" in result:
        print("OK {}".format(url))
        if get_wayback_machine_archived_page(url) is None:
            try:
                wayback_url = save_in_wayback_machine(url)
                print("    Archived as: {}".format(wayback_url))
            except:
                pass

    elif "redirect" in result:
        print("REDIRECT {}".format(url))
        print("    Redirects to: {}".format(result["redirect"]))

    elif "error" in result:
        print("BROKEN {}".format(url))
        print("    Reason: {}".format(result["error"]))

    if "success" not in result:
        try:
            wayback_url = get_wayback_machine_archived_page(url)
            if wayback_url is not None:
                print("    Archived copy: {}".format(wayback_url))
        except:
            pass
