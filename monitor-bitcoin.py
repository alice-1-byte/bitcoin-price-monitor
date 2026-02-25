import os
import customtkinter as ctk 
from PIL import Image
import requests

# cores -----------------------

cor0= "#010409"
cor1= "#0D1117" 
cor2= "#464661"
cor3= "#00D1FF"
cor4= "#FFFFFF" 
cor5= "#30363D"
cor6= "#BC39EE"

janela= ctk.CTk ()  
janela.title('')
janela.geometry('320x350')

janela.configure(fg_color= cor0)
janela.grid_columnconfigure(0, weight=1)

# Dividindo a janela em dois frames ----------------------

frame_cima = ctk.CTkFrame (janela, width= 320, height= 50, fg_color=cor1, corner_radius= 0)
frame_cima.grid(row= 0, column = 0, sticky="ew")

frame_cima.grid_rowconfigure(0, weight=1)

frame_cima.grid_columnconfigure(0, weight=1)
frame_cima.grid_columnconfigure(3, weight=1)

linha = ctk.CTkFrame(janela, height= 2, fg_color=cor5)
linha.grid(row=1, column=0, columnspan=1, sticky="ew", padx=10, pady=5)

frame_baixo = ctk.CTkFrame (janela, width= 320, height= 300, fg_color=cor0, corner_radius= 0)
frame_baixo.grid(row= 2, column = 0, sticky="nsew", padx = 0, pady = 0)


# Configurando frame cima ---------------------------------

diretorio_base = os.path.dirname(os.path.realpath(__file__))
caminho_imagem = os.path.join(diretorio_base, "logo.bitc.png")

imagem_logo = ctk.CTkImage(light_image=Image.open(caminho_imagem), size=(40, 40))

l_logo = ctk.CTkLabel(frame_cima, image=imagem_logo, text="")
l_logo.grid(row=0, column=1, padx=(0, 10), pady=10)

l_titulo = ctk.CTkLabel(frame_cima, text="BITCOIN PRICE MONITORING", font=("roboto", 20, "bold"), text_color=cor6)
l_titulo.grid(row=0, column=2, padx=(0, 0), pady= 10)

# configurando frame de baixo ------------------------------

l_info = ctk.CTkLabel (frame_baixo, text = "BITCOIN CURRENT PRICE (BTC)", font=("roboto", 14), text_color=cor6)
l_info.grid(row=0, column=0, columnspan=3, pady=(20, 10))

janela.grid_rowconfigure(2, weight=1)

frame_baixo.grid_columnconfigure(0, weight=1)
frame_baixo.grid_rowconfigure(0, weight=1)
frame_baixo.grid_rowconfigure(3, weight=1)

frame_baixo.grid_columnconfigure((0, 1, 2), weight=1) 

l_brl = ctk.CTkLabel(frame_baixo, text="Carregando...", font=("roboto", 22, "bold"), text_color=cor3)
l_brl.grid(row=1, column=0, pady=20)
l_usd = ctk.CTkLabel(frame_baixo, text="Carregando...", font=("roboto", 22, "bold"), text_color= cor3)
l_usd.grid(row=1, column=1, pady=20)
l_eur = ctk.CTkLabel(frame_baixo, text="Carregando...", font=("roboto", 22, "bold"), text_color= cor3)
l_eur.grid(row=1, column=2, pady=20)


def atualizar_precos():
    try:

        headers ={'User-Agent': 'Mozilla/5.0'}

        url_brl = "https://api.binance.com/api/v3/ticker/price?symbol=BTCBRL"
        url_usd = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        url_eur = "https://api.binance.com/api/v3/ticker/price?symbol=BTCEUR"

        res_brl = requests.get (url_brl, headers=headers).json()
        res_usd = requests.get (url_usd, headers=headers).json()
        res_eur = requests.get (url_eur, headers=headers).json()

        v_brl = f"R$ {float(res_brl['price']):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        v_usd = f"$ {float(res_usd['price']):,.2f}"
        v_eur = f"€ {float(res_eur['price']):,.2f}"

        ctk.CTkLabel(frame_baixo, text="REAIS (BRL)", font=("roboto", 10), text_color=cor6).grid(row=2, column=0)
        ctk.CTkLabel(frame_baixo, text="DÓLAR (USD)", font=("roboto", 10), text_color=cor6).grid(row=2, column=1)
        ctk.CTkLabel(frame_baixo, text="EURO (EUR)", font=("roboto", 10), text_color=cor6).grid(row=2, column=2)

        l_brl.configure(text=v_brl)
        l_usd.configure(text=v_usd)
        l_eur.configure(text=v_eur)
        print("Preços atualizados!")

    except Exception as e:
        print("Erro ao atualizar:", e)

janela.after(2000, atualizar_precos)


janela.mainloop()