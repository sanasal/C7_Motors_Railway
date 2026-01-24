(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);
    
    
    // Initiate the wowjs
    new WOW().init();


    $(document).ready(function () { 
        var $owl = $(".categories-carousel"); 
        $owl.owlCarousel({ 
            autoplay: true, 
            smartSpeed: 950, 
            dots: false, 
            loop: false, 
            margin: 25, 
            nav: true, 
            navText: [ 
                '<i class="fas fa-chevron-left"></i>', 
                '<i class="fas fa-chevron-right" id="next-right"></i>' 
            ], 
            responsiveClass: true, 
            responsive: { 
                0: { items: 1, nav: true }, 
                576: { items: 1, nav: true }, 
                768: { items: 1, nav: true }, 
                992: { items: 2, nav: true }, 
                1200:{ items: 4, nav: true } } }); 

            $owl.on("changed.owl.carousel", function (event) { 
                var current = event.item.index; 
                var total = event.item.count; 
                if (current === total - 1)
                    { $owl.trigger('stop.owl.autoplay'); } });
            $('.categories-carousel').find('.owl-next').on('click', function () { $owl.trigger('to.owl.carousel', [0, 300]); $owl.trigger('play.owl.autoplay'); }); });
    
})(jQuery);

function toggleReadMore(button) {
    const cardBody = button.closest('.card-body');
    const moreText = cardBody.querySelector('.more-text');

    moreText.classList.toggle('show');

    button.textContent = moreText.classList.contains('show')
        ? button.getAttribute('data-less-text')
        : button.getAttribute('data-more-text');
}
