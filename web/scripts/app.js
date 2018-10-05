$(document).ready(function() {

    $("a.search_button").on("click", search);

});

function search(event) {

	var text = $("input[name='search']").val();
	
	window.location = "/search?domain=" + text;

}
