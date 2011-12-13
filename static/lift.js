(function(){

    
    var parsePlugin = function(plugin){
	return {name: plugin.name,
		      description: plugin.description,
		      filename: plugin.filename,
		      version: plugin.version}
    },

    whorls = {};
    
    whorls.useragent = navigator.userAgent
    whorls.plugins = _.map(navigator.plugins, parsePlugin);
    whorls.timezone = (new Date()).getTimezoneOffset();
    whorls.screen = screen;
    whorls.cookiesenabled = navigator.cookieEnabled;
    whorls.localstorage = !!localStorage;
    whorls.sessionstorage = !!sessionStorage;
    console.log(whorls);
    $.ajax({
        url: '/identify', 
        processData: false,
        type: "POST", 
        data: JSON.stringify(whorls),
        success: function(response){
	    window.console.log(response);
        }
    });

})();