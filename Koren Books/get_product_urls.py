##web requests
import json
import requests
#regualr expresions
import re
#parses html
from bs4 import BeautifulSoup
#spreadsheet writer
import xlsxwriter
#date and time
from datetime import datetime
#tracker for progress
from alive_progress import alive_bar
    
def get_image(product_name):
    #The regular expression below removes anythinhg that is in parenthesis. So "Hello (World)" becomes "Hello World"
    product_name = re.sub(r"\([^()]*\)", "", product_name)
    #This removes spaces and other siubstrings that are not valid, changing them to "-". So "Hello World" becomes "Hello-World"
    product_name=product_name.replace(" - ", "%20").replace("'", "%20").replace("#", "").replace(", ", "%20").replace(" ", "%20").replace("י", "").lower()
    #This will check if there is a hanging "-" at the end, removing it
    if product_name[-1] == "-":
        product_name = product_name[:-1]
    #We will now be checking if the URL is valid or leads to a 404 error
    request = requests.get("https://www.searchanise.com/getresults?api_key=5Y0o7Q1h4v&q=%s&sortBy=relevance&sortOrder=desc&startIndex=0&maxResults=15&items=true&pages=true&categories=true&suggestions=true&queryCorrection=true&suggestionsMaxResults=3&pageStartIndex=0&pagesMaxResults=20&categoryStartIndex=0&categoriesMaxResults=20&facets=true&facetsShowUnavailableOptions=false&ResultsTitleStrings=2&ResultsDescriptionStrings=2&displaySubcatProducts=&output=jsonp&callback=jQuery224036319537954105874_1643306319571&_=1643306319572"%(product_name), verify=False)
    #json.loads converts the json string to a python dictionary, I use REGEX to remove random strings so we can convert to json
    #then I access the dictionary and get the image url and return it
    request_text = request.text.replace("jQuery224036319537954105874_1643306319571(", "").replace(");", "")
    try:
        return(json.loads(request_text)['items'][0]['shopify_images'][0])
    except Exception as e:
            return "No image found because [%s]"%(e)
        
def main():
    #Create spreadsheet and add headers
    workbook = xlsxwriter.Workbook(str(datetime.now()).replace(" ", "_")+'.xlsx', {'constant_memory': True})
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Product Name')
    worksheet.write('B1', 'Product Image')
    
    #open file with "r" so we just reads and not write
    product_name = open('./products.txt', 'r')
    all_lines = product_name.readlines()
    count = 2
    with alive_bar(len(all_lines)) as bar:
        for product in all_lines:
            #remove new line character
            product = product.replace("\n", "")
            #get url from product name
            product_image = get_image(product)
            if not "No image found because" in product_image:
                print("[+] " + product + ": " + product_image)
            else:
                print("[-] " + product + ": " + product_image)
            #write product name and image url to spreadsheet
            worksheet.write('A'+str(count), product)
            worksheet.write('B'+str(count), product_image)
            count+=1
            bar()
    workbook.close()
            
if __name__ == "__main__":
    main()    
