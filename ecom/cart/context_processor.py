def cart_total_amount(request):
    cart = request.session.get("cart", {})
    total = 0
    for item in cart.values():
        try:
            total += int(item.get("price", 0)) * int(item.get("quantity", 0))
        except (TypeError, ValueError):
            continue
    return {"cart_total_amount": total}
