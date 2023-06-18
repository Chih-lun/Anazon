loadCart();

if (checkCurrentURL('/cart_detail/')){
    loadCartDetail();
}

function getCart(){
    // load cart data from localStorage
    var cart = localStorage.getItem("cart");
    // check whether the cart is empty or not, then decide whether create a new one
    if (cart !== null) {
        // parse cart data into JSON format
        cart = JSON.parse(cart);
    } else {
        cart = {};
    }
    return cart;
}

function redirect(url){
    location.assign(url);
}

function checkCurrentURL(url){
    return window.location.pathname === url;
}


function loadCart(){
    var cart = getCart();

    // create item in dropdown cart
    var dropDown = $('#cart');

    // clear all the element at the beginning
    dropDown.html('');
    
    // check whether the cart is empty or not
    if (Object.keys(cart).length === 0){
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
            var productDetails = cart[pk];
            dropDown.append(`
            <li>
                <span class='dropdown-content'>
                    <h1>${productDetails['title']}</h1>
                    <p>${productDetails['quantity']}</p>
                    <button type="button" class="btn btn-primary" value="${pk}" onclick="append(this.value)">+</button>
                    <button type="button" class="btn btn-danger" value="${pk}" onclick="remove(this.value)">-</button>
                    <hr class="dropdown-divider">
                </span>
            </li>
            `);
        }

        dropDown.append(`
        <li>
            <span class='dropdown-content'>
                <button type="button" class="btn btn-primary" onclick="redirect('/cart_detail')">View Cart</button>
            </span>
        </li>
        `);
    }    
}

// for tomorrow
function loadCartDetail(){
    var detail = $("#cart_detail");
    
    // clear all the element at the beginning
    detail.html('');
    
    var cart = getCart();
    
    // check whether the cart is empty or not
    if (Object.keys(cart).length === 0){
        // if cart is empty, show message and then clear cart element in localStorage
        detail.append("<h1>Your cart is empty!</h1>");
    } else {
        // alphabetical sort primary keys
        var pks = Object.keys(cart).map(pk =>[pk, cart[pk]['title']]).sort((title1,title2) => title1[1].localeCompare(title2[1]));
        pks = pks.map(pk => Number(pk[0]));

        // generate each product
        for (var i=0; i<pks.length; i++){
            var pk = pks[i];
            var productDetails = cart[pk];
            detail.append(`
            <label>${productDetails['title']}</label>
            <input type="number" name="${pk}" value="${productDetails['quantity']}" min="1" step="1" onchange="updateCartItem(this.name, this.value)"></input>
            <button type="button" class="btn btn-primary" value="${pk}" onclick="append(this.value)">+</button>
            <button type="button" class="btn btn-danger" value="${pk}" onclick="remove(this.value)">-</button>
            <button type="button" class="btn btn-danger" value="${pk}" onclick="clearCartItem(this.value)">clear</button>
            <hr>
            `);
        }

        detail.append(`
        <input type="submit" class="btn btn-primary" value="Checkout">
        `)
    }
}

function addToCart(){
    // product information
    var pk = $("#product_pk").attr('value');
    var title = $("#product_title").attr('value');
    var image = $("#product_image").attr('src');
    var price = $("#product_price").attr('value');
    var quantity = $("#product_quantity").prop('value');
    
    var cart = getCart();

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
    loadCart();
}

function append(pk){
    var cart = getCart();

    // get item from cart and increase it
    var cartItem = cart[pk];
    cartItem['quantity'] = Number(cartItem['quantity']) + 1;

    // update cart
    cart[pk] = cartItem;

    // update localStorage
    localStorage.setItem("cart", JSON.stringify(cart));

    // refresh the html element
    loadCart();

    if (checkCurrentURL('/cart_detail/')){
        loadCartDetail();
    }
}

function remove(pk){
    var cart = getCart();

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
    loadCart();

    if (checkCurrentURL('/cart_detail/')){
        loadCartDetail();
    }
}


function updateCartItem(pk, quantity){
    if (quantity < 1) {
        quantity = 1;
    }

    var cart = getCart();

    // get item from cart and increase it
    var cartItem = cart[pk];
    cartItem['quantity'] = Number(quantity);

    // update cart
    cart[pk] = cartItem;

    // update localStorage
    localStorage.setItem("cart", JSON.stringify(cart));

    // refresh the html element
    loadCart();

    if (checkCurrentURL('/cart_detail/')){
        loadCartDetail();
    }
}

function clearCartItem(pk){
    var cart = getCart();
    
    // delete this item from cart
    delete cart[pk];
    
    // update localStorage
    localStorage.setItem("cart", JSON.stringify(cart));

    // refresh the html element
    loadCart();

    if (checkCurrentURL('/cart_detail/')){
        loadCartDetail();
    }
}