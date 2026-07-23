/*------------------------------------------------------------------
* Project:        EVdriveX - Electric Vehicle & Charging Station HTML Templates
* Author:         HtmlDesignTemplates
* URL:            https://themeforest.net/user/htmldesigntemplates
* Created:        04/04/2025
-------------------------------------------------------------------*/

console.log("EVdriveX - Electric Vehicle & Charging Station HTML Templates");

(function ($) {
  "use strict";

  /* ========================================
     SEARCH POPUP
     ======================================== */
  $('a[href="#search1"]').on('click', function(event) {
    event.preventDefault();
    $('#search1').addClass('open');
    $('#search1 input').focus();
  });

  $('#search1, #search1 button.close').on('click keyup', function(event) {
    if (event.target == this || $(event.target).hasClass('close') || event.keyCode == 27) {
      $('#search1').removeClass('open');
    }
  });

  /* ========================================
     SLICKNAV RESPONSIVE MENU
     ======================================== */
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

  /* ========================================
     DROPDOWN MENU
     ======================================== */
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

  /* ========================================
     SPIN ANIMATION FOR BANNER
     ======================================== */
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
          void letterSpan.offsetWidth;
          letterSpan.classList.add('spin');
      });
  }

  listItems.forEach((item, i) => {
      item.textContent = words[0][i] || '';
  });
  updateWords();

  /* ========================================
     COUNTER JS
     ======================================== */
  document.querySelectorAll(".num").forEach(valueDisplay => {
    let startValue = 0;
    let endValue = parseInt(valueDisplay.getAttribute("data-val"), 10);
    let duration = Math.max(Math.floor(2000 / endValue), 1);
    let counter = setInterval(() => {
        valueDisplay.textContent = ++startValue;
        if (startValue === endValue) clearInterval(counter);
    }, duration);
  });

  /* ========================================
     SLICK SLIDERS
     ======================================== */
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
      { breakpoint: 480, settings: { slidesToShow: 1, slidesToScroll: 1 } }
    ]
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

  /* ========================================
     COUNTER FOR PROGRESS BAR
     ======================================== */
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

  /* ========================================
     LIGHT GALLERY FOR GALLERY SECTION
     ======================================== */
  if (document.getElementById('lightgallery-video')) {
    lightGallery(document.getElementById('lightgallery-video'), {
      plugins: [lgVideo],
      speed: 500,
      videoMaxWidth: '1000px',
    });
  }

  /* ========================================
     BACK-TO-TOP
     ======================================== */
  $(document).ready(() => {
    $('#back-to-top').hide();

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

  /* ========================================
     STICKY HEADER
     ======================================== */
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

/* ========================================
   COLOR SWATCHES - SELECTABLE CIRCLES
   ======================================== */

(function() {
  'use strict';

  document.addEventListener('DOMContentLoaded', function() {

      const swatchesWrapper = document.getElementById('colorSwatchesWrapper');
      if (!swatchesWrapper) return;

      const swatches = swatchesWrapper.querySelectorAll('.color-swatch-btn');
      const selectedColorInput = document.getElementById('selectedColor');
      const selectedColorText = document.getElementById('selectedColorText');

      let selectedColor = '';

      // Function to detect if color is dark
      function isDarkColor(hex) {
          let color = hex;

          // Remove # if present
          if (color.startsWith('#')) {
              color = color.slice(1);
          }

          // Expand shorthand (e.g., #fff -> #ffffff)
          if (color.length === 3) {
              color = color.split('').map(c => c + c).join('');
          }

          // Parse RGB values
          const r = parseInt(color.substring(0, 2), 16);
          const g = parseInt(color.substring(2, 4), 16);
          const b = parseInt(color.substring(4, 6), 16);

          // Calculate luminance
          const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;

          return luminance < 0.5;
      }

      // Function to get color display name
      function getColorDisplayName(color) {
          // If it's a hex color, show it as is
          if (color.startsWith('#')) {
              return color.toUpperCase();
          }
          // Capitalize first letter
          return color.charAt(0).toUpperCase() + color.slice(1);
      }

      // Function to select a color
      function selectColor(swatch, color) {
          // Remove selected from all swatches
          swatches.forEach(s => s.classList.remove('selected'));

          // Add selected to current swatch
          swatch.classList.add('selected');

          // Update hidden input
          if (selectedColorInput) {
              selectedColorInput.value = color;
          }

          // Update display text
          if (selectedColorText) {
              selectedColorText.innerHTML = 'Selected: <span class="color-name">' + getColorDisplayName(color) + '</span>';
              selectedColorText.classList.add('active');
          }

          // Store selected color
          selectedColor = color;

          // Trigger custom event
          const event = new CustomEvent('colorSelected', {
              detail: { color: color }
          });
          document.dispatchEvent(event);

          console.log('🎨 Color selected:', color);
      }

      // Function to deselect color
      function deselectColor() {
          swatches.forEach(s => s.classList.remove('selected'));

          if (selectedColorInput) {
              selectedColorInput.value = '';
          }

          if (selectedColorText) {
              selectedColorText.textContent = 'No color selected';
              selectedColorText.classList.remove('active');
          }

          selectedColor = '';

          console.log('🔄 Color deselected');
      }

      // Loop through each swatch
      swatches.forEach(swatch => {
          const color = swatch.dataset.color;

          // Detect if color is dark
          if (isDarkColor(color)) {
              swatch.setAttribute('data-dark', 'true');
          }

          // Click event - Toggle selection
          swatch.addEventListener('click', function(e) {
              e.stopPropagation();
              const colorValue = this.dataset.color;

              // If already selected, deselect it
              if (this.classList.contains('selected')) {
                  deselectColor();
              } else {
                  selectColor(this, colorValue);
              }
          });

          // Hover event - Glow effect
          swatch.addEventListener('mouseenter', function() {
              const color = this.dataset.color;
              if (!this.classList.contains('selected')) {
                  this.style.boxShadow = `0 0 20px ${color}55, 0 4px 12px rgba(0,0,0,0.1)`;
              }
          });

          swatch.addEventListener('mouseleave', function() {
              if (this.classList.contains('selected')) {
                  this.style.boxShadow = '0 0 0 3px rgba(17, 160, 73, 0.25), 0 4px 14px rgba(0,0,0,0.12)';
              } else {
                  this.style.boxShadow = '0 2px 6px rgba(0,0,0,0.06)';
              }
          });
      });

      // If there's a preselected color from backend
      if (selectedColorInput) {
          const preselectedColor = selectedColorInput.value;
          if (preselectedColor) {
              swatches.forEach(swatch => {
                  if (swatch.dataset.color === preselectedColor) {
                      selectColor(swatch, preselectedColor);
                  }
              });
          }
      }

      // Expose functions globally
      window.getSelectedColor = function() {
          return selectedColor;
      };

      window.resetColorSelection = function() {
          deselectColor();
      };

      window.setColorSelection = function(color) {
          swatches.forEach(swatch => {
              if (swatch.dataset.color === color) {
                  selectColor(swatch, color);
              }
          });
      };

      console.log('🟢 Color Swatches initialized successfully!');
      console.log('📌 Available colors:', Array.from(swatches).map(s => s.dataset.color));

  });

})();