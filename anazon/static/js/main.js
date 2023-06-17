load();

function load(){
    var cart = localStorage.getItem("cart");
    cart = JSON.parse(cart);
    
    var dropDown = $('#cart');
    dropDown.html('');

    if (cart === null || Object.keys(cart).length === 0){
        dropDown.append("<li><span>Your cart is empty!</span></li>");
        localStorage.removeItem("cart");
    } else {
        for (var pk in cart){
            details = cart[pk];
            dropDown.append(`
            <li>
                <span class='dropdown-content'>
                    <h1>${details['title']}</h1>
                    <p>${details['quantity']}</p>
                    <button type="button" class="btn btn-primary" value="${pk}" onclick="append(this.value)">+</button>
                    <button type="button" class="btn btn-danger" value="${pk}" onclick="remove(this.value)">-</button>
                    <hr class="dropdown-divider">
                </span>
            </li>`);
        }
    }    
}

function addToCart(){
    var pk = $("#product_pk").attr('value');
    var title = $("#product_title").attr('value');
    var image = $("#product_image").attr('src');
    var price = $("#product_price").attr('value');
    var quantity = $("#product_quantity").prop('value');

    var cart = localStorage.getItem("cart");
    if (cart !== null) {
        cart = JSON.parse(cart);
    } else {
        cart = {};
    }

    var cartItem = cart[pk];
    if (cartItem === undefined){
        cartItem = {'title': title, 'image': image, 'price': price, 'quantity': Number(quantity)};
    } else {
        cartItem['quantity'] = Number(cartItem['quantity']) + Number(quantity);
    }
    cart[pk] = cartItem;

    localStorage.setItem("cart", JSON.stringify(cart));
    load();
}

function append(pk){
    var cart = localStorage.getItem("cart");
    cart = JSON.parse(cart);
    var cartItem = cart[pk];
    cartItem['quantity'] = Number(cartItem['quantity']) + 1;
    cart[pk] = cartItem;
    localStorage.setItem("cart", JSON.stringify(cart));
    load();
}

function remove(pk){
    var cart = localStorage.getItem("cart");
    cart = JSON.parse(cart);
    var cartItem = cart[pk];
    cartItem['quantity'] = Number(cartItem['quantity']) - 1;
    if (cartItem['quantity'] > 0){
        cart[pk] = cartItem;
    } else {
        delete cart[pk];
    }
    
    localStorage.setItem("cart", JSON.stringify(cart));
    load();
}