from shared import *
from client import *
from seller import *
from client import purchases_view
import customtkinter as ctk

# TODO add orders in seller
# TODO settings bugs

# TODO insert review buttons in purchase views
# TODO merge release brunch
# TODO merge develop-frontend brunch

# TODO bug: search -> enter any offer -> return to the menu -> duplicate offers appear


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Azot')
        window_size = utils.adjust_window(350, 350, self)
        self.geometry(window_size)
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')
        self.scaling = '100%'
        self.theme = 'Dark'
        self.fullscreen = 'Off'

        self.user = None
        self.user_type = None
        self.viewed_products = []

        self.login_frame = None
        self.registration_frame = None
        self.main_frame = None
        self.add_product_frame = None
        self.profile_frame = None
        self.settings_frame = None
        self.product_frame = None
        self.cart_frame = None
        self.forgot_password_frame = None
        self.purchases_frame = None
        self.review_frame = None
        self.review_read_frame = None

        self.create_login_frame()

    def create_login_frame(self):
        self.clear_frame()
        self.login_frame = login.LoginFrame(self)
        self.login_frame.pack(fill='both', expand=True)

    def create_registration_frame(self):
        self.clear_frame()
        self.registration_frame = register.RegistrationFrame(self)
        self.registration_frame.pack(fill='both', expand=True)

    def create_forgot_password_frame(self):
        self.clear_frame()
        self.forgot_password_frame = forgot_password.ForgotPasswordFrame(self)
        self.forgot_password_frame.pack(fill='both', expand=True)

    def create_seller_main_frame(self):
        self.clear_frame()
        self.main_frame = seller_menu.MainMenuFrame(self)
        self.main_frame.pack(fill='both', expand=True)

    def create_client_main_frame(self):
        self.clear_frame()
        self.main_frame = client_menu.MainMenuFrame(self)
        self.main_frame.pack(fill='both', expand=True)

    def create_client_profile_frame(self):
        self.clear_frame()
        self.profile_frame = client_profile.ProfileFrame(self)
        self.profile_frame.pack(fill='both', expand=True)

    def create_seller_profile_frame(self):
        self.clear_frame()
        self.profile_frame = seller_profile.ProfileFrame(self)
        self.profile_frame.pack(fill='both', expand=True)

    def create_add_product_frame(self):
        self.clear_frame()
        self.add_product_frame = add_product.AddProductFrame(self)
        self.add_product_frame.pack(fill='both', expand=True)

    def create_edit_product_frame(self, product_id):
        _product = None
        for product in self.user.products:
            if product_id == product.id:
                _product = product
        self.clear_frame()
        self.product_frame = edit_product_view.EditProductView(self, _product)
        self.product_frame.pack(fill='both', expand=True)

    def create_check_product_frame(self, product):
        self.clear_frame()
        self.product_frame = product_view.ProductView(self, product)
        self.product_frame.pack(fill='both', expand=True)

    def create_product_frame(self, product_id):
        _product = None
        for product in self.viewed_products:
            if product_id == product.id:
                _product = product
        self.clear_frame()
        self.product_frame = product_view.ProductView(self, _product)
        self.product_frame.pack(fill='both', expand=True)

    def create_cart_frame(self):
        self.clear_frame()
        self.cart_frame = cart_view.CartView(self)
        self.cart_frame.pack(fill='both', expand=True)

    def create_orders_frame(self):
        pass

    def create_purchases_frame(self):
        self.clear_frame()
        self.purchases_frame = purchases_view.PurchasesView(self)
        self.purchases_frame.pack(fill='both', expand=True)

    def create_settings_frame(self):
        self.clear_frame()
        self.settings_frame = settings.SettingsFrame(self)
        self.settings_frame.pack(fill='both', expand=True)

    def create_review_frame(self, product, review_type):
        self.clear_frame()
        self.review_frame = review.ReviewFrame(self, product, review_type)
        self.review_frame.pack(fill='both', expand=True)

    def create_review_read_frame(self, product, review_type):
        self.clear_frame()
        self.review_read_frame = read_review.ReviewReadFrame(self, product, review_type)
        self.review_read_frame.pack(fill='both', expand=True)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def quit(self):
        self.viewed_products.clear()
        self.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()
