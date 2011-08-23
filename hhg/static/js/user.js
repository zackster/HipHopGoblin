/** login users*/
function login() {
	if (jsonMutex.user == 0) {
		jsonMutex.user = 1;
		if ($("#token").val() == '' || $("#password").val() == '') {
			$("#msg").text("Please fill in both username and password");
			$("#msg").slideDown();
		}
		$.getJSON("/control/user.php", {
			u: $("#token").val(),
			p: $("#password").val(),
			cur: currentSong.id
		},
		function(json) {
			jsonMutex.user = 0;
			$("#msg").text(json.msg);
			$("#msg").slideDown();
			if (json.hide == 1) {
				loggedIn = true;
				$("#howto").slideUp();
				$("#login-panel").slideUp();
				$("#user-panel").slideDown();
				$("#howto").notify('Sup ' + $("#token").val() + '! Try clicking next to skip this song.<br>Click "More obscure" if you feel this song isn\'t fresh enough.<br>Make sure to click the heart to favorite a song!', 10000);
				$("#menu a[href*=logreg]").text($("#token").val());
				$("#favorite").removeClass("loved");
				$('#menu a[href*=fave]').show();
				$(".recent-item").children('a').removeClass("loved");
				$.each(json.fave, function(i, v) {
					v.artist = v.name;
					addFaveListItem(v, false);
					if (currentSong.id == v.id) {
						$("#favorite").addClass("loved");
					}
					/*$(".recent-item").each(function(i, j){
						if($(j).attr('id') != "recent-"+v.id){
							$(j).children("a").removeClass("loved");
							
						} else {
							$(j).children("a").addClass("loved");
							
						}
					});
					*/
					$(".heart-"+v.id).addClass("loved");
				});
				if (json.admin == 1) {
					createDelButton();
				}
			}
		});
	}
}


/** register new users*/
function register() {
	if (jsonMutex.user == 0) {
		jsonMutex.user = 1;
		if ($("#token").val() == '' || $("#password").val() == '' || $("#token").val() == 'Username' || $("#password").val() == 'Password') {
			$("#msg").text("Please fill in both fields");
			$("#msg").slideDown();
			$("#howto").notify('Mixest is easy. Just pick a username and password and you\'re done.');
			jsonMutex.user = 0;
		} else {
			$.getJSON("/control/register.php", {
				u: $("#token").val(),
				p: $("#password").val()
			},
			function(json) {
				jsonMutex.user = 0;
				$("#msg").text(json.msg);
				$("#msg").slideDown();
				if (json.hide == 1) {
					$("#howto").notify('That was quick right? Start using Mixest:<br>Try clicking next to skip this song.<br>Click "More obscure" if you feel this song isn\'t fresh enough.<br>Make sure to click the heart to favorite this song!', 15000);
					$("#login-panel").slideUp();
					$("#user-panel").slideDown();
					$("#favorite").slideDown();
					$('#menu a[href*=fave]').show();
				} else {
					$("#howto").notify('Mixest is easy. Just pick a username and password and you\'re done.');
				}
			});
		}
	}
}

/** Deals with logout*/
function logout() {
	if (jsonMutex.user == 0) {
		loggedIn = false;
		jsonMutex.user = 1;
		$.getJSON("/control/user.php", function(json) {
			jsonMutex.user = 0;
			$("#howto").notify('You are logged out', 2000);
			$("#msg").slideUp();
			$("#menu a[href*=logreg]").text("login / register");
			$("#user-panel").slideUp();
			$("#login-panel").slideDown();
			$("#favorite").removeClass("loved");
			$(".recent-item").children("a").removeClass("loved");
			$("#del").remove();
			$("#menu a[href*=fave]").hide();
			$("#fave-list").empty();
		});
	}
}

/** Creates delete button for admin users*/
function createDelButton() {
	$("<a></a>").text("Del").appendTo("#buttons").attr('href', '#').attr('id', 'del').click(function() {
		$.getJSON("/control/delete.php", {
			cur: currentSong.id
		});
		next(false);
	});
}