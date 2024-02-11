import re
import sys
import urllib.request


def load_web_page(url):
    print("URL: {}".format(url))
    print("----------------------------------------")

    web_page = urllib.request.urlopen(url)
    decoded_page = web_page.read().decode(web_page.headers.get_content_charset())

    links_to_other_pages = set(re.findall(r'href="(https?://.*?)"', decoded_page))
    print()
    print("Total unique links to other pages: {}".format(len(links_to_other_pages)))
    print("----------------------------------------")
    for link in sorted(links_to_other_pages):
        print(link)

    hosts_list = re.findall(r'https?://(.+?)/.*', "\n".join(links_to_other_pages))
    unique_hosts = set(hosts_list)

    print()
    print("Total unique hosts: {}".format(len(unique_hosts)))
    print("----------------------------------------")
    for host in sorted(unique_hosts):
        print(host)

    hosts_dict = {}

    for host in hosts_list:
        if host not in hosts_dict:
            hosts_dict[host] = 0

        hosts_dict[host] += 1

    print()
    print("Total occurrences of hosts")
    print("----------------------------------------")

    for hostname, occurrences in sorted(hosts_dict.items(), key=lambda item: -item[1]):
        print("{} {}".format(hostname, occurrences))

    emails = set(re.findall(r'\b[A-Za-z\d._%+-]+@[A-Za-z\d.-]+\.[A-Z|a-z]{2,}\b', decoded_page))
    print()
    print("Total unique emails: {}".format(len(emails)))
    print("----------------------------------------")
    for email in sorted(emails):
        print(email)

    images = set(re.findall(r'<img[^>]+src="([^">]+)"', decoded_page))
    print()
    print("Total unique images: {}".format(len(images)))
    print("----------------------------------------")
    for image in sorted(images):
        print(image)


def main():
    url = sys.argv[1]
    load_web_page(url)


if __name__ == "__main__":
    main()
