class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if cart is None:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            image_url = ""
            if getattr(product, "images", None):
                try:
                    image_url = product.images.url
                except Exception:
                    image_url = ""
            self.cart[product_id] = {
                "name": product.product_name,
                "quantity": 0,
                "price": str(product.price),
                "image": image_url,
            }
        self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] -= quantity
            if self.cart[product_id]["quantity"] <= 0:
                del self.cart[product_id]
            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.save()

    def save(self):
        self.session.modified = True
