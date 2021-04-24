import re
from urllib.parse import urlparse
from urllib.parse import urldefrag # for removing fragments form url
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer

longest_file_len = 0;

def scraper(url, resp):

    # create if files doesn't exist
    # otherwise write into files the url, context and longest 
    # text file in each appropriate file
    # using with automatically closese all files after the with statement
    with open("url.txt", "a", encoding='utf-8') as url_file, open("content.txt", "a", encoding='utf-8') as content_file, open("longestpage.txt", "a", encoding='utf-8') as longest_file:

        if is_valid(url) and (resp.status == 200 or resp.status == 201 or resp.status == 202):
            url_file.write(url+'\n')
            html_content = resp.raw_response.content
            tokens = tokenize(html_content)

            content_file.write("\n".join(tokens))

            tokens_length = len(tokens)
            if longest_file_len < tokens_length:
                lonest_file_len = tokens_length
                longest_file.write(longest_file_len)


	links = extract_next_links(url, resp)
	return [link for link in links if is_valid(link)]

### **************************** ###
### *** CURRENTLY INCOMPLETE *** ###
### **************************** ###
def extract_next_links(url, resp):
    extracted_links = list();

    #find new links

    # remove fragments

    # remove links visited 


    # remove duplicates



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

        # check if its a calendar, needs implementation



        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

def tokenize(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text("|")

    toReturn = list()

    # filter out words that are noise i.e. menu bar items (here assuming menu bar items are less than 15 character count)
    for item in text.split("|"):
        if len(item) > 15:
            toReturn.append(item)

    tokenizer = RegexpTokenizer(r'\w+')
    toReturn = tokenizer.tokenize(toReturn)
    return toReturn


