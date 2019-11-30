from selenium import webdriver
import requests

def get_links(url):
    """Find all links on page at the given url.
       Return a list of all link addresses, as strings.
    """
    browser = webdriver.Chrome('C:/Users/Jade/Downloads/chromedriver')
    browser.get(url)
    links = browser.find_elements_by_tag_name('a')
    list1 = []
    for link in links:
        link.get_attribute('href')
        list1.append(link)
    print(list1)
    browser.close()
    return list1

def invalid_urls(urllist):
    invalid_urls = []
    for url in urllist:
        request = requests.head(url)
        if request.status_code == 404:
            invalid_urls.append(url)
    return invalid_urls



if __name__ == "__main__":
    urllist = get_links('https://cpske.github.io/ISP/')
    for href in urllist:
        print(f"Valid: {href}")
    invalid_url = invalid_urls(urllist)        
    for invalid in invalid_url:
        print("Invalid: " + invalid)

