import cloudscraper
from bs4 import BeautifulSoup as bs
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
#Inicia sesion
f = open("C:\\Users\\stbaz\\Documents\\COPER\\cuentas\\cuentas.txt", "r")
while(True):
    line = f.readline()
    if not line: break
    datos = line.split(',')
    usr = datos[0]
    pwd = datos[1]
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    scraper = cloudscraper.create_scraper(browser='chrome')
    print("Iniciando sesion")
    startTime = time.time()
    site = scraper.get("https://www.innvictus.com/login",headers=headers)
    bs_content = bs(site.content, "html.parser")
    token = bs_content.find("input", {"name":"g-recaptcha-action"})["value"]
    crf = bs_content.find("input", {"name": "CSRFToken"})["value"]
    remeber = bs_content.find("input", {"name": "persistent_remember_me"})["value"]
    login_data = {"g-recaptcha-action":token,"j_username":usr.strip(), "j_password": pwd.strip(), "persistent_remember_me": remeber,"CSRFToken":crf}
    pag = scraper.post("https://www.innvictus.com/ajax/j_spring_security_check",login_data)
    if pag.url == "https://www.innvictus.com/login/ajax?error=true":
        print("No se pudo inicar sesión")
    else:
        print("Sesion iniciada en "+pag.url)
        product_id = "DD1869-102"
        search_url = "https://www.innvictus.com/search/?text="+product_id
        product_site = scraper.get(search_url)
        if product_site.url != "https://www.innvictus.com/search/?text=":
            print("Producto encontrado " +product_id)
            bs_content_product = bs(product_site.content, "html.parser")
            qty = bs_content_product.find("input", {"name":"qty"})["value"]
            product_code = bs_content_product.find("input", {"name":"productCodePost"})["value"]
            confirmation_message = bs_content_product.find("input", {"name":"displayConfirmationMessage"})["value"]
            token_product = bs_content_product.find("input", {"name":"CSRFToken"})["value"]
            atc_data = {"qty":qty, "productCodePost": product_code, "displayConfirmationMessage": "false", "CSRFToken":token_product}
            atc_pag = scraper.post("https://www.innvictus.com/cart/add", atc_data)
            print("Producto agregado al carrtio")
            checkout_page = scraper.get("https://www.innvictus.com/checkout/multi/delivery-address/add",headers=headers)
            bs_content_cart = bs(checkout_page.content, "html.parser")
            cart_product_name = bs_content_cart.find("div", {"class":"shipping-product-address-title"})
            cart_product_quantity = bs_content_cart.find("div", {"class":"qty"})
            cart_product_size = bs_content_cart.find("div", {"class":"style-size"})
            cart_product_image = bs_content_cart.find("img", {"style":"max-width: 100%;"})["src"]
            pic = "https://www.innvictus.com/"+cart_product_image
            tiempo_total = time.time() - startTime
            #--------------------------------------------------DISCORD-------------------------------------------
            webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/781705037290143754/VVWvzY6rEQ7pGH_mwnQAZK-mmKvr-IjSKUnvIcA6zrNVlTQs_MZCV6PeL2wBDm-rpMje', username="COPER")
            embed = DiscordEmbed(title=usr, description=cart_product_name.text, color=242424)
            embed.set_author(name='NUEVO PRODUCTO ASEGURADO')
            embed.set_footer(text="--- %s seconds ---" % (tiempo_total))
            embed.set_thumbnail(url=pic)
            embed.set_timestamp()
            embed.add_embed_field(name='Cantidad', value=cart_product_quantity.text)
            embed.add_embed_field(name='Talla y colores', value=cart_product_size.text)
            embed.add_embed_field(name='CARTHOLD', value='TRUE')
            webhook.add_embed(embed)            
            response = webhook.execute()
            print(time.time() - startTime)
        else:
            print("Producto no encontrado")