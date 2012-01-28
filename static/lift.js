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


    var ec = new evercookie();


    ec.get("uid", function(best, all) {
	whorls.evercookie = all;
	whorls.username = "Sean";
	whorls.password = "password";
	learn(whorls, function(){ 
	    identify(whorls, function(){
		console.log(response);
	    })
	});
    });
    
    //    ec.set("uid", "112")
    
    var learn = function(whorls, callback){
	$.ajax({url: "/learn", 
		processData: false,
		type: "POST",
		data: JSON.stringify(whorls),
		success: callback})
    },
    
    identify = function(whorls, callback){
	$.ajax({
	    url: '/identify', 
	    processData: false,
	    type: "POST", 
	    data: JSON.stringify(whorls),
	    success: callback
	});
    },

    endCB = function () {
	console.log(new Date().getTime() - start + ' milliseconds');
    };

})();
