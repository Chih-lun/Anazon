load();

function load(){
    // load cart data from localStorage
    var cart = localStorage.getItem("cart");
    // parse cart data into JSON format
    cart = JSON.parse(cart);

    // create item in dropdown cart
    var dropDown = $('#cart');

    // clear all the element at the beginning
    dropDown.html('');

    // check whether the cart is empty or not
    if (cart === null || Object.keys(cart).length === 0){
        // if cart is empty, show message and then clear cart element in localStorage
        dropDown.append("<li><span>Your cart is empty!</span></li>");
        localStorage.removeItem("cart");
    } else {
        // alphabetical sort primary keys
        var pks = Object.keys(cart).map(pk =>[pk, cart[pk]['title']]).sort((title1,title2) => title1[1].localeCompare(title2[1]));
        pks = pks.map(pk => Number(pk[0]));

        // generate each product
        for (var i=0; i<pks.length; i++){
            var pk = pks[i];
            var details = cart[pk];
            dropDown.append(`
            <li>
                <span class='dropdown-content'>
                    <h1>${details['title']}</h1>
                    <p>${details['quantity']}</p>
                    <button type="button" class="btn btn-primary" value="${pk}" onclick="append(this.value)">+</button>
                    <button type="button" class="btn btn-danger" value="${pk}" onclick="remove(this.value)">-</button>
                    <hr class="dropdown-divider">
                </span>
            </li>
            <li>
                <span class='dropdown-content'>
                    <button type="button" class="btn btn-primary" onclick="">View Cart</button>
                </span>
            </li>
            `);
        }
    }    
}

function addToCart(){
    // product information
    var pk = $("#product_pk").attr('value');
    var title = $("#product_title").attr('value');
    var image = $("#product_image").attr('src');
    var price = $("#product_price").attr('value');
    var quantity = $("#product_quantity").prop('value');
    
    // check whether the cart is empty or not, then decide whether create a new one
    var cart = localStorage.getItem("cart");
    if (cart !== null) {
        cart = JSON.parse(cart);
    } else {
        cart = {};
    }

    // check whether the product is in the cart or not, then decide whether create a new one
    var cartItem = cart[pk];
    if (cartItem === undefined){
        cartItem = {'title': title, 'image': image, 'price': price, 'quantity': Number(quantity)};
    } else {
        cartItem['quantity'] = Number(cartItem['quantity']) + Number(quantity);
    }

    // update cart
    cart[pk] = cartItem;

    // update localStorage
    localStorage.setItem("cart", JSON.stringify(cart));

    // refresh the html element
    load();
}

function append(pk){
    // get cart from localStorage
    var cart = localStorage.getItem("cart");
    cart = JSON.parse(cart);

    // get item from cart and increase it
    var cartItem = cart[pk];
    cartItem['quantity'] = Number(cartItem['quantity']) + 1;

    // update cart
    cart[pk] = cartItem;

    // update localStorage
    localStorage.setItem("cart", JSON.stringify(cart));

    // refresh the html element
    load();
}

function remove(pk){
    // get cart from localStorage
    var cart = localStorage.getItem("cart");
    cart = JSON.parse(cart);

    // get item from cart and decrease it
    var cartItem = cart[pk];
    cartItem['quantity'] = Number(cartItem['quantity']) - 1;

    // determine whether the quantity is below 0
    if (cartItem['quantity'] > 0){
        // update cart
        cart[pk] = cartItem;
    } else {
        // delete this item from cart
        delete cart[pk];
    }
    
    // update localStorage
    localStorage.setItem("cart", JSON.stringify(cart));

    // refresh the html element
    load();
}