$(document).ready(function(){
    bigbrother.guess(function(name, whorls){
	$("#guess").text("Hello " + name)
    })
});
