$(document).ready(function ($) {
  $.cookie.raw = true;
  $.cookie.json = true;


  if ($.cookie("shopping-cart")) {
    $('.shopping-cart').attr('attr-count', Object.keys(JSON.parse($.cookie("shopping-cart"))).length);
  } else {
    $('.shopping-cart').attr('attr-count', 0);
  }

  $('.to-shopping-cart').on('click', function (e) {
    e.preventDefault();
    if ($.cookie('shopping-cart')) {
      let k = 0;
      let basketItems = $.makeArray(JSON.parse($.cookie('shopping-cart')));
      let basketItem = { id: $(this).closest('.catalog__item, .card__info').attr('product-id'), count: $(this).closest('.catalog__item, .card__info').find('.catalog__count input').val() };
      for (let i = 0; i < basketItems.length; i++) {
        if (basketItems[i].id == $(this).closest('.catalog__item, .card__info').attr('product-id')) {
          basketItems[i].count = (parseFloat(basketItems[i].count) + parseFloat($(this).siblings('.catalog__count, .card__price-and-delivery').find('input').val()));
          k++;
        }
      } if (k == 0) {
        basketItems.push(basketItem);
        $('.shopping-cart').attr('attr-count', parseInt($('.shopping-cart').attr('attr-count')) + 1);
      }
      $.cookie('shopping-cart', basketItems, { path: '/', expires: 7 });
    } else {
      let basketItem = { id: $(this).closest('.catalog__item, .card__info').attr('product-id'), count: $(this).siblings('.catalog__count, .card__price-and-delivery').find('input').val() };
      let basketItems = [];
      basketItems.push(basketItem);
      $('.shopping-cart').attr('attr-count', parseInt($('.shopping-cart').attr('attr-count')) + 1);
      $.cookie('shopping-cart', basketItems, { path: '/', expires: 7 });
    }
  });

  $('.shop-cart__delete').on('click', function () {
    let basketItems = $.makeArray(JSON.parse($.cookie('shopping-cart')));
    let newBasketItems = [];
    for (let i = 0; i < basketItems.length; i++) {
      if (basketItems[i].id != $(this).closest('.shop-cart__item').attr('product-id')) {
        newBasketItems.push(basketItems[i]);
      }
    }
    $('.shopping-cart').attr('attr-count', parseInt($('.shopping-cart').attr('attr-count')) - 1);
    $.cookie('shopping-cart', newBasketItems, { path: '/', expires: 7 });
    location.reload();
  });

  $('.shop-cart__delete-all').on('click', function () {
    $('.shop-cart__item .filter__checkbox.active').each(function () {
      let basketItems = $.makeArray(JSON.parse($.cookie('shopping-cart')));
      let newBasketItems = [];
      for (let i = 0; i < basketItems.length; i++) {
        if (basketItems[i].id != $(this).closest('.shop-cart__item').attr('product-id')) {
          newBasketItems.push(basketItems[i]);
        }
      }
      $('.shopping-cart').attr('attr-count', parseInt($('.shopping-cart').attr('attr-count')) - 1);
      $.cookie('shopping-cart', newBasketItems, { path: '/', expires: 7 });
    });
    location.reload();
  });

  $('.filter__checkbox[name="select-all"]').on('click', function () {
    if ($(this).hasClass('active')) {
      $('.shop-cart__items .filter__checkbox').removeClass('active');
    } else {
      $('.shop-cart__items .filter__checkbox').addClass('active');
    }
  });

  var search = window.location.search.split('?')[1];
  if (search) {
    var arrFiltred = search.replace('/', '').split('&');
    for (let i = 0; i < arrFiltred.length; i++) {
      let optionId = arrFiltred[i].split('=')[0];
      let paramIdArr = arrFiltred[i].split('=')[1].split(':');
      if ($('[option-id="' + optionId + '"]').hasClass('filter__checkboxs')) {
        for (let j = 0; j < paramIdArr.length; j++) {
          $('[option-id="' + optionId + '"]').find('[option-value-id="' + paramIdArr[j] + '"]').addClass('active');
        }
      } else {
        $('[option-id="' + optionId + '"]').find('.close').addClass('active');
        $('[option-id="' + optionId + '"]').find('[name="min"]').val(paramIdArr[0]);
        $('[option-id="' + optionId + '"]').find('[name="max"]').val(paramIdArr[1]);
      }
    }
    if (search.split('filter=')[1] == 'maintenance') {
      $('.custom-select span').html('обслуживание');
    }
    if (search.split('filter=')[1] == 'repair') {
      $('.custom-select span').html('сервис');
    }
    if (search.split('filter=')[1] == 'sell') {
      $('.custom-select span').html('продажи');
    }
    if (search.split('filter=')[1] == 'all') {
      $('.custom-select span').html('сервис и обслуживание');
    }
  }

  $('.filter__title span').on('click', function () {
    document.location.href = window.location.pathname;
  });

  $('.filter .filter__checkbox').on('click', function () {
    $('.filter-apply').addClass('active');
  });

  $('.filter__range .close').on('click', function () {
    $(this).removeClass('active');
    $('.filter-apply').addClass('active');
    $(this).closest('.filter__range').find('input').val('');
  });

  $('.filter__inputs input').keyup(function () {
    $('.filter-apply').addClass('active');
    $(this).closest('.filter__range').find('.close').addClass('active');
  });

  $('.filter__inputs input').on('change', function () {
    let pattern = new RegExp(/^[0-9]*[.,]?[0-9]+$/)
    if (pattern.test($(this).val()) == false && $(this).val() != '') {
      $(this).val($(this).attr('valide-value'));
    }
    if ($(this).attr('name') == 'min') {
      if (parseFloat($(this).val()) < parseFloat($(this).attr('valide-value'))) {
        $(this).val(parseFloat($(this).attr('valide-value')));
      } else if (parseFloat($(this).val()) > parseFloat($(this).siblings().attr('valide-value'))) {
        $(this).val(parseFloat($(this).attr('valide-value')));
      }
    } else {
      if (parseFloat($(this).val()) > parseFloat($(this).attr('valide-value'))) {
        $(this).val(parseFloat($(this).attr('valide-value')));
      } else if (parseFloat($(this).val()) < parseFloat($(this).siblings().attr('valide-value'))) {
        $(this).val(parseFloat($(this).attr('valide-value')));
      }

    }
    if ($(this).val() == '' && $(this).siblings().val() == '') {
      $(this).closest('.filter__range').find('.close').removeClass('active');
    }
  });

  getFilterLink = () => {
    let filterLink = window.location.pathname + '?';
    $('[option-id]').each(function () {
      if ($(this).hasClass('filter__checkboxs') && $(this).children().hasClass('active')) {
        filterLink += $(this).attr('option-id') + '='
        $(this).find('.active').each(function () {
          filterLink += $(this).attr('option-value-id') + ':';
        })
        filterLink = filterLink.slice(0, -1);
        filterLink += '&';
      } else
        if ($(this).hasClass('filter__range')) {
          if ($(this).find('[name="min"]').val() != '' && $(this).find('[name="max"]').val() != '') {
            filterLink += $(this).attr('option-id') + '=' + $(this).find('[name="min"]').val() + ':' + $(this).find('[name="max"]').val() + '&';
          } else if ($(this).find('[name="min"]').val() == '' && $(this).find('[name="max"]').val() != '') {
            filterLink += $(this).attr('option-id') + '=' + '' + ':' + $(this).find('[name="max"]').val() + '&';
          } else if ($(this).find('[name="min"]').val() != '' && $(this).find('[name="max"]').val() == '') {
            filterLink += $(this).attr('option-id') + '=' + $(this).find('[name="min"]').val() + ':' + '' + '&';
          }
        }
    });
    filterLink = filterLink.slice(0, -1);
    return filterLink;
  }

  $('.filter-apply').on('click', function () {
    if (window.location.search.includes('page')) {
      if (getFilterLink() == window.location.pathname) {
        document.location.href = "?page=" + window.location.search.split('page=')[1];
      } else {
        document.location.href = getFilterLink() + "&page=" + window.location.search.split('page=')[1];
      }
    } else document.location.href = getFilterLink();
  });


  $('.pagination a').on('click', function (e) {
    if (window.location.search != '') {
      e.preventDefault();
      if (getFilterLink() == window.location.pathname) {
        document.location.href = "?" + $(this).attr('href').split('?')[1];
      } else {
        document.location.href = getFilterLink() + "&" + $(this).attr('href').split('?')[1];
      }
    }
  });

  $(document).on('scroll', function () {
    if ($('.catalog .filter').length != 0) {
      if ((($('.filter').offset().top + $('.filter').height()) - (window.innerHeight + window.scrollY) + 70) < 0) {
        $('.filter-apply').addClass('posAbs');
      } else {
        $('.filter-apply').removeClass('posAbs');
      }
      /*  console.log($('.filter').offset().top);
       console.log(window.scrollY);
       if (window.scrollY >= 141) {
         $('.filter').addClass('posAbs').css('top', window.scrollY - 150 + 'px');
       } else {
         $('.filter').removeClass('posAbs');
       } */
    }
    if (window.scrollY > 300) {
      $('.to-header').removeClass('hidden');
    } else {
      $('.to-header').addClass('hidden');
    }
  });

  $('.armClockPage_block').css('filter', 'blur(0px)');

  $('.our-team__item').on('click', function () {
    $('.modal, .team-form[worker-id="' + $(this).attr('worker-id') + '"]').addClass('active');
  });
  $('.show-certificate').on('click', function (e) {
    e.preventDefault();
    $('.modal, .card-certificate-slider').addClass('active');
  });
  $('.certificates__slide img, .reviews__slider img, .reviews-page__img, .card__slider-main img, .project__slide img').on('click', function () {
    $('.card-certificate-slider').removeClass('active');
    if ($(this).hasClass('slider-img')) {
      $('.certificates-form').addClass('w55');
    }
    $('.certificates-form .form-img').attr('src', $(this).attr('src'));
    $('.modal, .certificates-form').addClass('active');
  });

  $('.card__gallery img').on('click', function () {
    $('.card-certificate-slider').removeClass('active')
    $('.certificates-form').addClass('w55');
    $('.certificates-form .form-img').attr('src', $(this).attr('src'));
    $('.modal, .certificates-form').addClass('active');
  });


  $('.modal .close').on('click', function () {
    $('.modal, .team-form, .certificates-form, .success').removeClass('active').removeClass('w55');
  });

  $('#sort').on('click', function () {
    $(this).siblings('.custom-select').toggleClass('active');
  });

  $('#sort').on('change', function () {
    $(this).siblings('.custom-select').find('span').html($(this).find('option:selected').text());
    if ($(this).val() != 'ALL') {
      document.location.href = document.location.pathname + '?filter=' + $(this).val().toLowerCase();
    } else {
      document.location.href = document.location.pathname;
    }
  });


  $('.feedback__checkbox').on('click', function () {
    $(this).find('.feedback__check').toggleClass('active');
  });

  $('.card__thumb').on('click', function () {
    $(this).addClass('active').siblings().removeClass('active');
    $('.card__item').removeClass('active').eq($(this).index()).addClass('active');
  });

  setTimeout(function () {
    $('.bid__item').each(function () {
      $(this).find('.bid__company').css('animation-duration', ($(this).find('.bid__company').width() / 100).toFixed(1) + 's');
    })
  }, 500);

  $('.bid__item').hover(function () {
    if ($(document).width() > 600) {
      $(this).find('.bid__company').css('animation-duration', ($(this).find('.bid__company').width() / 350).toFixed(1) + 's');
    }
  });

  $('.nav__open').on('click', function () {
    $(this).toggleClass('active');
    $('.nav-mobile').toggleClass('active');
  });

  $('.filter__title').on('click', function () {
    $(this).closest('.filter').toggleClass('active');
  });


  $('.filter__checkbox').on('click', function () {
    $(this).toggleClass('active');
  });

  $('.catalog__count .catalog__minus, .catalog__count .catalog__plus').on('click', function (e) {
    e.preventDefault();
    if ($(this).hasClass('catalog__minus')) {
      if ($(this).closest('.catalog__count').find('input').val() >= 2) {
        $(this).closest('.catalog__count').find('input').val((parseFloat($(this).closest('.catalog__count').find('input').val()) - 1));
      }
    } else {
      $(this).closest('.catalog__count').find('input').val((parseFloat($(this).closest('.catalog__count').find('input').val()) + 1));
    }
    console.log($(this).closest('.catalog__count').find('input').val());
    $(this).closest('.catalog__count').find('input').change();
  });

  $('.catalog__count input').on('click', function (e) {
    e.preventDefault();
  });

  $('.feedback form').on('submit', function (e) {
    e.preventDefault();
    let emptyInputCount = 0;
    $(this).find('input[type="text"], input[type="phone"]').each(function () {
      if ($(this).val() == '' && $(this).attr('name') != 'mail') {
        $(this).addClass('form-error');
        emptyInputCount++;
        let errorInput = $(this);
        setTimeout(function () {
          $(errorInput).removeClass('form-error');
        }, 1500);
      }
    });
    if ($(this).find('.feedback__check').hasClass('active')) {
      if (emptyInputCount == 0) {
        $.ajax({
          data: {
            name: $(this).find('input[name="name"]').val(),
            phone: $(this).find('input[name="phone"]').val(),
            email: $(this).find('input[name="mail"]').val(),
            msg: $(this).find('textarea[name="message"]').val(),
            csrfmiddlewaretoken: $(this).find('input[name="csrfmiddlewaretoken"]').val()
          },
          method: 'post',
          url: "/send_feedback/",
          dataType: 'json',
          complete: function (response) {
            $('.modal').addClass('active');
            $('.success').addClass('active');
          }
        });
      }
    }
    else {
      $(this).find('span').addClass('form-error');
      $(this).find('.feedback__check').addClass('form-error');
      setTimeout(function () {
        $('.feedback form').find('span').removeClass('form-error');
        $('.feedback form').find('.feedback__check').removeClass('form-error');
      }, 1500);
    }
  });

  $('.order .btn').on('click', function () {
    let emptyInputCount = 0;
    $(this).closest('.order').find('input').each(function () {
      if ($(this).val() == '' && $(this).attr('inputmode') != 'email') {
        $(this).addClass('form-error');
        emptyInputCount++;
        let errorInput = $(this);
        setTimeout(function () {
          $(errorInput).removeClass('form-error');
        }, 1500);
      }
    });
    if ($.cookie("shopping-cart")) {
      if (emptyInputCount == 0) {
        $.ajax({
          data: {
            name: $(this).closest('.order').find('input[name="name"]').val(),
            phone: $(this).closest('.order').find('input[name="phone"]').val(),
            email: $(this).closest('.order').find('input[name="mail"]').val(),
            csrfmiddlewaretoken: $(this).closest('.order').find('input[name="csrfmiddlewaretoken"]').val()
          },
          method: 'post',
          url: "/send_basket/",
          dataType: 'json',
          complete: function (response) {
            $('.modal').addClass('active');
            $('.success').addClass('active');
            $.removeCookie('shopping-cart', { path: '/' });
            $('.shopping-cart').attr('attr-count', 0);
          }
        });
      }
    } else {
      $(this).addClass('form-error').html('Корзина пуста');
      setTimeout(function () {
        $('.order .btn').removeClass('form-error').html('Продолжить')
      }, 1500)
    }
  });

  $('.to-header').on('click', function () {
    $('html, body').animate({
      scrollTop: $('header').offset().top
    }, {
      duration: 370,   // по умолчанию «400»
      easing: "linear"
    });
  });

  $('.catalog__count input').change(function () {
    let pattern = new RegExp(/^[0-9]*[.,]?[0-9]+$/)
    if (pattern.test($(this).val()) == false) {
      $(this).val(1);
    }
    if (parseFloat($(this).val()) <= parseFloat(1)) {
      $(this).val(1);
    }
    if ($(this).closest('.shop-cart__item').hasClass('shop-cart__item')) {
      let k = 0;
      let basketItems = $.makeArray(JSON.parse($.cookie('shopping-cart')));
      let basketItem = { id: $(this).closest('.shop-cart__item').attr('product-id'), count: $(this).closest('.shop-cart__item').find('input').val() };
      for (let i = 0; i < basketItems.length; i++) {
        if (basketItems[i].id == basketItem.id) {
          basketItems[i].count = parseFloat(basketItem.count);
          k++;
        }
      }
      $.cookie('shopping-cart', basketItems, { path: '/', expires: 7 });
      location.reload();
    }
  });


  var cardThumbsSwiper = new Swiper(".card__slider-thumbs", {
    spaceBetween: 15,
    slidesPerView: 3,
    freeMode: true,
    watchSlidesProgress: true,
  });


  var cardSwiper = new Swiper(".card__slider-main", {
    spaceBetween: 10,
    slidesPerView: 1,
    thumbs: {
      swiper: cardThumbsSwiper,
    },
  });


  var swiper = new Swiper(".reviews__slider, .certificates__slider", {
    slidesPerView: 3,
    spaceBetween: 3,
    slidesPerGroup: 1,
    loop: true,
    loopFillGroupWithBlank: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    }, breakpoints: {
      300: {
        slidesPerView: 1,
      },
      640: {
        slidesPerView: 3,
      }
    }
  });

  var projectSwiper = new Swiper(".project__slider", {
    slidesPerView: 2,
    spaceBetween: 100,
    slidesPerGroup: 1,
    loopFillGroupWithBlank: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    }, breakpoints: {
      300: {
        slidesPerView: 1,
      },
      640: {
        slidesPerView: 3,
      }
    }
  });

  var heroSwiper = new Swiper(".hero-slider", {
    pagination: {
      el: ".swiper-pagination",
    },
  });

  /* $('input[name="mail"]').inputmask("email");


  $('input[name="phone"]').inputmask("+375 (99) 999-99-99");
 */
  $(document).mouseup(function (e) { // event of a click on a web document
    var div = $(".search, .search__result");
    if (!div.is(e.target)
      && div.has(e.target).length === 0) {
      $('.search__result').removeClass('active').addClass('searching');
      $('.search__item').remove();
    }
  });



  var searchTimer;

  let currency = 'BYN';
  let domain = document.domain;
  if (domain.includes('ru')) currency = ' RUB';

  $('.search input').on('input', function () {
    if (searchTimer) {
      clearTimeout(searchTimer);
      searchTimer = null;
    }
    let val = $(this).val();
    let resultBox = $('.search__result');
    resultBox.addClass('searching');
    $('.search__item, .empty').remove();
    if (val.length > 1) {
      $(resultBox).addClass('active');
      searchTimer = setTimeout(function () {
        $.ajax({
          data: {
            search: val.toUpperCase().replace(/\s+/g, '').replace(/[^a-zA-Z0-9 ]/g, ""),
          },
          method: 'get',
          url: "/do_search/",
          dataType: 'json',
          complete: function (response) {
            let items = response.responseJSON.items;
            resultBox.removeClass('searching');
            if (items.length != 0) {
              items.map(item => {
                $('.search__result').append(`
              <a href="${item.link}" class="search__item">
                <img src="${item.image}" alt="">
                <div class="search__info">
                    <div class="search__name">
                      ${item.name}
                    </div>
                    <div class="search__sku">
                        Артикул: ${item.article}
                    </div>
                </div>
                <div class="search__price">
                 ${item.price} ${currency}
                </div>
              </a>
          `);

              });
            } else {
              $('.search__result').append(`<div class='empty'>Ничего не найдено</div>`);
            }
          }
        });
      }, 1000);
    } else resultBox.removeClass('active');
  });


  let nextItems;
  let page = 2;
  let waitAjax = false
  let pageEnd = false;

  $(document).on('scroll', function () {
    if ($('.parts-catalog').length != 0) {
      if ((($('.catalog__items').offset().top + $('.catalog__items').height()) - (window.innerHeight + window.scrollY)) < 0 && !pageEnd && !waitAjax) {
        if (nextItems) clearTimeout(nextItems);
        waitAjax = true;
        let data = {
          cat_id: $('.parts-catalog').attr('id'),
          page: page,
        };
        let searchParams = new URLSearchParams(window.location.search);
        for (const [key, value] of searchParams) {
          data[key] = value;
        }
        nextItems = setTimeout(() => {
          $.ajax({
            data: data,
            method: 'get',
            url: "/parts_ajax/",
            complete: function (response) {
              let items = response.responseJSON.page;
              console.log(items);
              items.map((item) => {
                let price;
                if (item.fields.calc_price != null)
                  price = item.fields.calc_price + '' + currency;
                else
                  price = 'ПОД ЗАКАЗ';
                $('.parts-catalog .catalog__items').append(`
                <a href="/part_single/${item.pk}/" class="catalog__item" product-id="${item.pk}">
                  <img class="catalog__img" data-src="${item.fields.first_image}" alt="" src="${item.fields.first_image}">                
                  <div class="catalog__price">${price}</div>              
                  <div class="catalog__delivery">срок поставки: ${item.fields.supply_time}</div>         
                  <h3 class="catalog__art">Артикул: ${item.fields.article}</h3>                
                  <h2 class="catalog__name">${item.fields.name}</h2>
                  <div class="catalog__count">
                      <div class="catalog__minus">-</div>
                      <input id="catalog-count" type="text" value="1">
                      <div class="catalog__plus">+</div>
                  </div>                
                  <div class="btn to-shopping-cart">
                      <img class=" ls-is-cached lazyloaded" data-src="/static/airsyst_app/img/icons/to-basket.svg" alt="" src="/static/airsyst_app/img/icons/to-basket.svg">
                      В корзину
                  </div>
                
                </a>
                `)
              });
              if (page < response.responseJSON.page_count)
                page++;
              else
                pageEnd = true;
              waitAjax = false;
            }
          });
        }, 500)
      }
    }
  });



})