import customtkinter as ctk
from shared import utils
from functools import partial
from urllib.request import urlopen
from PIL import Image
import threading
import requests
import io
from app_settings import *


class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = utils.adjust_window(800, 600, master)
        master.geometry(window_size)

        self.main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        self.main_frame.pack(fill='both', expand=True)

        left_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        left_frame.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky='nswe')
        ctk.CTkLabel(left_frame, text='Azot', font=('Helvetica', 20, 'bold')).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Profile', command=master.create_seller_profile_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Add Product', command=master.create_add_product_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Orders', command=master.create_orders_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Settings', command=master.create_settings_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Log Out', command=self.log_out).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Close App', command=self.quit).pack(padx=20, pady=10)

        top_frame = ctk.CTkFrame(self.main_frame)
        top_frame.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        ctk.CTkLabel(top_frame, text='Welcome to Azot!', font=('Helvetica', 20, 'bold')).pack(pady=10)

        self.setup_offers_frame()

        thread = threading.Thread(target=self.start)
        thread.start()

        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=0)
        self.main_frame.rowconfigure(2, weight=1)


    def setup_offers_frame(self):
        self.offers_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color='#313335')
        self.offers_frame.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')
        self.popular_offers_label = ctk.CTkLabel(self.offers_frame, text='Your products:', font=('Helvetica', 18))
        self.popular_offers_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)
        self.shuffle_button = ctk.CTkButton(self.offers_frame, text='Refresh', command=self.refresh)
        self.shuffle_button.grid(row=0, column=2, columnspan=2)

        self.offers_frame.columnconfigure(0, weight=1)
        self.offers_frame.columnconfigure(1, weight=1)
        self.offers_frame.columnconfigure(2, weight=1)
        self.offers_frame.columnconfigure(3, weight=1)
        self.offers_frame.rowconfigure(0, weight=0)
        self.offers_frame.rowconfigure(1, weight=1)
        self.offers_frame.rowconfigure(2, weight=1)

    def refresh(self):
        self.setup_offers_frame()
        self.master.user.products.clear()

        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/seller/{self.master.user.id}/product'
        response = requests.get(url)

        if response.status_code == 200:
            products_list = response.json().get('content')
            for product_data in products_list:
                self.master.user.products.append(utils.create_product(product_data))
            self.display_offers()

        else:
            self.master.after(0, self.show_error)

    def start(self):
        if self.master.user.products:
            self.display_offers()
        else:
            url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/seller/{self.master.user.id}/product'
            response = requests.get(url)

            if response.status_code == 200:
                products_list = response.json().get('content')
                for product_data in products_list:
                    self.master.user.products.append(utils.create_product(product_data))
                self.display_offers()

            else:
                self.master.after(0, self.show_error)

    def display_offers(self):
        self.current_row = 1
        self.current_column = 0
        self.placeholder_frames = []
        for _ in range(len(self.master.user.products)):
            product_frame = ctk.CTkFrame(self.offers_frame)
            placeholder_label = ctk.CTkLabel(product_frame, text='Loading...')
            placeholder_label.pack()
            product_frame.grid(row=self.current_row, column=self.current_column, padx=5, pady=5, sticky='nsew')
            self.current_column += 1
            if self.current_column > 3:
                self.current_row += 1
                self.current_column = 0

            self.placeholder_frames.append((product_frame, placeholder_label))

        for idx, product in enumerate(self.master.user.products):
            product_frame, placeholder_label = self.placeholder_frames[idx]
            thread = threading.Thread(target=self.update_product_view, args=(product_frame, placeholder_label, product))
            thread.start()

    def update_product_view(self, product_frame, placeholder_label, product):
        placeholder_label.pack_forget()
        ctk.CTkLabel(product_frame, text=f'{product.name}').pack()
        image_url = product.image
        image_data = urlopen(image_url).read()
        image_pil = Image.open(io.BytesIO(image_data))
        new_size = (80, 80)
        image_pil_resized = image_pil.resize(new_size, Image.LANCZOS)
        image_ctk = ctk.CTkImage(light_image=image_pil_resized, size=new_size)
        ctk.CTkLabel(product_frame, image=image_ctk, text='').pack()
        ctk.CTkLabel(product_frame, text=f'Price: ${product.price:.2f}').pack()
        ctk.CTkLabel(product_frame, text=f'Items available: {product.items_available}').pack()
        check_command = partial(self.check_product, product.id)
        ctk.CTkButton(product_frame, text='Edit', command=check_command).pack(padx=10, pady=5)

    def show_error(self):
        utils.ErrorDialog(self, message='Failed to download product').show()

    def check_product(self, product_id):
        self.master.create_edit_product_frame(product_id)

    def log_out(self):
        dialog = utils.ConfirmDialog(self, title='Log Out', message='Are you sure you want to log out?')
        if dialog.show():
            self.master.create_login_frame()

    def quit(self):
        dialog = utils.ConfirmDialog(self, title='Quit', message='Are you sure you want to exit?')
        if dialog.show():
            self.master.quit()
