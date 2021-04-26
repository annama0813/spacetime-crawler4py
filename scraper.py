import re
from urllib.parse import urlparse
from urllib.parse import urldefrag # for removing fragments form url
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer

def scraper(url, resp):

    # Read longestpage.txt. If the text file doesn't exist, create it and write 0 to it. Otherwise, update the current_longest variable
    current_longest = 0
    with open('longestpage.txt', 'a+') as longest_file:
        longest_file.seek(0)
        text = longest_file.readline()
        # If file is empty, write 0 to it. Otherwise update current_longest
        if text == '':
            current_longest = 0
            longest_file.write('0')
        else:
            current_longest = int(text)


    # create if files doesn't exist
    # otherwise write into files the url, context and longest 
    # text file in each appropriate file
    # using with automatically closese all files after the with statement
    with open("url.txt", "a", encoding='utf-8') as url_file, open("content.txt", "a", encoding='utf-8') as content_file, open("longestpage.txt", "a", encoding='utf-8') as longest_file:

        if is_valid(url) and (resp.status == 200 or resp.status == 201 or resp.status == 202):
            html_content = resp.raw_response.content
            tokens = tokenize(html_content)

            # Skip low information pages based on low token count
            if len(tokens) < 20 or len(tokens) > 100000:
                return []

            # Write to URL and Content files
            url_file.write(url+'\n')
            content_file.write(" ".join(tokens))
            content_file.write("\n")

            # If the current page is longer, erase the longest_file and write the new length
            if current_longest < len(tokens):
                longest_file.truncate(0)
                longest_file.write(str(len(tokens)))
                longest_file.write('\n' + url)

            links = extract_next_links(url, resp)
            return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    extracted_links = list()

    # find new links
    if resp.raw_response != None:
        soup = BeautifulSoup(resp.raw_response.content, "html.parser")
        for link in soup.findAll('a'):
            extracted_links.append(link.get('href'))

        # filter fragments
        for count, link in enumerate(extracted_links):
            extracted_links[count] = urldefrag(link)[0]
            # extracted_links[count] = urljoin(extracted_links[count],\
            #     urlparse(url).path)

        # remove links visited 
        with open("url.txt", 'r') as f:
            for line in f:
                current_link = line.rstrip('\n')
                if current_link in extracted_links:
                    extracted_links.remove(current_link)
                # if all links are visited
                if len(extracted_links) == 0:
                    return extracted_links

    # remove duplicates
    extracted_links = set(extracted_links)

    return extracted_links

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        accetable_domains = [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu", 
        ".stat.uci.edu", "today.uci.edu"]
        if not any(domain in parsed.netloc for domain in accetable_domains):
        	return False

        if "today.uci.edu" in parsed.netloc:
            if "department/information_computer_sciences" not in parsed.path:
                return False

        # check for trap
        if check_trap(url):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|ppsx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|z)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

# checks string (url) if it has the specific word
# since we know those can be traps for crawlers
# one specific website is https://wics.ics.uci.edu/events which is a calendar
def check_trap(string_to_check):
    if (re.search(r'(\/pdf\/)',string_to_check.lower())):
        return True

    if (re.search(r'calendar|events|share|replytocom',string_to_check.lower())):
        return True

    return False


def tokenize(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text("|")

    words = list()

    # filter out words that are noise i.e. menu bar items (here assuming menu bar items are less than 15 character count)
    for item in text.split("|"):
        if len(item) > 15:
            words.append(item)
    
    words = ' '.join(words)
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(words)

    toReturn = list()

    for item in words:
        try:
            item.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            continue
        else:
            if len(item) > 1:
                toReturn.append(item.lower())

    return toReturn


