##web requests
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
    product_name=product_name.replace(" - ", "%20").replace("'", "%20").replace("#", "").replace(", ", "%20").replace(" ", "%20").lower()
    #This will check if there is a hanging "-" at the end, removing it
    if product_name[-1] == "-":
        product_name = product_name[:-1]
    #We will now be checking if the URL is valid or leads to a 404 error
    request = requests.get("https://svc-2-usf.hotyon.com/search?q=%s&apiKey=2a834cb4-4cda-48a1-9a79-28287083a21a&locale=en&getProductDescription=0&skip=0&take=28"%(product_name), verify=False)
    request_json = request.json()
    return(request_json['data']['items'][0]['images'][0]['url'].replace("//cdn.shopify.com", "https://cdn.shopify.com"))
    #return(find_image_from_content(request))
    
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
            if product_image != "No image found":
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
