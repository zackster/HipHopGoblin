function favorite() {
	if(loggedIn){
		var songid;
		
		if($(this).attr("id") == "favorite"){
			songid = currentSong.id;
		} else {
			songid = $(this).data("song");
		}
		
		
		if ($(this).hasClass("loved")) {
			$(this).removeClass("loved");
			if(songid == currentSong.id){
				$("#favorite").removeClass("loved");
			}
			$(".heart-"+songid).removeClass("loved");
			$.getJSON("/control/fave.php?del", {
				cur: songid
			});
			delFaveListItem(songid, true);
			
		} else {
			$(this).addClass("loved");
			$(".heart-"+songid).addClass("loved");
			$.getJSON("/control/fave.php?add", {
				cur: songid
			});
			if(songid == currentSong.id){
				var v = currentSong;
				$("#favorite").addClass("loved");
			} else {
				var v = $(this).parent().data("v");
			}
			addFaveListItem(v, true);
		}
	} else {
		$("#howto").notify("You gotta log in to do that");
	}
}



/** v is the song object?*/
function addFaveListItem(v, animate) {
	var fave = $("<div></div>").data("v", {id: v.id, title: v.title, artist: v.artist}).addClass("fave-item").attr('id', 'fave-'+v.id).text(v.title);
	$("<span></span>").addClass("quiet").text(" "+v.artist).appendTo(fave);
	addHeartHover(fave, true);
	if(animate){
		fave.hide();
		fave.prependTo("#fave-list");
		fave.slideDown();
	} else {
		fave.prependTo("#fave-list");
	}
}

/** deletes the song with the given songid from the favorites list shown on the html page*/
function delFaveListItem(id, animate){
	if(animate){
		$("#fave-"+id).slideUp(function(){$(this).remove();});
	} else {
		$("#fave-"+id).remove();
	}
}