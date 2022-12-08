$(document).ready(function(){
    $('.slider').slick({
        arrows:false,
        slidesToShow: 4,
        slidesToScroll: 4,
        responsive:[
			{
				breakpoint: 768,
				settings: {
					slidesToShow:2,
					slidesToScroll: 2
				}
			},
			{
				breakpoint: 550,
				settings: {
					slidesToShow:1,
					slidesToScroll: 1
				}
			}
		]
    });

    $('.form-btn').submit(function (e) {
        e.preventDefault();
        var thisForm = this;
        var url = thisForm.action;
        var data = {};
        data.product_id = thisForm.dataset.product_id;
        var csrf_token = $('.form-btn [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            cache: true,
            success: function (data) {
                 console.log("OK");
                 if (data.total_items == 1) {
                     $('.page-header__icon-wrap').append('<div class="page-header__counter"><span id="total-items">{{ total_items }}</span></div>');
                 }
                 $('#total-items').text(data.total_items);
            }
        })
    });

});

document.addEventListener("DOMContentLoaded", onLoad);
function onLoad() {
    if (document.forms['filter'] != null) {
        document.forms['filter'].onsubmit = form_submit;
        document.forms['filter-reset'].onsubmit = form_submit_reset;
    }
    if (document.location.pathname == localStorage.getItem('pathname')) {
        for (var i = 0, arr_elements = document.forms['filter'].elements; i < arr_elements.length; i++) {
            var input = arr_elements[i];
            if (input.type == 'checkbox') {
                var checkbox = localStorage.getItem(i)
                if (checkbox == 'true') {
                    input.checked = true
                }
            } else {
                var number = localStorage.getItem(i)
                if (number != null) {
                    input.value = number
                }
            }
        }
    } else {
        window.localStorage.clear();
    }
}

function form_submit() {
    localStorage.setItem('pathname', document.location.pathname)
    for (var i = 0, arr_elements = document.forms['filter'].elements; i < arr_elements.length; i++) {
        var input = arr_elements[i];
        if (input.name) {
            var val = input.value.trim();
            if (input.type == 'checkbox') {
                localStorage.setItem(i, input.checked)
            } else {
                localStorage.setItem(i, val)
            }
            if (val === "" || +val === 0)
                input.disabled = true;
        }
    }
}

function form_submit_reset() {
    window.localStorage.clear();
}

