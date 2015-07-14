$(document).ready(function () {
	$('#tabContent1').show();

	for (j = 2; j < 8; j++) {
		$('#tabContent' + j).hide();
	}

	$(".collapse").collapse();
	$('#accordion').collapse({hide: true});
});

$('.nav a').click(function (e) {
    $(this).tab('show');
  
  var tabContent = '#tabContent' + this.id; 
  
  $('#tabContent1').hide();
  $('#tabContent2').hide();
  $('#tabContent3').hide();
  $(tabContent).show();
});

$('.panel a').click(function (e) {
	$('#collapse' + location.hash).collapse('toggle');
});