$(document).ready(function () {
	if (location.hash) {
		goToLink(location.hash);
	}

	$('#anchorlink').click(function () {
		goToLink(location.hash);
	});
});

function goToLink(link) {
	hashtag = link.replace("#", "").split("-");

	// Show tab
	$('.navbar a[href="#' + hashtag[0] + '"]').tab('show');

	// Show accordion if link refers to an accordion
	if (hashtag.length > 1) {
		if (hashtag.length > 2) {
			$('#' + hashtag[0] + "-" + hashtag[1]).collapse('show');
		}
		$(location.hash).collapse('show');
	}
}