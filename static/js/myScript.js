// Navbar
function showHideMegaMenuItem(id) {
  const megaMenuItems = document.getElementsByClassName("megamenu-item");
  const menuItem = document.getElementById('nav-item' + id);
  for(var x=0; x < megaMenuItems.length; x++)
  {
    if (menuItem != megaMenuItems[x]) {
      megaMenuItems[x].classList.add('collapse');
    }
  }
  if (menuItem.classList.contains('collapse')) {
    menuItem.classList.remove('collapse');    
  } else {
    menuItem.classList.add('collapse');
  }
}

function showMegaMenuRegion(id) {
  const megaMenuItems = document.getElementsByClassName("megamenu-item");
  var megaMenuItemHeight = 0;
  for(var x=0; x < megaMenuItems.length; x++)
  {
    if (!megaMenuItems[x].classList.contains("collapse")) {
      megaMenuItemHeight = megaMenuItems[x].offsetHeight-1 + 80;
    }
  }
  const megaMenuRegion = document.getElementById('region-item' + id);
  megaMenuRegion.classList.remove('collapse');
  megaMenuRegion.style.marginTop = megaMenuItemHeight + "px";

  const regionImage = document.getElementById('region-img' + id);
  regionImage.style.borderBottom = "3px solid #dcbc94";
}
function hideMegaMenuRegion(id) {
  document.getElementById('region-item' + id).classList.add('collapse');
  document.getElementById('region-img' + id).style.borderBottom = "";
}

function showMegaMenuPage(id) {
  const megaMenuItems = document.getElementsByClassName("megamenu-item");
  var megaMenuItemHeight = 0;
  for(var x=0; x < megaMenuItems.length; x++)
  {
    if (!megaMenuItems[x].classList.contains("collapse")) {
      megaMenuItemHeight = megaMenuItems[x].offsetHeight-1 + 80;
    }
  }
  const megaMenuPage = document.getElementById('page-item' + id);
  megaMenuPage.classList.remove('collapse');
  megaMenuPage.style.marginTop = megaMenuItemHeight + "px";

  const regionImage = document.getElementById('page-img' + id);
  regionImage.style.borderBottom = "3px solid #dcbc94";
}
function hideMegaMenuPage(id) {
  document.getElementById('page-item' + id).classList.add('collapse');
  document.getElementById('page-img' + id).style.borderBottom = "";
}

// Default Carousel
$().ready(function () {
  $(".slick-carousel").slick({
    centerPadding: "370px",
    infinite: true,
    slidesToShow: 1,
    prevArrow: false,
    nextArrow: false,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 5000,
    centerMode: true,
    responsive: [
      {
        breakpoint: 1400,
        settings: {
          centerPadding: "330px",
          slidesToShow: 1,
        },
      },
      {
        breakpoint: 978,
        settings: {
          centerPadding: "100px",
          slidesToShow: 2,
        },
      },
      {
        breakpoint: 768,
        settings: {
          centerPadding: "0px",
          slidesToShow: 1,
        },
      },
    ],
  });
});

// Homepage Carousel
$().ready(function () {
  $(".slick-carousel-homepage").slick({
    centerPadding: "0px",
    infinite: true,
    slidesToShow: 1,
    prevArrow: false,
    nextArrow: false,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 5000,
    fade: true,
  });
});

// Yard Cover Carousel
$().ready(function () {
  $(".slick-carousel-yard-cover").slick({
    centerPadding: "0px",
    infinite: true,
    slidesToShow: 1,
    prevArrow: false,
    nextArrow: false,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 5000,
    fade: true,
  });
});

// Show Preview (rr_form.html)
function preview() {
  var totalRating = document.getElementById("totalRating").innerText;
  document.getElementById("totalRatingPreview").innerHTML = totalRating;
  var titleValue = document.getElementById("titleValue").value;
  document.getElementById("titlePreview").innerHTML = titleValue;
  var reviewValue = document.getElementById("reviewValue").value;
  document.getElementById("reviewPreview").innerHTML = reviewValue;
}

// Show Live Total Rating Calculation (rr_form.html)
function liveCalculation() {
  var recommendedValue = Number(document.getElementById("recommendedRange").value);
  var valueValue = Number(document.getElementById("valueRange").value);
  var serviceValue = Number(document.getElementById("serviceRange").value);
  var cleanlinessValue = Number(document.getElementById("cleanlinessRange").value);
  var locationValue = Number(document.getElementById("locationRange").value);
  var sustainabilityValue = Number(document.getElementById("sustainabilityRange").value);
  var totalRating =
    (recommendedValue +
      valueValue +
      serviceValue +
      cleanlinessValue +
      locationValue +
      sustainabilityValue) /
    6;
  document.getElementById("totalRating").innerHTML = totalRating.toFixed(2);
}

