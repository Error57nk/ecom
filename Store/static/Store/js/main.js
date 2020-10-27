
$(document).ready(function () {


    $('.home-case').owlCarousel({
        items: 1,
        margin: 0,
        autoHeight: true,
        autoplay: true,
        autoplayTimeout: 4000,
        nav: true,
        dots: false,
        navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
        loop: true,
        smartSpeed: 500,
        animateOut: 'fadeOut',
    });
    $('.item-products').owlCarousel({
        items: 6,
        margin: 0,
        autoHeight: true,
        nav: true,
        dots: false,
        navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
        touchDrag: false,

        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                nav: true
            },
            400: {
                items: 2,
                nav: true
            },
            600: {
                items: 4,
                nav: false
            },
            1000: {
                items: 6,
                nav: true,
                loop: false
            }
        }
    });

    const toTop = document.querySelector(".nscroller");
    const lower_nav = document.querySelector(".lower-nav");
    window.addEventListener("scroll", () => {
        if (window.pageYOffset > 100) {
            toTop.classList.add("active");
            lower_nav.classList.add("active");
        } else {
            toTop.classList.remove("active");
            lower_nav.classList.remove("active");
        }
    })

    $('ul li').click(function () {
        $(this).siblings().removeClass('active')
        $(this).toggleClass('active')
    })






})

$(".custom-file-input").on("change", function () {
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});
$('.content, .sidebar').theiaStickySidebar({
    // Settings
    additionalMarginTop: 77
});
var sh_cat = true;
function cattoggler() {

    if (sh_cat) {
        $(".nav-cat-nav").css("width", "50%");
        sh_cat = false;
    } else {
        $(".nav-cat-nav").css("width", "0px");
        sh_cat = true;
    }

}

// console.log("");

var updateBtns = document.getElementsByClassName('update-cart')
for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action

        console.log('productId: ', productId, 'action: ', action);

        console.log('USER: ', user)
        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            // console.log('User Loged in sending data');
            updateUserOrder(productId, action)
        }


    })
}

function addCookieItem(productId, action) {
    console.log('Not Loged In-----');

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }
        } else {
            cart[productId]['quantity'] += 1
        }
    }
    if (action == 'remove') {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log("Removing the item")
            delete cart[productId]
        }
    }
    console.log('Cart: ', cart)
    document.cookie = 'cart =' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload()
}


function updateUserOrder(productId, action) {
    console.log('User is Looged in, Sending data.. ')
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data:', data);
            location.reload()

        })

}