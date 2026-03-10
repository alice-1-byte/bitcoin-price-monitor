import os
import customtkinter as ctk 
from PIL import Image
import requests

janela = ctk.CTk()
janela.geometry('450x350')
janela.title('')
janela.attributes('-zoomed', True)

# cores -----------------------

cor0= "#010409"
cor1= "#0D1117" 
cor2= "#464661"
cor3= "#C2A607"
cor4= "#FFFFFF" 
cor5= "#30363D"
cor6= "#BC39EE"
cor7= "#9B111E"
cor8= "#4A5D23"

preco_anterior = {"BRL": 0.0, "USD": 0.0, "EUR": 0.0}

janela.configure(fg_color= cor0)
janela.grid_rowconfigure(2, weight=1) 
janela.grid_columnconfigure(0, weight=1)

# Frame de cima --------------------------------------------

frame_cima = ctk.CTkFrame(janela, height=60, fg_color=cor1, corner_radius=0)
frame_cima.grid(row=0, column=0, sticky="ew")

frame_cima.grid_columnconfigure(0, weight=1) 
frame_cima.grid_columnconfigure(1, weight=0) 
frame_cima.grid_columnconfigure(2, weight=0) 
frame_cima.grid_columnconfigure(3, weight=1) 

# Imagem ------------------------------------

diretorio_base = os.path.dirname(os.path.realpath(__file__))
caminho_imagem = os.path.join(diretorio_base, "logo.bitc.png")

img_logo = Image.open(caminho_imagem)
imagem_logo = ctk.CTkImage(light_image=img_logo, dark_image=img_logo, size=(40, 40))

l_logo = ctk.CTkLabel(frame_cima, image=imagem_logo, text="")
l_logo.grid(row=0, column=1, padx=(0, 10), pady=10)

# título -----------------------------------

l_titulo = ctk.CTkLabel(frame_cima, text="BITCOIN PRICE MONITORING", font=("roboto", 20, "bold"), text_color=cor6)
l_titulo.grid(row=0, column=2, pady=20)

# Linha divisoria -----------------------------------------

linha = ctk.CTkFrame(janela, height=2, fg_color=cor5)
linha.grid(row=1, column=0, sticky="ew")

# configurando frame de baixo ------------------------------

frame_baixo = ctk.CTkFrame(janela, fg_color=cor0, corner_radius=0)
frame_baixo.grid(row=2, column=0, sticky="nsew", pady=(20, 0)) 
frame_baixo.grid_columnconfigure((0, 1, 2), weight=1)

l_info = ctk.CTkLabel(frame_baixo, text="BITCOIN CURRENT PRICE (BTC)", font=("roboto", 20), text_color=cor6)
l_info.grid(row=0, column=0, columnspan=3, pady=(18, 130), padx=(50,10))

l_brl = ctk.CTkLabel(frame_baixo, text="Carregando...", font=("roboto", 25, "bold"), text_color=cor3)
l_brl.grid(row=1, column=0, pady=(0, 10))

l_usd = ctk.CTkLabel(frame_baixo, text="Carregando...", font=("roboto", 25, "bold"), text_color=cor3)
l_usd.grid(row=1, column=1, pady=(0, 10))

l_eur = ctk.CTkLabel(frame_baixo, text="Carregando...", font=("roboto", 25, "bold"), text_color=cor3)
l_eur.grid(row=1, column=2, pady=(0, 10))

# Labels dos valores -------------------------------------------------------------------------

ctk.CTkLabel(frame_baixo, text="REAIS (BRL)", font=("roboto", 15),
text_color=cor4 if 'cor4' in locals() else "white").grid(row=2, column=0, pady=(5, 5))

ctk.CTkLabel(frame_baixo, text="DÓLAR (USD)", font=("roboto", 15),
text_color=cor4 if 'cor4' in locals() else "white").grid(row=2, column=1, pady=(5, 5))

ctk.CTkLabel(frame_baixo, text="EURO (EUR)", font=("roboto", 15), 
text_color=cor4 if 'cor4' in locals() else "white").grid(row=2, column=2, pady=(5, 5))    

# Atualização de preços com APIs -----------------------------------------

def atualizar_precos():
    
    try:

        headers ={'User-Agent': 'Mozilla/5.0'}
    
    #APIs ----------------------------

        res_brl = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCBRL", headers=headers).json()
        res_usd = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSD" , headers=headers).json()
        res_eur = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCEUR" , headers=headers).json()

        p_brl = float(res_brl['price'])
        p_usd = float(res_usd['price'])
        p_eur = float(res_eur['price'])

     # Comparação com valores anteriores ------------------------------------------------
        
        def definir_estilo(atual, anterior):
            
            if anterior == 0: return "", cor3
            if atual > anterior: return "▲", cor8
            if atual < anterior: return "▼", cor7
            return "", cor3
        
        seta_brl, cor_brl = definir_estilo(p_brl, preco_anterior["BRL"])
        seta_usd, cor_usd = definir_estilo(p_usd, preco_anterior["USD"])
        seta_eur, cor_eur = definir_estilo(p_eur, preco_anterior["EUR"])

        v_brl = f"R$ {p_brl:,.2f} {seta_brl}".replace(",", "X").replace(".", ",").replace("X", ".")
        l_brl.configure(text=v_brl, text_color=cor_brl)

        l_usd.configure(text=f"$ {p_usd:,.2f} {seta_usd}", text_color=cor_usd)
        
        l_eur.configure(text=f"€ {p_eur:,.2f} {seta_eur}", text_color=cor_eur)

        preco_anterior["BRL"] = p_brl
        preco_anterior["USD"] = p_usd
        preco_anterior["EUR"] = p_eur

        print("Preços atualizados!")
    
    except Exception as e:
        print("Erro ao atualizar:", e)

janela.after(100, atualizar_precos)       
janela.mainloop()