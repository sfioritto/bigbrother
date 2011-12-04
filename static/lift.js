(function(){

    
    var parsePlugin = function(plugin){
	return plugin.description + plugin.filename + plugin.name + plugin.version
    }

    var whorls = {};
    
    whorls.useragent = navigator.userAgent
    whorls.plugins = _.map(navigator.plugins, parsePlugin);
    whorls.timezone = (new Date()).getTimezoneOffset();
    whorls.screen = screen;
    whorls.cookiesenabled = navigator.cookieEnabled;
    whorls.localstorage = !!localStorage;
    whorls.sessionstorage = !!sessionStorage;

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