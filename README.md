This was made for my college, Yeshiva University, Jewish Book Sale. I was approached to help get product images for thousands of books as the manufacturers did not provide them. 

I use Python to make a request top the manufacturers site, and make a search query based on their public API or regular website search if no API available. When there was an API, I selected the firsty, which is the most relevent, index of the JSON and grabbed the product image URL. If there was no API I used the BeautifulSoup Python module to query any HTMML tag that represented search result products, and selected the first occurence, following the product URL, and finally using the same methods to grab the product image URL.

This was very fun and educational as I learned how powerful BeautifulSoup can be.