$(document).ready(function(){
    $("#mybutton").click(function(){
	$("#message").html('Give me about 20 seconds to try and memorize your computer fingerprint.');
	bigbrother.learn($("#myfield").val(), function(username, whorls){
	    $("#message").html('ok, click <a href="/static/playing.html">here</a> and use this url from now on to play.');
	});
    });
});
