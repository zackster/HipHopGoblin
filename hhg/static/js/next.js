function next(heard) {
	if (jsonMutex.next == 0) {
		jsonMutex.next = 1;
		var url = "http://www.stormreportmap.com/mag/random.php";
		if (heard) {
			url += "?heard";
		}
		$.getJSON(url, {
			cur: 814
		},
		function(json) {
			jsonMutex.next = 0;
			$("#jquery_jplayer").jPlayer("setFile", json.filename + ".mp3").jPlayer("play");
			$("#title").text(json.title);
			$("#artist").text(json.name);
			currentSong.id = json.id;
			currentSong.title = json.title;
			currentSong.artist = json.name;
			if (json.fave == json.id) {
				$("#favorite").addClass("loved");
			} else {
				$("#favorite").removeClass("loved");
			}
			json.artist = json.name;
			addToRecent(json);
		});
	}
}