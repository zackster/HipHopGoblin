var currentSong = {
	id: 0,
	title: "",
	artist: ""
}

var jsonMutex = {
	next: 0,
	user: 0
};

var loggedIn = false;

function initPlayer(){
	var jpPlayTime = $("#jplayer_play_time");
	var jpTotalTime = $("#jplayer_total_time");
	$("#jquery_jplayer").jPlayer({
		ready: function() {
			next(false);
			$("#next").show();
			$("#heard").show();
		},
		volume: 50
	}).jPlayer("onProgressChange", function(loadPercent, playedPercentRelative, playedPercentAbsolute, playedTime, totalTime) {
		jpPlayTime.text($.jPlayer.convertTime(playedTime));
		jpTotalTime.text($.jPlayer.convertTime(totalTime));
	}).jPlayer("onSoundComplete", next);
}

function initClickHandlers(){

	$("#next").click(function(){next(false);});
	$("#heard").click(function(){next(true);}); // aka More Obscure
	$("#favorite").click(favorite);
	
	$("#login").click(login);
	$("#register").click(register);
	$("#logout").click(logout);
	
	
}


function initPages() {
	$('#pages').children().hide();
	$('#logreg').show();//show logreg by default.
	$('#menu a[href*=logreg]').addClass('menu_active');
	$('#menu a').each(showPage);
}

function initOtherCrap(){
	
	if(!$("#user-panel").hasClass("hide")){
		loggedIn = true;
	}
	
	$("#token").example("Username");
	$("#password").example("Password");
	
	$("#token, #password").keypress(function(e) {
	if (e.which == 13) {
		$("#login").click();
		return false;
	}
	});
	
	enableCuteMessages();
	enableHotkeys();

	$('a[href=#]').click(function() { return false; });
	
	$(".fave-item").each(function(i , v){addHeartHover($(v), true)});

}

$(document).ready(function() {

	
	initPlayer();
	initClickHandlers();
	initPages();
	initOtherCrap();
	
});



function addToRecent(json) {
	
	var recent = $("<div></div>").addClass("recent-item").data("v", {id: json.id, title: json.title, artist: json.artist}).attr('id', 'recent-' + json.id).text(json.title);
	$("<span></span>").addClass("quiet").text(" " + json.name).appendTo(recent);
	recent.hide();
	recent.prependTo("#recent-list");
	recent.slideDown();
	addHeartHover(recent, json.fave==json.id);// re init listeners	
  	// Leave only the last three listens visible.
  	$('#recent-list .recent-item:gt(2)').slideUp(function(){$(this).remove();})
}


/** adds heart hover ability to given elements. Used on newly made favorites and recent-items*/
function addHeartHover (el, isFave) {
 
	var songid;
	var v = el.data("v");
		
	if(v){
		songid = v.id;
	} else {
		var arr = el.attr('id').split('-');
		songid = arr[1];
	}
	
	var heartBtn = $('<a class="favorite right" href="javascript:void(0);">&hearts;</span>').data("song", songid).addClass("heart-"+songid).appendTo(el).click(favorite).hide();
	if(isFave){
		heartBtn.addClass("loved");
	}
	el.hover(function(){$(this).children("a").show();}, function(){$(this).children("a").hide();});
}






/** displays different message based on how times they've been to the site :) */	
function enableCuteMessages(){
  var numvisits = $.cookie("numvisits");
  
  if (numvisits == 0 || numvisits == undefined) {//first visit
  	$("#howto").notify('Congrats. You\'ve found Mixest', 4000);
  	$.cookie("numvisits", 1, { expires: 365 });
  
  } else if (numvisits == 1) {//second visit
  	$("#howto").notify("Glad you're back for more", 4000);
  	$.cookie("numvisits", ++numvisits, { expires: 365 });//make sure to increment first ;) 
  } else {
  	$.cookie("numvisits", ++numvisits, { expires: 365 });//semi keep track of visits
  }
}

/** hotkeys :)*/
function enableHotkeys() {
	
	$(document).bind('keydown', 'right', next);
    $(document).bind('keypress', 'space', function(evt) { 
		if ($('#jplayer_play').is(':visible')) {
		  $("#jplayer_play").click();
		} else if ($('#jplayer_pause').is(':visible')) {//music is playing if pause button visible
		  $("#jplayer_pause").click();
		}
   	});
    
    var legend = 
    "<h1>Hotkeys</h1>"+
    "<p>"+
    "  right arrow &mdash; next song<br>"+
    "  spacebar &mdash; pause / play"+
    "</p>";
    
    //show hotkey list
    $(document).bind('keydown', 'Shift+/', function(evt) { 
        $("#howto").notify(legend);
    });
    
    //easter egg sheep :)    
    var sheep = 
     "<pre>        __  _\n"
     +"    .-.'  `; `-._  __  _\n"
     +"   (_,         .-:'  `; `-._\n"
     +" ,'o&quot;(        (_,           )\n"
     +"(__,-'      ,'o&quot;(            )>\n"
     +"   (       (__,-'            )\n"
     +"    `-'._.--._(             )\n"
     +"       |||  |||`-'._.--._.-'\n"
     +"                  |||  |||\n</pre";
    $(document).bind('keydown', 'Alt+m', function() {
      $('#howto').notify(sheep);
    });
    
}