// Read more & Read less (on interest detail reviews)
function moreLess(element) {
  var half = "half-" + element.id;
  var full = "full-" + element.id;
  var halfDisplay = document.getElementById(half).style.display;
  if (halfDisplay == "none") {
    document.getElementById(half).style.display = "block";
    document.getElementById(full).style.display = "none";
  } else if (halfDisplay == "block") {
    document.getElementById(half).style.display = "none";
    document.getElementById(full).style.display = "block";
  }
}

// Read more & Read less (on recent reviews)
function sidebarMoreLess(element) {
  var half = "half-" + element.id + "-sidebar";
  var full = "full-" + element.id + "-sidebar";
  var halfDisplay = document.getElementById(half).style.display;
  if (halfDisplay == "none") {
    document.getElementById(half).style.display = "block";
    document.getElementById(full).style.display = "none";
  } else if (halfDisplay == "block") {
    document.getElementById(half).style.display = "none";
    document.getElementById(full).style.display = "block";
  }
}

// Change width of text below your rating (rr_form.html)
$(document).ready(function () {
  $("#text-below-your-rating").css({
    width: $("#your-rating").width() + "px",
  });
  $(window).resize(function () {
    $("#text-below-your-rating").css({
      width: $("#your-rating").width() + "px",
    });
  });
});

// Refresh captcha
$(function() {
  // Add refresh button after field (this can be done in the template as well)
  $('img.captcha').after(
    $('<a href="#void" class="captcha-refresh btn btn-secondary m-3">Refresh</a>')
  );

  // Click-handler for the refresh-link
  $('.captcha-refresh').click(function(){
      var $form = $(this).parents('form');
      var url = location.protocol + "//" + window.location.hostname + ":"
                + location.port + "/captcha/refresh/";

      // Make the AJAX-call
      $.getJSON(url, {}, function(json) {
          $form.find('input[name="captcha_0"]').val(json.key);
          $form.find('img.captcha').attr('src', json.image_url);
      });

      return false;
  });
});

// Refresh captcha automatically
$(document).ready(function() {
  // Refresh captcha every 5 minutes
  setInterval(function() {
      var $form = $('.captcha-refresh').parents('form');
      var url = location.protocol + "//" + window.location.hostname + ":"
                + location.port + "/captcha/refresh/";
      
      // Make the AJAX call
      $.getJSON(url, {}, function(json) {
          $form.find('input[name="captcha_0"]').val(json.key);
          $form.find('img.captcha').attr('src', json.image_url);
      });
  }, 1000 * 60 * 5);  // refresh every 5 minutes
});

// Login Form Popup
$(function() {
  $('#login-form').submit(function(event) {
    event.preventDefault();
    var form = $(this);
    var url = form.attr('action');
    var redirectUrl = getSessionRedirectUrl();
    var data = form.serialize();
    $.ajax({
      url: url,
      type: 'POST',
      data: data,
      success: function(response) {
        if (redirectUrl) {
          window.location.href = redirectUrl;
          clearSessionRedirectUrl();
        } else {
          window.location.reload();
        }
      },
      error: function(xhr) {
        var errorJson = JSON.parse(xhr.responseText);
        var errorList = '';

        if (errorJson.form.errors.length > 0) {
          errorJson.form.errors.forEach(element => {
            errorList += '<li>' + element + '</li>';
          });
        }

        var result = '<div id="login-error"><div class="alert alert-block alert-danger"><ul class="m-0">' + errorList + '</ul></div></div>';
        $('#login-error').replaceWith(result);
      }
    });
  });
});

// Signup Form Popup
$(function() {
  $('#signup-form').submit(function(event) {
    event.preventDefault();
    var form = $(this);
    var url = form.attr('action');
    var redirectUrl = getSessionRedirectUrl();
    console.log(redirectUrl);
    var data = form.serialize();
    $.ajax({
      url: url,
      type: 'POST',
      data: data,
      success: function(response) {
        if (redirectUrl) {
          window.location.href = redirectUrl;
          clearSessionRedirectUrl();
        } else {
          window.location.reload();
        }
      },
      error: function(xhr) {
        var errorJson = JSON.parse(xhr.responseText);
        var errorList = '';
      
        Object.values(errorJson.form.fields).forEach(function(field) {
          console.log(errorJson.form.fields);
          field.errors.forEach(function(error) {
            errorList += '<li>' + error + '</li>';
          });
        });
      
        var result = '<div id="signup-error"><div class="alert alert-block alert-danger"><ul class="m-0">' + errorList + '</ul></div></div>';
        $('#signup-error').replaceWith(result);
      }
    });
  });
});

