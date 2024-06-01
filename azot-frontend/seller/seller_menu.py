import customtkinter as ctk
from shared import utils, classes
import threading
import requests
from functools import partial
from urllib.request import urlopen
from PIL import Image
import io


class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.setup_window()
        self.create_main_frame()
        self.create_left_frame()
        self.create_top_frame()
        self.create_offers_frame()

        if not self.master.viewed_products:
            threading.Thread(target=self.get_products).start()
        else:
            self.display_products(self.master.viewed_products)

    def setup_window(self):
        window_size = utils.adjust_window(800, 600, self.master)
        self.master.geometry(window_size)

    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        self.main_frame.pack(fill='both', expand=True)
        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)

    def create_left_frame(self):
        left_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        left_frame.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky='nsew')
        ctk.CTkLabel(left_frame, text='Azot', font=('Helvetica', 20, 'bold')).pack(padx=20, pady=10)
        self.create_left_buttons(left_frame)

    def create_left_buttons(self, frame):
        buttons = [
            ('Profile', self.master.create_seller_profile_frame),
            ('Add Product', self.master.create_add_product_frame),
            ('Orders', self.master.create_orders_frame),
            ('Settings', self.master.create_settings_frame),
            ('Log Out', self.log_out),
            ('Close App', self.quit)
        ]
        for text, command in buttons:
            ctk.CTkButton(frame, text=text, command=command).pack(padx=20, pady=10)

    def create_top_frame(self):
        top_frame = ctk.CTkFrame(self.main_frame)
        top_frame.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        ctk.CTkLabel(top_frame, text='Welcome to Azot!', font=('Helvetica', 20, 'bold')).pack(pady=10)

    def create_offers_frame(self):
        self.offers_frame = ctk.CTkFrame(self.main_frame, fg_color='#313335')
        self.offers_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        products_label = (ctk.CTkLabel(self.offers_frame, text='Your products:', font=('Helvetica', 18)))
        products_label.grid(row=0, column=0,columnspan=4, padx=5, pady=10)

    def show_error(self):
        utils.ErrorDialog(self, message='Failed to download product').show()

    def display_no_results(self):
        results_label = ctk.CTkLabel(self.offers_frame, text='No Results', font=('Helvetica', 18))
        results_label.grid(row=1, column=0, columnspan=4, padx=5, pady=10)

    def create_product(self, product_info):
        product = classes.Product(
            product_info['id'],
            product_info['name'],
            product_info['price'],
            product_info['description'],
            product_info['image'],
            product_info['items_available'],
            product_info['tags'],
            product_info['owner']
        )
        self.master.user.products.append(product)
        return product

    def get_products(self):
        url = f'http://localhost:8080/api/seller/{self.master.user.id}/product'
        try:
            response = requests.get(url)
            response.raise_for_status()
            products = response.json().get('content')
            self.master.after(0, self.display_products, products)
        except requests.RequestException:
            self.master.after(0, self.display_no_results)

    def display_products(self, products):
        if not products:
            self.display_no_results()
            return

        row, column = 1, 0
        for product_data in products:
            if column > 3:
                row += 1
                column = 0

            product = self.create_product(product_data)
            self.create_product_frame(product, row, column)
            column += 1

    def create_product_frame(self, product, row, column):
        product_frame = ctk.CTkFrame(self.offers_frame)
        product_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')
        ctk.CTkLabel(product_frame, text=f"{product.name}").pack()

        image_label = self.create_image_label(product.image, product_frame)
        image_label.pack()

        ctk.CTkLabel(product_frame, text=f"Price: ${product.price:.2f}").pack()
        ctk.CTkLabel(product_frame, text=f"Items available: {product.items_available}").pack()
        edit_command = partial(self.edit_product, product.id)
        ctk.CTkButton(product_frame, text='Edit', command=edit_command, fg_color='#382449',
                      hover_color='#301934').pack()

    def create_image_label(self, image_url, frame):
        image_data = urlopen(image_url).read()
        image_pil = Image.open(io.BytesIO(image_data))
        new_size = (80, 80)
        image_pil_resized = image_pil.resize(new_size, Image.LANCZOS)
        image_ctk = ctk.CTkImage(light_image=image_pil_resized, size=new_size)
        return ctk.CTkLabel(frame, image=image_ctk, text='')

    def edit_product(self, product_id):
        self.master.create_edit_product_frame(product_id)

    def log_out(self):
        dialog = utils.ConfirmDialog(self, title='Log Out', message='Are you sure you want to log out?')
        if dialog.show():
            self.master.create_login_frame()

    def quit(self):
        dialog = utils.ConfirmDialog(self, title='Quit', message='Are you sure you want to exit?')
        if dialog.show():
            self.master.quit()
