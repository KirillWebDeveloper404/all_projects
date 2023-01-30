
// slider
$(document).ready(function(){
    $('.slider-offer').slick({
        dots: true,
        infinite: true,
        speed: 800,
        arrows: false,
        autoplay: true,
        slidesToShow: 1,
        centerMode: true,
        variableWidth: true
    });
});

$(document).ready(function(){
    $('.slider-car').slick({
        dots: false,
        infinite: true,
        speed: 800,
        arrows: false,
		autoplay: true,
        slidesToShow: 2,
        responsive: [
            {
              breakpoint: 992,
              settings: {
                slidesToShow: 1
              }
            },
            {
                breakpoint: 320,
                settings: {
                  slidesToShow: 1,
                  centerMode: true
            
                }
              }
          ]
    });
});

$(document).ready(function(){
    $('.slick-img').slick({
        dots: false,
        infinite: true,
        speed: 300,
        arrows: true,
        slidesToShow: 1
    });
});


// hamburger 
$('.menu-open').click(function (e) {
    e.preventDefault;
    $(this).toggleClass('menu-open_active');
    $('.menu-collapse').toggleClass('d-none').css('order', '1')
    $('.menu-header').toggleClass('menu-opened');
});


//плавная прокрутка 

	$(".menu__list a").click(function() {
	var elementClick = $(this).attr("href")
	var destination = $(elementClick).offset().top;
	jQuery("html:not(:animated),body:not(:animated)").animate({
		scrollTop: destination
	}, 800);
	return false;
});

//arrow

$(".arrow-top").click(function() {
    var body = $("html, body");
    body.stop().animate({scrollTop:0}, 800, 'swing', function() {});
});




 