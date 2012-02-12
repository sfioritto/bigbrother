(function(){
    
    var parsePlugin = function(plugin){
	return {name: plugin.name,
		description: plugin.description,
		filename: plugin.filename,
		version: plugin.version}
    },

    whorls = {},
    
    ec = new evercookie(),

    get_history = function(cb){
	visipisi.get(function(results){
	    whorls.history = results;
	    cb(whorls);
	});
    },

    get_fonts = function(cb){
	
	// Check Flash version
	if (!swfobject.hasFlashPlayerVersion("9.0.0")){
	    //just skip fonts.
	    cb();
	} else {
            var fontDetect = new FontDetect("fontdetectswf", "FontList.swf", function(fd) {        
		var fonts = fd.fonts();
		whorls.fonts = fonts;
		cb();
	    });

	}	
    },

    learn = function(whorls, callback){
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


    set_basic_whorl = function(name){

	if (name){
	    whorls.name = name;
	}
	whorls.plugins = _.map(navigator.plugins, parsePlugin);
	whorls.useragent = navigator.userAgent;
	whorls.timezone = (new Date()).getTimezoneOffset();
	whorls.screen = screen;
	whorls.cookiesenabled = navigator.cookieEnabled;
	whorls.localstorage = !!window.localStorage;
	whorls.sessionstorage = !!window.sessionStorage;
    };

    window.bigbrother = {};

    bigbrother.learn = function(name, cb){

	set_basic_whorl(name);
	get_fonts(function(){
	    get_history(function(){
		ec.set("uid", name + Math.floor(Math.random() * 100000));
		setTimeout(function(){
		    ec.get("uid", function(best, all){
			whorls.evercookie = all;
			learn(whorls, function(){
			    cb(name, whorls);
			});
		    });
		}, 10000); //setting evercookie provides no callback
	    });
	});

    };

    bigbrother.guess = function(cb){
	set_basic_whorl();
	ec.get("uid", function(best, all) {
	    whorls.evercookie = all;

	    get_fonts(function(){
		get_history(function(){
		    identify(whorls, cb);
		})
	    });
	});
    };
})();
