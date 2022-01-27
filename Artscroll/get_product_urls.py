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

def findString(string):
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)      
    return [x[0] for x in url]
    
def get_image(product_name):
    #The regular expression below removes anythinhg that is in parenthesis. So "Hello (World)" becomes "Hello World"
    product_name = re.sub(r"\([^()]*\)", "", product_name)
    #This removes spaces and other siubstrings that are not valid, changing them to "-". So "Hello World" becomes "Hello-World"
    product_name=product_name.replace(" - ", "%20").replace("'", "%20").replace("#", "").replace(", ", "%20").replace(" ", "%20").lower()
    #This will check if there is a hanging "-" at the end, removing it
    if product_name[-1] == "-":
        product_name = product_name[:-1]
    #We will now be checking if the URL is valid or leads to a 404 error
    request = requests.get("https://www.artscroll.com/search/%s.aspx"%(product_name), verify=False)
    #use bs4 to get ing tag with class Product
    soup = BeautifulSoup(request.text, 'html.parser')
    #if the product search results in many options then choose first one
    if "/search" in request.url:
        #use bs4 to get a tag with id "ctl00_mPageContent_itemList1_shopItemsView_ctrl0_Hyperlink2"
        product = soup.find('a', id='ctl00_mPageContent_itemList1_shopItemsView_ctrl0_Hyperlink2')
        request = requests.get(str(product['href']), verify=False)
        soup = BeautifulSoup(request.text, 'html.parser')
        product = str(soup.find('a', class_='DAIucLink'))
        start = product.find('<a class="DAIucLink" id="ctl00_mPageContent_hplLinkToZoom" onclick="ShowPopUp(\'https://www.artscroll.com/EnlargedImage.aspx?imageid=&amp;imagetype=&amp;imagePath=') + len('<a class="DAIucLink" id="ctl00_mPageContent_hplLinkToZoom" onclick="ShowPopUp(\'https://www.artscroll.com/EnlargedImage.aspx?imageid=&amp;imagetype=&amp;imagePath=')
        end = product.find("&amp;name=101+Engaging+Questions+to+spur+dynamic+Torah+conversation+in+any+setting', 550, 600, 'yes')\">Click here to view a full-size image</a>")
        return(findString("https://www.artscroll.com"+product[start:end].rpartition('&amp')[0].rpartition('')[0])[0])
    else:
    #pull the image location and add it top URL scheme from product var
    #find image with class Product (first result)
        product = str(soup.find('a', class_='DAIucLink'))
        start = product.find('<a class="DAIucLink" id="ctl00_mPageContent_hplLinkToZoom" onclick="ShowPopUp(\'https://www.artscroll.com/EnlargedImage.aspx?imageid=&amp;imagetype=&amp;imagePath=') + len('<a class="DAIucLink" id="ctl00_mPageContent_hplLinkToZoom" onclick="ShowPopUp(\'https://www.artscroll.com/EnlargedImage.aspx?imageid=&amp;imagetype=&amp;imagePath=')
        end = product.find("&amp;name=101+Engaging+Questions+to+spur+dynamic+Torah+conversation+in+any+setting', 550, 600, 'yes')\">Click here to view a full-size image</a>")
        return("https://www.artscroll.com"+product[start:end])
    
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
        for product in all_lines[1:]:
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
