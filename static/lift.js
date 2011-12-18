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
    whorls.username = "sean"
    console.log(whorls);
    $.ajax({
        url: '/tag', 
        processData: false,
        type: "POST", 
        data: JSON.stringify(whorls),
        success: function(response){
	    console.log(response);
        }
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

})();