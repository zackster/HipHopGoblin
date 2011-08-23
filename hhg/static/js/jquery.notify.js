(function($)
{
   $.fn.notify = function(msg, duration)
   {
	  if(!(duration>0)){
	  	 duration = 5000;
	  }
      return this.each(function()
      {
         // The element to be modified
         var el = $(this);
		 
		 el.html(msg);
		 el.slideDown();
		 if(el.data('timeout') != ''){
		 	clearTimeout(el.data('timeout'));
		 }
		 el.data('timeout', setTimeout(function(){
									   	  el.slideUp();	 
									   }, duration)
		 );
      });
   };


})(jQuery);