import cloudscraper
from bs4 import BeautifulSoup as bs
from discord_webhook import DiscordWebhook, DiscordEmbed
f = open("C:\\Users\\stbaz\\Documents\\COPER\\cuentas\\cuentas3.txt", "r")
while(True):
    line = f.readline()
    if not line: break
    datos = line.split(',')
    usr = datos[0]
    pwd = datos[1]
    print(usr)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    scraper = cloudscraper.create_scraper(browser='chrome')
    print("Iniciando sesion")
    site = scraper.get("https://www.innvictus.com/login",headers=headers)
    bs_content = bs(site.content, "html.parser")
    token = bs_content.find("input", {"name":"g-recaptcha-action"})["value"]
    crf = bs_content.find("input", {"name": "CSRFToken"})["value"]
    remeber = bs_content.find("input", {"name": "persistent_remember_me"})["value"]
    login_data = {"g-recaptcha-action":token,"j_username":usr.strip(), "j_password": pwd.strip(), "persistent_remember_me": remeber,"CSRFToken":crf}
    pag = scraper.post("https://www.innvictus.com/ajax/j_spring_security_check",login_data,headers=headers)
    if pag.url == "https://www.innvictus.com/login/ajax?error=true":
        print("No se pudo inicar sesión")
    else:
        print("Sesion iniciada en "+pag.url)
        cart_page = scraper.get("https://www.innvictus.com/cart",headers=headers)
        print(cart_page.url)
        try:
            bs_content_cart = bs(cart_page.content, "html.parser")
            entry_number = bs_content_cart.find("input", {"name":"entryNumber"})["value"]
            product_code = bs_content_cart.find("input", {"name":"productCode"})["value"]
            initial_qty =  bs_content_cart.find("input", {"name":"initialQuantity"})["value"]
            token = bs_content_cart.find("input", {"name":"CSRFToken"})["value"]
            empty_cart = {"entryNumber":entry_number.strip(),"productCode":product_code.strip(),"initialQuantity":initial_qty.strip(),"quantity":"0","CSRFToken":token.strip()}
            print(empty_cart)
            cart_empty_pag = scraper.post("https://www.innvictus.com/cart/update",empty_cart,headers=headers)
            print(cart_empty_pag)
        except:
            print("No hay productos")