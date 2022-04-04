from tkinter import *

from tkinter import ttk
from turtle import color, down
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import matplotlib.dates as mpl_dates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import websocket
from threading import Thread
from matplotlib import style

#from controller.api_left import api_Left
#from controller.api_right import api_Right
from controller.graph import Graph

from controller.botorderclient import BotOrderClient


#  red  	#f6465d
#  green    #0ecb81
#  black    #000000
#  number   #a5a9b2


class Main:
    def __init__(self, name) -> None:

        self. left_side_table = tuple()
        self.candle = pd.read_csv(
            'https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

        self.window = Tk()
        self.bool = False
        self.window.title(name)
        self.window.configure(bg="#000000")
        self.bottom()
        self.menu()
        self.side_bar_Left()
        self.graph_zone()
        self.side_bar_Right()

    def side_bar_Left(self):
        side = Frame(self.window)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#000000",
                        foreground="#a5a9b2",
                        fieldbackground="#000000"
                        )
        table_variation = ttk.Treeview(side, show="headings")
        table_variation['columns'] = ('Prix', 'Montant', 'Total')
        table_variation.heading("Prix", text="Prix")
        table_variation.heading("Montant", text="Montant")
        table_variation.heading("Total", text="Total")
        table_variation.column("Prix", anchor=CENTER, width=30)
        table_variation.column("Montant", anchor=CENTER, width=60)
        table_variation.column("Total", anchor=CENTER, width=35)
        data = self.con()

        for contact in data:
            table_variation.insert('', END, values=contact)

        table_variation.pack(fill=BOTH, expand=TRUE)
        side.pack(fill=BOTH, side=LEFT, expand=TRUE)

    def con(self):
        contacts = []
        for n in range(1, 100):
            contacts.append(
                (f'first {n}', f'last {n}', f'email{n}@example.com'))
        return contacts

    def graph_zone(self):
        # frame
        side = Frame(self.window, bg="white")
        side.pack(side=LEFT, fill=BOTH, expand=TRUE)

        # self.candle.loc[:, ['Date', 'AAPL.Open',
        #    'AAPL.High', 'AAPL.Low', 'AAPL.Close']]
        self.candle['Date'] = self.candle['Date']

        self.candle['Open'] = self.candle['AAPL.Open']
        self.candle['High'] = self.candle['AAPL.High']
        self.candle['Low'] = self.candle['AAPL.Low']
        self.candle['Close'] = self.candle['AAPL.Close']
        self.candle['Volume'] = self.candle['AAPL.Volume']
        self.candle.index = pd.DatetimeIndex(self.candle['Date'])
        colors = mpf.make_marketcolors(
            up="#0ecb81",
            down="#f6465d",
            wick="inherit",
            edge="inherit",
            volume="in"
        )

        mpf_style = mpf.make_mpf_style(
            base_mpf_style="mike", marketcolors=colors)
        fig, ax = mpf.plot(self.candle, type='candle', mav=(
            3, 6, 9), volume=True, style=mpf_style, returnfig=True)

        canvas = FigureCanvasTkAgg(fig, master=side)

        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)

    def menu(self):
        top = Frame(self.window, height=30, bg="#000000")
        top.pack(fill=X, side=TOP)

        # paire
        paire = Frame(top, bg="#000000")
        paire.pack(side=LEFT, fill=BOTH, expand=TRUE)
        lpaire = Label(paire, text="paire", fg="#0ecb81", bg="#000000")
        lpaire.pack(side=LEFT)

        # price
        price = Frame(top, bg="#000000")
        price.pack(side=LEFT, fill=BOTH, expand=TRUE)
        lprice = Label(price, text="price", fg="#0ecb81", bg="#000000")
        lprice.pack(side=LEFT)

        # variation
        variation = Frame(top, bg="#000000")
        variation.pack(side=LEFT, fill=BOTH, expand=TRUE)
        lvariation = Label(variation, text="variation 24h",
                           fg="#0ecb81", bg="#000000")
        lvariation.pack(side=LEFT)

        # 24h haut
        haut = Frame(top, bg="#000000")
        haut.pack(side=LEFT, fill=BOTH, expand=TRUE)
        lhaut = Label(haut, text="24h haut", fg="#0ecb81", bg="#000000")
        lhaut.pack(side=LEFT)

        # 24h bas
        bas = Frame(top, bg="#000000")
        bas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        lbas = Label(bas, text="24h bas", fg="#0ecb81", bg="#000000")
        lbas.pack(side=LEFT)

        # volume
        volume = Frame(top, bg="#000000")
        volume.pack(side=LEFT, fill=BOTH, expand=TRUE)
        lvolume = Label(volume, text="24h volume", fg="#0ecb81", bg="#000000")
        lvolume.pack(side=LEFT)

        #  robot
        robot = Frame(top, bg="#000000")
        robot.pack(side=RIGHT, fill=BOTH, expand=TRUE)
        b_robot = Button(robot, text="Robot", fg="#0ecb81",
                         bg="#000000", command=self.state)
        b_robot.pack(side=RIGHT)

    def state(self):
        self.bool = not self.bool
        print(self.bool)

    def side_bar_Right(self):
        side = Frame(self.window)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#000000",
                        foreground="#a5a9b2",
                        fieldbackground="#000000"
                        )
        table_variation = ttk.Treeview(side, show="headings")
        table_variation['columns'] = ('s', 'p', 'v')
        table_variation.heading("s", text="Paire")
        table_variation.heading("p", text="Prix")
        table_variation.heading("v", text="Variation")
        table_variation.column("s", anchor=CENTER, width=40)
        table_variation.column("p", anchor=CENTER, width=60)
        table_variation.column("v", anchor=CENTER, width=65)

        # for n in range(1, 100):

        table_variation.insert('', END, values=self.left_side_table)

        table_variation.pack(fill=BOTH, expand=TRUE)
        side.pack(fill=BOTH, side=LEFT, expand=TRUE)

    def bottom(self):
        btm = Frame(self.window, height="5", bg="#000000")
        # compte
        fcompte = Frame(btm, bg="#000000")
        fcompte.pack(side=LEFT, expand=TRUE, fill=X)
        l_owner = Label(fcompte, bg="#000000", fg="#0ecb81", text="owner :")
        l_owner.pack(side=LEFT, expand=TRUE, fill=BOTH)
        l_owner_name = Label(fcompte, bg="#000000",
                             fg="#0ecb81", text="group-projet")
        l_owner_name.pack(side=LEFT, expand=TRUE, fill=BOTH)

        l_montant_compte = Label(
            fcompte, bg="#000000", fg="#0ecb81", text="Solde :")
        l_montant_compte.pack(side=LEFT, expand=TRUE, fill=BOTH)
        l_owner_solde = Label(fcompte, bg="#000000",
                              fg="#0ecb81", text="100000$")
        l_owner_solde.pack(side=LEFT, expand=TRUE, fill=BOTH)

        fdetail = Frame(btm, bg="#000000").pack(
            side=LEFT, expand=TRUE, fill=BOTH)
        fdetail1 = Frame(btm, bg="#000000").pack(
            side=LEFT, expand=TRUE, fill=BOTH)

        # buy
        buyframe = Frame(btm, bg="#000000")
        buyframe.pack(expand=TRUE, side=LEFT, fill=BOTH, pady=10, padx=10)

        # first
        first_buy = Frame(buyframe, bg="#000000")
        first_buy.pack(fill=X)
        l_prix_buy = Label(first_buy, text="prix", fg="#0ecb81", bg="#000000")
        l_prix_buy.pack(fill=X, side=LEFT, expand=TRUE)
        entry_prix_buy = Entry(first_buy, fg="#0ecb81", bg="#000000")
        entry_prix_buy.pack(fill=X, side=LEFT, expand=TRUE)

        # # second
        second_buy = Frame(buyframe, bg="#000000")
        second_buy.pack(fill=X)
        l_montant_buy = Label(second_buy, text="montant",
                              fg="#0ecb81", bg="#000000")
        l_montant_buy.pack(fill=X, side=LEFT, expand=TRUE)
        entry_montant_buy = Entry(second_buy, fg="#0ecb81", bg="#000000")
        entry_montant_buy.pack(fill=X, side=LEFT, expand=TRUE)
        btn_buy = Button(buyframe, text="buy",
                         bg="#0ecb81", fg="white", bd="0")
        btn_buy.pack(fill=X)

        # sell
        sellFrame = Frame(btm, bg="#000000")
        sellFrame.pack(expand=TRUE, side=LEFT, fill=BOTH, pady=10, padx=10)
        # first
        first_sell = Frame(sellFrame)
        first_sell.pack(fill=X)
        l_prix = Label(first_sell, text="prix", fg="#0ecb81", bg="#000000")
        l_prix.pack(fill=X, side=LEFT, expand=TRUE)
        entry_prix_sell = Entry(first_sell, fg="#0ecb81", bg="#000000")
        entry_prix_sell.pack(fill=X, side=LEFT, expand=TRUE)

        # # second
        second_sell = Frame(sellFrame)
        second_sell.pack(fill=X)
        l_montant = Label(second_sell, text="montant",
                          fg="#0ecb81", bg="#000000")
        l_montant.pack(fill=X, side=LEFT, expand=TRUE)
        entry_montant_sell = Entry(second_sell, fg="#0ecb81", bg="#000000")
        entry_montant_sell.pack(fill=X, side=LEFT, expand=TRUE)

        btn_sell = Button(sellFrame, text="sell",
                          bg="#f6465d", fg="white", bd="0")
        btn_sell.pack(fill=X)

        #
        btm.pack(fill=BOTH, expand=TRUE, side=BOTTOM, pady=20)

    def start(self):

        self.window.mainloop()

    def animation(self):
        pulldata = open("data.txt").read()
        datalist = pulldata.split('\n')
        xList = []
        yList = []
        for line in datalist:
            if len(line) > 1:
                x, y = line.split(',')
                xList.append(int(x))
                yList.append(int(y))


# /quote?symbol=AAPL
if __name__ == "__main__":
    main = Main("Tranding Robot 1")

    # t_right = Api_Right()
    # right = Thread(target=t_right.start)
    # right.setDaemon(True)
    # right.start()
    # print(t_right.data)

    # t_left = Api_Left()
    # left = Thread(target=t_left.start)
    # left.setDaemon(True)
    # left.start()

    t_center = Graph()
    center = Thread(target=t_center.start)
    center.setDaemon(True)
    center.start()

    # start the GUI
    main.start()
