import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from tkinter import *
import customtkinter
from tkinter.ttk import Progressbar
import os

from PIL import Image , ImageTk
from pytube import YouTube
import datetime
import calendar
import requests
import re
import moviepy.editor as mp

janela = customtkinter.CTk()
janela.geometry('640x400')
janela.title('DownPyTube')
janela.resizable(False,False)
janela.iconbitmap('imagens\youtube-logo-png-2076-256x256.ico')

##MÓDULO CUSTOMTKINTER[ESTE MÓDULO DEIXA A INTERFACE MAIS MODERNA]
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme('blue')
fundo = "#3b3b3b"

def pesquisar():
    global img
    
#pegando o link
    url = entrada.get()
    
    yt = YouTube(url)
    
# titulo
    titulo = yt.title

#  Função para baixar a thumbnail do vídeo.
    foto = yt.thumbnail_url
    img = Image.open(requests.get(foto, stream=True).raw)
    img = img.resize((141,167), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)
    label_imagem['image'] = img
    label_titulo['text'] ="Titulo : " + titulo

#Função para baixar o vídeo e converter para mp3.
def download_mp3():
    download_Folder = download_Path.get() 
    url=entrada.get()
    yt=YouTube(url)
    yt.register_on_progress_callback(on_progress)
    yt.streams.filter(file_extension='mp4')
    yt.streams.get_by_itag(22).download(download_Folder)
    yt.streams.filter(only_audio=True).first().download()
    messagebox.showinfo("SUCESSO", " VÍDEO BAIXADO E SALVO NO DIRETÓRIO\n"+ download_Folder)
#Convertendo para MP3.
    for file in os.listdir(download_Folder):
        if re.search('mp4', file):
            mp4_path = os.path.join(download_Folder, file)
            mp3_path = os.path.join(download_Folder, os.path.splitext(file)[0]+'.mp3')
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)
            os.remove(mp4_path)

#Função para download do vídeo.
def download_mp4():
    download_Folder = download_Path.get() 
    url=entrada.get()
    yt=YouTube(url)
    yt.register_on_progress_callback(on_progress)
    yt.streams.filter(file_extension='mp4')
    yt.streams.get_by_itag(22).download(download_Folder)
    yt.streams.filter(only_audio=True).first().download()
    messagebox.showinfo("SUCESSO", " VÍDEO BAIXADO E SALVO NO DIRETÓRIO\n"+ download_Folder)
video_Link = StringVar() 
download_Path = StringVar() 

#Função para escolher o diretório de salvamento do vídeo.
def Browse(): 
    download_Directory = filedialog.askdirectory(initialdir="ESCOLHA O DIRETÓRIO") 
    download_Path.set(download_Directory)

#Função para barra de progresso sincronizada com tempo de download.
previousprogress = 0
def on_progress(stream, chunk, bytes_remaining):
    global previousprogress
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining 

    liveprogress = (int)(bytes_downloaded / total_size * 100)
    if liveprogress > previousprogress:
        previousprogress = liveprogress
        print(liveprogress)
        bar['value'] = liveprogress
        frame3.update_idletasks()
    if liveprogress == 100:
         previousprogress = 0
        
#Função para configurar a janela no modo noturno ou light.   
def change_appearance_mode(new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

frame = customtkinter.CTkFrame(master=janela, width=250, height=400, corner_radius=10, border_width=1, border_color='cyan')
frame.pack(padx=10, pady=10, side='left', fill='both', anchor='n', expand=False)
frame2 = customtkinter.CTkFrame(master=janela, width=500, height=400, corner_radius=10, border_width=1, border_color='black')
frame2.pack(padx=10, pady=10, fill='both', side='right', anchor='n', expand=True)
frame3 = customtkinter.CTkFrame(master=frame2, width=500, height=400, corner_radius=10, border_width=1, border_color='black')
frame3.pack(padx=10, pady=10, fill="both", side='bottom', anchor='n', expand=True)

#inserindo imagem no frame.
logo = PhotoImage(file='imagens\youtube-logo-png-46039.png')
logo = logo.subsample(2,3)
imagem = customtkinter.CTkLabel(master=frame2, image=logo)
imagem.pack(side='top', anchor='n', pady=5, expand=False)

label = customtkinter.CTkLabel(master=frame3, width=20, text_font='cambria 10', text="LINK YOUTUBE:")
label.pack(pady=20, padx=10, side='left', anchor='n')
entrada = customtkinter.CTkEntry(master=frame3, width=210, height=11, corner_radius=10, border_width=2, border_color='gray')
entrada.place(x=110, y=22)
botao = customtkinter.CTkButton(master=frame3, width=3, height=4, text_font='georgia 9', corner_radius=8, border_width=1, border_color='gray',  text="Pesquisar",command=pesquisar)
botao.pack(padx=10, pady=21, side='right', anchor='n')
label = customtkinter.CTkLabel(master=frame3, text_font='cambria 10', width=20, text="DIRETÓRIO:")
label.place(x=10, y=70)
diretorio = customtkinter.CTkEntry(master=frame3, width=210, height=11, corner_radius=10, border_width=2, border_color='gray', textvariable=download_Path)
diretorio.place(x=110, y=73)
botao3 = customtkinter.CTkButton(master=frame3, width=3, height=3, text_font='georgia 9', corner_radius=8, border_width=1, border_color='gray',  text="Diretório", command=Browse)
botao3.place(x=332, y=72)
botao4= customtkinter.CTkButton(master=frame3, width=3, height=4, text_font='cambria 10', corner_radius=8, border_width=1, text='DOWNLOAD MP3', border_color='gray', command=download_mp3)
botao4.place(x=67, y=150)
botao2= customtkinter.CTkButton(master=frame3, width=3, height=4, text_font='cambria 10', corner_radius=8, border_width=1, text='DOWNLOAD MP4', border_color='gray', command=download_mp4)
botao2.place(x=230, y=150)

frame4 = customtkinter.CTkFrame(master=frame, width=151, height=175, corner_radius=7, border_width=1, border_color='black')
frame4.pack(pady=8, padx=5)
label_imagem = ttk.Label(master=frame4, text="", background='#313131', compound="center")
label_imagem.place(x=4,y=2)

label_titulo = Label(frame, wraplength=140, justify="left", anchor="nw", bg="#303030", font="ivy 9 bold")
label_titulo.pack(pady=2)

optionmenu_1 = customtkinter.CTkOptionMenu(master=frame, text_font="georgia 10", corner_radius=15, values=["Light", "Dark"], command=change_appearance_mode)
optionmenu_1.pack(pady=15, padx=10,  side="bottom")
label = customtkinter.CTkLabel(master=frame, text_font='cambria 10', width=15, height=6, text="TEMA:")
label.place(x=57, y=317)

#Barra de Progresso
style = ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", background='#00E676')
style.configure("TProgressbar", thickness=5)
bar = Progressbar(frame3, length=300,style='black.Horizontal.TProgressbar')
bar.place(x=60, y=190)

optionmenu_1.set("Dark")



janela.mainloop()