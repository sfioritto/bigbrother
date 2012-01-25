(function(){

    
    var parsePlugin = function(plugin){
	return {name: plugin.name,
		      description: plugin.description,
		      filename: plugin.filename,
		      version: plugin.version}
    },

    whorls = {};
    
    whorls.plugins = _.map(navigator.plugins, parsePlugin);
    whorls.timezone = (new Date()).getTimezoneOffset();
    whorls.screen = screen;
    whorls.cookiesenabled = navigator.cookieEnabled;
    whorls.localstorage = !!localStorage;
    whorls.sessionstorage = !!sessionStorage;

    if (navigator.userAgent === "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"){
	whorls.username = "firefox"
    } else {
	whorls.username = "chrome"
    }

    $.post("/tag", 
	   {username: "Sean", 
	    password: "paaaasword" },
	   function(response){ 
	       console.log(response);
	   });

    
    $.ajax({
        url: '/identify', 
        processData: false,
        type: "POST", 
        data: JSON.stringify(whorls),
        success: function(response){
	    console.log(response);
        }
    });

    var ec = new evercookie();


    ec.get("uid", function(best, all) {
	console.log("evercookie get");
	console.log(best);
	console.log(all);
    });


//    ec.set("uid", "112")

    /*
     * 1. Do a get on uid
     * 2. if it's not there
     */

})();