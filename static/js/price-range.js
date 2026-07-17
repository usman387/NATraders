/*------------------------------------------------------------------
* Project:        EVdriveX - Electric Vehicle & Charging Station HTML Templates
* Author:         HtmlDesignTemplates
* URL:            https://themeforest.net/user/htmldesigntemplates
* Created:        04/04/2025
-------------------------------------------------------------------*/

(function ($) {
  "use strict";

  /* Price Range Slider */ 
const minPrice = document.getElementById('min-price');
const maxPrice = document.getElementById('max-price');
const minValue = document.getElementById('min-value');
const maxValue = document.getElementById('max-value');
const rangeSelected = document.querySelector('.range-selected');

if (!minPrice || !maxPrice || !minValue || !maxValue || !rangeSelected) {
    console.log("Price range elements are missing. Make sure they exist in the HTML.");
    return;
}

function updateRange() {
    let min = parseInt(minPrice.value);
    let max = parseInt(maxPrice.value);

    if (min > max) {
        [min, max] = [max, min];
        minPrice.value = min;
        maxPrice.value = max;
    }

    minValue.textContent = `$${min}`;
    maxValue.textContent = `$${max}`;

    const minPercent = (min / 100) * 100;
    const maxPercent = (max / 100) * 100;
    rangeSelected.style.left = `${minPercent}%`;
    rangeSelected.style.width = `${maxPercent - minPercent}%`;
}

minPrice.addEventListener('input', updateRange);
maxPrice.addEventListener('input', updateRange);
updateRange();


})(jQuery);
