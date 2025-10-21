$(document).ready(function () {
    let timeout;

    $('.dropend').on({
        "mouseleave": function (){
            if ($(this).find('.dropdown-menu').hasClass("show")) {
                let aux = $(this)
                timeout = setTimeout(function (){
                    aux.click();
                },500);
            }
        },
        "mouseenter": function (){
            clearTimeout(timeout)
        }
    });
});

    /**
   * Menu isotope and filter
   */
  window.addEventListener('load', () => {
    let menuContainer = select('.menu-container');
    if (menuContainer) {
      let menuIsotope = new Isotope(menuContainer, {
        itemSelector: '.menu-item',
        layoutMode: 'fitRows'
      });

      let menuFilters = select('#menu-flters li', true);

      on('click', '#menu-flters li', function(e) {
        e.preventDefault();
        menuFilters.forEach(function(el) {
          el.classList.remove('filter-active');
        });
        this.classList.add('filter-active');

        menuIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        menuIsotope.on('arrangeComplete', function() {
          AOS.refresh()
        });
      }, true);
    }

  });