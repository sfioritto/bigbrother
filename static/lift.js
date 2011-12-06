(function(){

    
    var parsePlugin = function(plugin){
	return plugin.description + plugin.filename + plugin.name + plugin.version
    },

    whorls = {};//just make this a list of k, v pairs, blow up plugin and screen
//objects with screenresolution1000px, screenwidth100px, pluginjibberish here, etc.
    
    whorls.useragent = navigator.userAgent
    whorls.plugins = _.map(navigator.plugins, parsePlugin);
    whorls.timezone = (new Date()).getTimezoneOffset();
    whorls.screen = screen;
    whorls.cookiesenabled = navigator.cookieEnabled;
    whorls.localstorage = !!localStorage;
    whorls.sessionstorage = !!sessionStorage;
    window.console.log(whorls)
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