// Redirect Url on Login and Signup Form Popup
function getSessionRedirectUrl() {
  return sessionStorage.getItem('redirectUrl');
}

function setSessionRedirectUrl(redirectUrl) {
  console.log(redirectUrl);
  sessionStorage.setItem('redirectUrl', redirectUrl);
}

function clearSessionRedirectUrl() {
  sessionStorage.removeItem('redirectUrl');
}

// Filter Checkbox
$(document).ready(function(){
  $(".ajaxLoader").hide();
  $("#loading-filter-selection").hide();
  filterData();

  // If user select anything
	$(".filter-checkbox").on("change", function(){
    closeFilterDropdown();
    syncFilterCheckbox($(this));
    showSelectedFilter();
    // filterSelection();
    filterData();
    scrollToInterestSection();
	});
  
});

// Sync Filter Checkbox on Filter Selection and Offcanvas
function syncFilterCheckbox(current){
  $('input[type=checkbox]').each(function(index) {
    if (current.next("label").text() == $(this).next("label").text()) {
      $(this).prop('checked', current.prop('checked'));
    }
  });
}

// Close Filter Dropdown
function closeFilterDropdown(){
  $('.dropdown-btn.show').removeClass('show');
  $('.dropdown-menu.show').removeClass('show');
  $('.collapse-btn').addClass('collapsed');
  $('.list-group.show').removeClass('show');
}

// Remove Selected Filter
function removeSelectedFilter(text){
  $('input[type=checkbox]:checked').each(function(index) {
    if (text == $(this).next("label").text()) {
      $(this).prop('checked', false).change();
        return false;
    }
  });
}

// Filter Data
function filterData(){
  var _data={defaultInterests, perPage, pageType};

  $(".filter-checkbox").each(function(index,ele){
    var _filterVal=$(this).val();
    var _filterKey=$(this).data('filter');
    _data[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
      return el.value;
    });
  });
  
  // Run Ajax
  $.ajax({
    url:'/filter-data',
    data:_data,
    dataType:'json',
    beforeSend:function(){
      $(".ajaxLoader").show();
      // Disable Filter Selection while processing
      $("#filter-selection").children().css({"pointer-events": "none", "opacity": "0.5"});
      $("#offcanvasFilter").children().css({"pointer-events": "none", "opacity": "0.5"});
      $("#selected-filters").children().css({"pointer-events": "none", "opacity": "0.5"});
    },
    success:function(res){
      // Enable Filter Selection after success processing
      $("#filter-selection").children().css({"pointer-events": "auto", "opacity": "1"});
      $("#offcanvasFilter").children().css({"pointer-events": "auto", "opacity": "1"});
      $("#selected-filters").children().css({"pointer-events": "auto", "opacity": "1"});
      showAllFilter();
      $(".filter-checkbox").each(function(index, ele){
        $(this).next().next().text(" (" + res.count_result[index] + ")");
        if ($(this).next().next().text() == " (0)") {
          $(this).parent().parent().hide();
        }
      });

      $("#filteredInterests").html(res.data);
      $(".ajaxLoader").hide();
      $('#view-filtered-interests').text("View all " + res.total_interests + " Restaurants");
    }
  });
}

// Automatically Scroll to  
function scrollToInterestSection(){
  $('html, body').animate({scrollTop: $("#filteredInterests").offset().top-300}, 100); 
}

