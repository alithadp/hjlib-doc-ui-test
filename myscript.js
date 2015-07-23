$(document).ready(function () {
	if (location.hash) {
		goToLink(location.hash);
	}

	
	$('.anchorlink').click(function () {
		goToLink(this.getAttribute("href"));
	});
});

function goToLink(link) {
	hashtag = link.replace("#", "").split("-");

	// Show tab
	$('.navbar a[href="#' + hashtag[0] + '"]').tab('show');

	// Show accordion if link refers to an accordion
	if (hashtag.length > 1) {
		$('#' + hashtag[0] + "-" + hashtag[1]).collapse('show');
		if (hashtag.length > 2) {
			$('#' + hashtag[0] + "-" + hashtag[1] + "-" + hashtag[2]).collapse('show');
		}
	}
}