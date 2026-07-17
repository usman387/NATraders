/*------------------------------------------------------------------
* Project:        EVdriveX - Electric Vehicle & Charging Station HTML Templates
* Author:         HtmlDesignTemplates
* URL:            https://themeforest.net/user/htmldesigntemplates
* Created:        04/04/2025
-------------------------------------------------------------------*/
console.log("EVdriveX - Electric Vehicle & Charging Station HTML Templates");
(function ($) {
  "use strict";

  /*//For Popup search start//*/
  $('a[href="#search1"]').on('click', function(event) {
    event.preventDefault();
    $('#search1').addClass('open');
    $('#search1 input').focus(); // Focus on the input field
  });

  $('#search1, #search1 button.close').on('click keyup', function(event) {
    if (event.target == this || $(event.target).hasClass('close') || event.keyCode == 27) {
      $('#search1').removeClass('open');
    }
  });

  /* SlickNav Responsive Menu */
  $('#responsive-menu').slicknav({
    duration: 500,
    easingOpen: 'easeInExpo',
    easingClose: 'easeOutExpo',
    closedSymbol: '<i class="arrow-indicator fa fa-angle-down"></i>',
    openedSymbol: '<i class="arrow-indicator fa fa-angle-up"></i>',
    prependTo: '#slicknav-mobile',
    allowParentLinks: true,
    label: ""
  });

  /* Dropdown Menu */
  var selected = $('#navbar li');
  selected.on("mouseenter", function () {
      $(this).find('ul').first().stop(true, true).delay(350).slideDown(500, 'easeInOutQuad');
  }).on("mouseleave", function () {
      $(this).find('ul').first().stop(true, true).delay(100).slideUp(150, 'easeInOutQuad');
  });

  /* Arrow Indicator for Submenus */
  if ($(window).width() > 992) {
      $(".navbar-arrow ul ul > li").has("ul").children("a").append("<i class='arrow-indicator fa fa-angle-right'></i>");
  }

  /* Spin Animation For Banner */
  const listItems = document.querySelectorAll('.spin');
  const words = ['faster', 'bigger', 'better'];
  let currentWordIndex = 0;

  function updateWords() {
      listItems.forEach((item, index) => {
          item.style.animationDelay = `${index * 0.1}s`;
          if (index === listItems.length - 1) {
              item.addEventListener('animationend', handleAnimationEnd);
          }
      });
  }

  function handleAnimationEnd() {
      currentWordIndex = (currentWordIndex + 1) % words.length;
      const nextWord = words[currentWordIndex];
      
      listItems.forEach((letterSpan, i) => {
          letterSpan.textContent = nextWord[i] || '';
          letterSpan.classList.remove('spin');
          void letterSpan.offsetWidth; // Trigger reflow
          letterSpan.classList.add('spin');
      });
  }

  listItems.forEach((item, i) => {
      item.textContent = words[0][i] || ''; // Set initial word
  });
  updateWords();

  /* Counter JS */
  document.querySelectorAll(".num").forEach(valueDisplay => {
    let startValue = 0;
    let endValue = parseInt(valueDisplay.getAttribute("data-val"), 10);
    let duration = Math.max(Math.floor(2000 / endValue), 1);
    let counter = setInterval(() => {
        valueDisplay.textContent = ++startValue;
        if (startValue === endValue) clearInterval(counter);
    }, duration);
  });

  /* Slick Sliders */
  $('.partner-slider').slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2500,
    arrows: false,
    dots: false,
    responsive: [
      { breakpoint: 1100, settings: { slidesToShow: 3, slidesToScroll: 1 } },
      { breakpoint: 600, settings: { slidesToShow: 2, slidesToScroll: 1 } },
      { breakpoint: 480, settings: { slidesToShow: 1, slidesToScroll: 1 } }]
  });

  $('.review-slider').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2500,
    arrows: false,
    dots: false,
  });      

  $('.slider-for').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    draggable: false,
    asNavFor: '.slider-nav'
  });

  $('.slider-nav').slick({
    slidesToShow: 4,
    slidesToScroll: 0,
    asNavFor: '.slider-for',
    dots: false,
    arrows: false,
    centerMode: true,
    focusOnSelect: true,
    responsive: [
      { breakpoint: 600, settings: { slidesToShow: 3, slidesToScroll: 1 } }
    ]
  });

  $('.banner-slider').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2500,
    arrows: false,
    dots: true,
  });

  $('.price-slider').slick({
    slidesToShow: 2,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2500,
    arrows: false,
    dots: true,
    responsive: [
      { breakpoint: 600, settings: { slidesToShow: 1, slidesToScroll: 1 } }
    ]
  });

  $('.project-slider').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2500,
    arrows: false,
    dots: false,
    responsive: [
      { breakpoint: 1200, settings: { slidesToShow: 2, slidesToScroll: 1 } },
      { breakpoint: 600, settings: { slidesToShow: 1, slidesToScroll: 1 } }
    ]
  });

  $('.testimonial-slider').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: false,
    autoplaySpeed: 2500,
    arrows: false,
    dots: true,
  });

  $('.news-slider').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: false,
    autoplaySpeed: 2500,
    arrows: false,
    dots: true,
  }); 

  /* Counter for progress bar start */
  let valueDisplayss = document.querySelectorAll(".progress-num");
  let intervall = 3000;

  valueDisplayss.forEach((valueDisplay) => {
      let startValue = 0;
      let endValue = parseInt(valueDisplay.getAttribute("data-val"));
      let duration = Math.floor(intervall / endValue);
      let counter = setInterval(function() {
          startValue += 1;
          valueDisplay.textContent = startValue;
          if (startValue == endValue) {
              clearInterval(counter);
          }
      }, duration);
  });

  /* Light Gallery For Gallery section Start */
  lightGallery(document.getElementById('lightgallery-video'), {
    plugins: [lgVideo],
    speed: 500,
    videoMaxWidth: '1000px',
  });  

  /* Back-to-top js Start */
  $(document).ready(() => {
    $('#back-to-top').hide(); // Hide button initially

    $(window).on('scroll', () => {
        if ($(window).scrollTop() > 500) {
            $('#back-to-top').fadeIn(200);
        } else {
            $('#back-to-top').fadeOut(200);
        }
    });

    $(document).on('click', '#back-to-top, .back-to-top', () => {
        $('html, body').animate({
            scrollTop: 0
        }, 500);
        return false;
    });
  }); 

  /* Sticky Header */
  let $headerMenu = $('.header-nav-menu');

    $(window).on('scroll', function () {
        let curScroll = $(window).scrollTop();

        if (curScroll > 130) {
            $headerMenu.addClass('navbar-sticky-in');
        } else {
            $headerMenu.removeClass('navbar-sticky-in');
        }
    });

})(jQuery);