// Show Selected Filters
function showSelectedFilter(){
  var $checkedCheckbox = $('input[type="checkbox"]:checked');
  var selectedFilters = $checkedCheckbox.map(function() {
    return $(this).next("label").text();
  }).get();

  // Remove Duplicate
  selectedFilters = [...new Set(selectedFilters)];
  
  var list = "";
  for(i=0; i<selectedFilters.length; i++){
    list += "<button class='btn btn-secondary btn-sm ps-3 pe-2 mx-1 selected-filter' type='button' onclick='removeSelectedFilter(\""+selectedFilters[i].replace(/'/g, "&#39;")+"\")' >"+selectedFilters[i]+"<span class='ps-2 pe-1'>x</span>"+"</button>";
  }
  $(".selectedFilters").html(list);
}

// Show all filter
function showAllFilter() {
  $('.ratingItem').show();
  $('.worldItem').show();
  $('.countryItem').show();
  $('.regionItem').show();
  $('.cityItem').show();
  $('.sp1Item').show();
  $('.sp2Item').show();
  $('.sp3Item').show();
  $('.facilityItem').show();
  $('.serviceItem').show();
  $('.ratingItem div').children('input[type="checkbox"]').attr("disabled", false);
  $('.worldItem div').children('input[type="checkbox"]').attr("disabled", false);
  $('.countryItem div').children('input[type="checkbox"]').attr("disabled", false);
  $('.regionItem div').children('input[type="checkbox"]').attr("disabled", false);
  $('.cityItem div').children('input[type="checkbox"]').attr("disabled", false);
  $('.sp1Item div').children('input[type="checkbox"]').attr("disabled", false);
  $('.sp2Item div').children('input[type="checkbox"]').attr("disabled", false);
  $('.sp3Item div').children('input[type="checkbox"]').attr("disabled", false);
  $('.facilityItem div').children('input[type="checkbox"]').attr("disabled", false);
  $('.serviceItem div').children('input[type="checkbox"]').attr("disabled", false);
  $('.count-interests').css("opacity", "1.0");
}

// // Filter Selection
// function filterSelection(){
//   // From World
//   var world = $('.worldItem div').children('input[type="checkbox"]:checked').val();
//   var world_country = $('.worldItem div').children('input[type="checkbox"]:checked').attr("country");
//   var world_region = $('.worldItem div').children('input[type="checkbox"]:checked').attr("region");

//   // From Country
//   var country = $('.countryItem div').children('input[type="checkbox"]:checked').val();
//   var country_world = $('.countryItem div').children('input[type="checkbox"]:checked').attr("world");
//   var country_region = $('.countryItem div').children('input[type="checkbox"]:checked').attr("region");

//   // From Region
//   var region = $('.regionItem div').children('input[type="checkbox"]:checked').val();
//   var region_world = $('.regionItem div').children('input[type="checkbox"]:checked').attr("world");
//   var region_country = $('.regionItem div').children('input[type="checkbox"]:checked').attr("country");

//   // Convert to JS Array
//   world !== undefined ? world = world.split(',') : world = [];
//   world_country !== undefined ? world_country = world_country.split(',') : world_country = [];
//   world_region !== undefined ? world_region = world_region.split(',') : world_region = [];
//   country !== undefined ? country = country.split(',') : country = [];
//   country_world !== undefined ? country_world = country_world.split(',') : country_world = [];
//   country_region !== undefined ? country_region = country_region.split(',') : country_region = [];
//   region !== undefined ? region = region.split(',') : region = [];
//   region_world !== undefined ? region_world = region_world.split(',') : region_world = [];
//   region_country !== undefined ? region_country = region_country.split(',') : region_country = [];

//   // Case 1: Select World
//   if(world.length == 1 && country.length == 0 && region == 0) {
//     showAllFilter();
//     $('.worldItem div').children(':checkbox:not(:checked)').attr("disabled", true);
//     $('.worldItem div').children(':checkbox:not(:checked)').next().next().css("opacity", "0.5");
//     if(world_country!==undefined){
//       $('.countryItem').each(function(i, obj) {        
//         if ($.inArray($(obj).attr('id'), world_country) == -1)
//         {
//           $(obj).hide();
//         }
//       });
//     }
//     if(world_region!==undefined){
//       $('.regionItem').each(function(i, obj) {        
//         if ($.inArray($(obj).attr('id'), world_region) == -1)
//         {
//           $(obj).hide();
//         }
//       });
//     }
//   } 
//   // Case 2: Select Country
//   else if(world.length == 0 && country.length == 1 && region == 0){
//     showAllFilter();
//     $('.countryItem div').children(':checkbox:not(:checked)').attr("disabled", true);
//     $('.countryItem div').children(':checkbox:not(:checked)').next().next().css("opacity", "0.5");
//     $('.worldItem div').children(':checkbox').attr("disabled", true);
//     $('.worldItem div').children(':checkbox').next().next().css("opacity", "0.5");
//     if(country_region!==undefined){
//       $('.regionItem').each(function(i, obj) {        
//         if ($.inArray($(obj).attr('id'), country_region) == -1)
//         {
//           $(obj).hide();
//         }
//       });
//     }
//   }
//   // Case 3: Select Region
//   else if(world.length == 0 && country.length == 0 && region.length == 1) {
//     showAllFilter();
//     $('.regionItem div').children(':checkbox:not(:checked)').attr("disabled", true);
//     $('.regionItem div').children(':checkbox:not(:checked)').next().next().css("opacity", "0.5");
//     $('.worldItem div').children(':checkbox').attr("disabled", true);
//     $('.worldItem div').children(':checkbox').next().next().css("opacity", "0.5");
//     $('.countryItem div').children(':checkbox').attr("disabled", true);
//     $('.countryItem div').children(':checkbox').next().next().css("opacity", "0.5");
//   }
//   // Case 4: Select World and Country
//   else if(world.length == 1 && country.length == 1 && region.length == 0) {
//     showAllFilter();
//     $('.worldItem div').children(':checkbox').attr("disabled", true);
//     $('.worldItem div').children(':checkbox').next().next().css("opacity", "0.5");
//     $('.countryItem div').children(':checkbox:not(:checked)').attr("disabled", true);
//     $('.countryItem div').children(':checkbox:not(:checked)').next().next().css("opacity", "0.5");
//     if(country_region!==undefined){
//       $('.regionItem').each(function(i, obj) {        
//         if ($.inArray($(obj).attr('id'), country_region) == -1)
//         {
//           $(obj).hide();
//         }
//       });
//     }
//   }
//   // Case 5: Select World and Region
//   else if(world.length == 1 && country.length == 0 && region.length == 1) {
//     showAllFilter();
//     $('.worldItem div').children(':checkbox').attr("disabled", true);
//     $('.worldItem div').children(':checkbox').next().next().css("opacity", "0.5");
//     $('.countryItem div').children(':checkbox').attr("disabled", true);
//     $('.countryItem div').children(':checkbox').next().next().css("opacity", "0.5");
//     $('.regionItem div').children(':checkbox:not(:checked)').attr("disabled", true);
//     $('.regionItem div').children(':checkbox:not(:checked)').next().next().css("opacity", "0.5");
//   }
//   // Case 6: Select Country and Region
//   else if(world.length == 0 && country.length == 1 && region.length == 1) {
//     showAllFilter();
//     $('.worldItem div').children(':checkbox').attr("disabled", true);
//     $('.worldItem div').children(':checkbox').next().next().css("opacity", "0.5");
//     $('.countryItem div').children(':checkbox').attr("disabled", true);
//     $('.countryItem div').children(':checkbox').next().next().css("opacity", "0.5");
//     $('.regionItem div').children(':checkbox:not(:checked)').attr("disabled", true);
//     $('.regionItem div').children(':checkbox:not(:checked)').next().next().css("opacity", "0.5");
//   }
//   // Case 7: Select World, Country, and Region
//   else if(world.length == 1 && country.length == 1 && region.length == 1) {
//     showAllFilter();
//     $('.worldItem div').children(':checkbox').attr("disabled", true);
//     $('.worldItem div').children(':checkbox').next().next().css("opacity", "0.5");
//     $('.countryItem div').children(':checkbox').attr("disabled", true);
//     $('.countryItem div').children(':checkbox').next().next().css("opacity", "0.5");
//     $('.regionItem div').children(':checkbox:not(:checked)').attr("disabled", true);
//     $('.regionItem div').children(':checkbox:not(:checked)').next().next().css("opacity", "0.5");
//   }
//   // Case 8: Nothing Selected
//   else if(world.length == 0 && country.length == 0 && region.length == 0) {
//     showAllFilter();
//   }
//   else {
//     alert("Error");
//   }
// }

// Reset Filter
function resetAllFilters(){
  $('input[type=checkbox]:checked').each(function(index) {
    $(this).prop('checked', false).change();
  });
}

// Interest Section Pagination
function loadMore(currentPage){
  var _data={currentInterests, perPage, currentPage};

  // Run Ajax
  $.ajax({
    url:'/load-more-data',
    data:_data,
    dataType:'json',
    beforeSend:function(){
      $(".ajaxLoader").show();
    },
    success:function(res){
      $("#filteredInterests").html(res.data);
      $(".ajaxLoader").hide();
      $('html, body').animate({scrollTop: $("#filteredInterests").offset().top-300}, 100); 
      $('#view-filtered-interests').text("View all " + res.total_interests + " Restaurants");
    }
  });
};
