/** Deals with showing and hiding pages, e.g. about, team, etc.*/
function showPage() {
	$(this).click(function() {

	    link = $(this);
		var pageid = link.attr('href');

		if (link.hasClass('menu_active')) {
			link.removeClass('menu_active');
			$(pageid).slideUp();
		} else {
			  $('#menu a').removeClass('menu_active');
			  link.addClass('menu_active');
			  $(pageid).siblings().slideUp(function() {
				$(pageid).slideDown();
	     	});        
		}
		return false;
	});
}
