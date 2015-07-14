$(document).ready(function () {
	$('#tabContent1').show();

	for (j = 2; j < 8; j++) {
		$('#tabContent' + j).hide();
	}

	for (i = 1; i < 3; i++) {
		$('#collapse' + i).collapse('hide');
	}
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