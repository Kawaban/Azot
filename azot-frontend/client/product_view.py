import requests
import customtkinter as ctk
import threading
from shared import utils
from urllib.request import urlopen
from PIL import Image
import io
from app_settings import *


class ProductView(ctk.CTkFrame):
    def __init__(self, master, product):
        super().__init__(master)
        self.master = master
        self.product = product

        self.setup_window()
        self.create_main_frame()
        self.create_label_frame()
        self.create_left_frame()
        self.create_right_frame()

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

    def create_label_frame(self):
        label_frame = ctk.CTkFrame(self.main_frame)
        label_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
        name_label = ctk.CTkLabel(label_frame, text='Product Name', font=('Helvetica', 16, 'bold'))
        name_label.pack()
        name_entry = ctk.CTkEntry(label_frame, justify='center', font=('Helvetica', 16, 'bold'), width=230)
        name_entry.insert(0, self.product.name)
        name_entry.configure(state='disabled')
        name_entry.pack()

    def create_left_frame(self):
        left_frame = ctk.CTkFrame(self.main_frame)
        left_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        self.create_label(left_frame, 'Price')
        price_entry = ctk.CTkEntry(left_frame, justify='center')
        price_entry.insert(0, f'{self.product.price:.2f}')
        price_entry.configure(state='disabled', )
        price_entry.pack()

        self.create_label(left_frame, 'Seller')
        seller_entry = ctk.CTkEntry(left_frame, justify='center')

        if self.product.owner['seller_info']['organization']:
            seller_entry.insert(0, self.product.owner['seller_info']['organization'])
        else:
            seller_entry.insert(0, 'Individual Seller')

        seller_entry.configure(state='disabled')
        seller_entry.pack()

        self.create_label(left_frame, 'Product Rating')

        rating = f'{self.product.avg_rating:.1f}' if self.product.avg_rating else 'No Ratings'
        rating_entry = ctk.CTkEntry(left_frame, justify='center')
        rating_entry.insert(0, rating)
        rating_entry.configure(state='disabled')
        rating_entry.pack()

        self.create_label(left_frame, 'Seller Rating')
        seller_rating_entry = ctk.CTkEntry(left_frame, justify='center')
        owner_avg_rating = self.product.owner.get('average_rating')
        seller_rating_entry.insert(0, f'{owner_avg_rating:.1f}' if owner_avg_rating else 'No Ratings')
        seller_rating_entry.configure(state='disabled')
        seller_rating_entry.pack()

        self.create_label(left_frame, 'Items Available')
        items_available_entry = ctk.CTkEntry(left_frame, justify='center')
        items_available_entry.insert(0, str(self.product.items_available))
        items_available_entry.configure(state='disabled')
        items_available_entry.pack()

        #ctk.CTkLabel(left_frame, text='').pack()

        ctk.CTkButton(left_frame, text='Add to cart', command=self.add_to_cart, fg_color='red', hover_color='#8B0000').pack(pady=20)

        #ctk.CTkButton(left_frame, text='Product reviews', command=lambda: self.master.create_review_read_frame(self.product,'product')).pack(pady=5)
        #ctk.CTkButton(left_frame, text='Seller reviews', command=lambda: self.master.create_review_read_frame(self.product,'seller')).pack(pady=5)

        ctk.CTkButton(left_frame, text='Back', command=self.master.create_client_main_frame).pack()
        #ctk.CTkButton(left_frame, text='Write Product Review', command=lambda: self.master.create_review_frame(self.product.id,'product')).pack(pady=10)
        #ctk.CTkButton(left_frame, text='Write Seller Review', command=lambda: self.master.create_review_frame(self.product.id,'seller')).pack(pady=10)

    def create_label(self, frame, text):
        label = ctk.CTkLabel(frame, text=text, font=('Helvetica', 16))
        label.pack(padx=5, pady=10)

    def create_right_frame(self):
        right_frame = ctk.CTkFrame(self.main_frame)
        right_frame.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        image_label = self.create_image_label(right_frame)
        image_label.pack(pady=10)

        description_textbox = ctk.CTkTextbox(right_frame, wrap='word', font=('Helvetica', 16), width=450, height=140)
        description_textbox.insert('1.0', self.product.description)
        description_textbox.configure(state='disabled')
        description_textbox.pack(padx=5, pady=10)

        ctk.CTkButton(right_frame, text='Product reviews', command=lambda: self.master.create_review_read_frame(self.product,'product')).pack(pady=8)
        ctk.CTkButton(right_frame, text='Seller reviews', command=lambda: self.master.create_review_read_frame(self.product,'seller')).pack(pady=8)

    def create_image_label(self, frame):
        image_url = self.product.image
        image_data = urlopen(image_url).read()
        image_pil = Image.open(io.BytesIO(image_data))
        new_size = (450, 230)
        image_pil_resized = image_pil.resize(new_size, Image.LANCZOS)
        image_ctk = ctk.CTkImage(light_image=image_pil_resized, size=new_size)
        return ctk.CTkLabel(frame, image=image_ctk, text='')

    def load_products(self):
        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/client/{self.master.user.id}/cart'
        response = requests.get(url)

        if response.status_code == 200:
            products_data = response.json().get('content', {}).get('orders', [])
            if products_data:
                self.master.user.cart.clear()
                for product_data in products_data:
                    quantity = product_data['quantity']
                    product = utils.create_product(product_data['product'])
                    product_tuple = (quantity, product)
                    self.master.user.cart.append(product_tuple)
        else:
            self.master.after(0, self.show_error, response)

    def add_to_cart(self):
        try:
            load_thread = threading.Thread(target=self.load_products)
            load_thread.start()

            value = utils.InputDialog(self, title='Add to cart', message='Enter the amount:').show()
            quantity = int(value)
            if quantity <= 0:
                raise ValueError

            load_thread.join()

            orders = []
            for product_tuple in self.master.user.cart:
                quantity, product = product_tuple
                orders.append({
                    'product': product.id,
                    'quantity': quantity
                })

            quantity = int(value)
            orders.append({
                'product': self.product.id,
                'quantity': quantity
            })

            data = {'orders': orders}

            url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/client/{self.master.user.id}/cart'
            response = requests.put(url, json=data)

            if response.status_code == 200:
                utils.InfoDialog(self, title='Success', message='Product added to cart').show()
            elif response.status_code == 400:
                utils.ErrorDialog(self, message=response.json()['error']).show()
            else:
                utils.ErrorDialog(self, message='Failed to add product to cart!').show()
        except ValueError:
            utils.ErrorDialog(self, message='Please enter a valid quantity!').show()
        except Exception as err:
            utils.ErrorDialog(self, message=f'Error occurred: {err}').show()

    def show_error(self, response):
        utils.ErrorDialog(self, message=response.json().get('error')).show()
