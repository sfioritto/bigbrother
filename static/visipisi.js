(function(){
    
    
    var start = new Date().getTime(),
    results = {},
    urls = {
	facebook: 'https://s-static.ak.facebook.com/rsrc.php/v1/yJ/r/vOykDL15P0R.png',
	twitter: 'https://twitter.com/images/spinner.gif',
	digg: 'http://cdn2.diggstatic.com/img/sprites/global.5b25823e.png',
	reddit: 'http://www.redditstatic.com/sprite-reddit.pZL22qP4ous.png',
	hn: 'http://ycombinator.com/images/y18.gif',
	stumbleupon: 'http://cdn.stumble-upon.com/i/bg/logo_su.png',
	wired: 'http://www.wired.com/images/home/wired_logo.gif',
	xkcd: 'http://imgs.xkcd.com/s/9be30a7.png',
	linkedin: 'http://static01.linkedin.com/scds/common/u/img/sprite/sprite_global_v6.png',
	slashdot: 'http://a.fsdn.com/sd/logo_w_l.png',
	myspace: 'http://cms.myspacecdn.com/cms/x/11/47/title-WhatsHotWhite.jpg',
	engadget: 'http://www.blogsmithmedia.com/www.engadget.com/media/engadget_logo.png',
	lastfm: 'http://cdn.lst.fm/flatness/anonhome/1/anon-sprite.png',
	pandora: 'http://www.pandora.com/img/logo.png',
	youtube: 'http://s.ytimg.com/yt/img/pixel-vfl3z5WfW.gif',
	yahoo: 'http://l.yimg.com/ao/i/mp/properties/frontpage/01/img/aufrontpage-sprite.s1740.gif',
	google: 'https://www.google.com/intl/en_com/images/srpr/logo3w.png',
	hotmail: 'https://secure.shared.live.com/~Live.SiteContent.ID/~16.2.8/~/~/~/~/images/iconmap.png',
	cnn: 'http://i.cdn.turner.com/cnn/.element/img/3.0/global/header/intl/hdr-globe-central.gif',
	bbc: 'http://static.bbc.co.uk/frameworks/barlesque/1.21.2/desktop/3/img/blocks/light.png',
	reuters: 'http://www.reuters.com/resources_v2/images/masthead-logo.gif',
	wikipedia: 'http://upload.wikimedia.org/wikipedia/en/b/bc/Wiki.png',
	amazon: 'http://g-ecx.images-amazon.com/images/G/01/gno/images/orangeBlue/navPackedSprites-US-22._V183711641_.png',
	ebay: 'http://p.ebaystatic.com/aw/pics/au/logos/logoEbay_x45.gif',
	newegg: 'http://images10.newegg.com/WebResource/Themes/2005/Nest/neLogo.png',
	bestbuy: 'http://images.bestbuy.com/BestBuy_US/en_US/images/global/header/hdr_logo.gif',
	walmart: 'http://i2.walmartimages.com/i/header_wide/walmart_logo_214x54.gif',
	abebooks: 'http://www.abebooks.com/images/HeaderFooter/siteRevamp/AbeBooks-logo.gif',
	mcmasterone: "http://images1.mcmaster.com/gfx/HomePageImages.png?ver=31503143",
	mcmastertwo: "http://images2.mcmaster.com/gfx/HomePageImages.png?ver=31503143",
	msy: 'http://msy.com.au/images/MSYLogo-long.gif',
	techbuy: 'http://www.techbuy.com.au/themes/default/images/tblogo.jpg',
	mozilla: 'http://www.mozilla.org/images/template/screen/logo_footer.png',
	anandtech: 'http://www.anandtech.com/content/images/globals/header_logo.png',
	tomshardware: 'http://m.bestofmedia.com/i/tomshardware/v3/logo_th.png',
	shopbot: 'http://i.shopbot.com.au/s/i/logo/en_AU/shopbot.gif',
	staticice: 'http://staticice.com.au/images/banner.jpg',
	bing: 'http://www.bing.com/fd/s/a/h9.png',
	zappos: 'http://a2.zassets.com/assets/hotspot/timeslot_images/10425_1311613627.png',
	drudge: 'http://www.drudgereport.com/i/logo9.gif',
	huffington: 'http://s.huffpost.com/images/v/logos/v4/homepage.gif?v9',
	boingboing: 'http://boingboing.net/wp-content/themes/bb/sundries/logo.png',
	vimeo: 'http://a.vimeocdn.com/images/logo_vimeo_land.png',
	trib: 'http://www.chicagotribune.com/images/logo.png',
	nyt: 'http://i1.nyt.com/images/misc/nytlogo379x64.gif',
	nfl: 'http://i.nflcdn.com/static/site/3.11/img/global/alt/large-logo.png'
    },
    
    visipisiCB = function(vp, endCB, sites, urls, site, result) {
	if (result === null) {
	    //whoops
	} else {
	    results[site] = result;
	}
	var nextSite = sites.pop();
	if (nextSite) {
	    vp(urls[nextSite], function (result) {
		visipisiCB(vp, endCB, sites, urls, nextSite, result);
	    });
	} else {
	    endCB(results);
	}
    },
    
    visipisi = function(url, cb) {
	var start;
	var loaded = false;
	var runtest = function () {
	    window.removeEventListener("message", runtest, false);
	    var img = new Image();
	    start = new Date().getTime();
	    img.src = url;
	    var messageCB = function (e) {
		var now = new Date().getTime();
		if (img.complete) {
		    delete img;
		    window.removeEventListener("message", messageCB, false);
		    cbWrap(true);
		} else if (now - start > 10) {
		    delete img;
		    window.stop();
		    window.removeEventListener("message", messageCB, false);
		    cbWrap(false);
		} else {
		    window.postMessage('', '*');
		}
	    };
	    window.addEventListener("message", messageCB, false);
	    window.postMessage('', '*');
	};
	cbWrap = function (value) { cb(value); };
	window.addEventListener("message", runtest, false);
	window.postMessage('', '*');
    };
    
    
    window.visipisi = {};
    
    window.visipisi.get = function(endCB){
	results = {}; //reset it every time we call this.
	if (window.postMessage){
	    sites = [];
	    for (var k in urls)
		sites.push(k);
	    sites.reverse();
	    
	    vp = visipisi;
	    
	    var firstSite = sites.pop();
	    vp(urls[firstSite], function(result) {
		visipisiCB(vp, endCB, sites, urls, firstSite, result);
	    });
	} else {
	    endCB({});//empty results
	}}
})();