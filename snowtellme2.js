// JS script Snotel Stations
/*
Big thought: instead of building the stations as separate objects from the markers, we should make the markers contain all of the information for a station
*/

var curDate = new Date();
var markerCluster;

var allStations = []

// I'm not sure why I set this width to 100 less than the window width
var infoMaxWidth = window.innerWidth - 100; 

// these info listeners are on each map marker
function addInfoListener(mark, markIndex) {
	mark[markIndex].infoWindow = new google.maps.InfoWindow({
    content: mark[markIndex].infoContent, // Sect
    maxWidth: infoMaxWidth
    });
	mark[markIndex].addListener('click', function () {
	// closes all of the open windows
		for (i=0; i < mark.length; i++) {
			mark[i].infoWindow.close();
		};
		// resets the info content
    		mark[markIndex].infoWindow.setContent(mark[markIndex].infoContent); // Sect
    		// opens the window
    		mark[markIndex].infoWindow.open(map, mark[markIndex]);
	});

}; // addInfoListener function
      
function doNothing(){};   

// this will contain all the information of the river section
var Station = function (id,title,lat,long,water=0,precip=0,dep=0,snow=0) {
		this.id = id;
		this.title = title;
		this.position = {lat: parseFloat(lat), lng: parseFloat(long)};
		this.snow = parseFloat(snow)||0;
		this.clabel = Math.round(this.snow) + '"';
		this.web = "https://wcc.sc.egov.usda.gov/nwcc/site?sitenum=" + this.id;
		this.rcolor = 'Blue';
		this.depth = parseFloat(dep)||0;
		this.infoContent = "<h3>" + this.title + " " + this.snow + "inches of new snow </h3>";
		this.infoContent += "<p><a href=" + this.web + " target='_blank'> Snotel Site </a></p>";
		this.infoContent += "<p>SWE Total: " + water + " inches of water this season </p>";
		this.infoContent += "<p>SWE New: " + precip + " inches of new water </p>";
		this.infoContent += "<p>Snow Depth: " + dep + " inches  </p>";
		if (precip > 0) {
		    this.infoContent += "<p>New Snow Ratio: " + (snow/precip).toFixed(2) + " snow / precip  </p>";
		}
		
		this.setColor = function() {
		    if (this.snow <= 0) {
		        this.rcolor = 'Brown'
		    } else if (this.snow <= 3) {
		        this.rcolor = 'Yellow'
		    } else if (this.snow <= 7) {
		        this.rcolor = 'Green'
		    } else if (this.snow <= 12) {
		        this.rcolor = 'Blue'
		    } else {
		        this.rcolor = 'Purple'
		    }
		}

		this.resetSect = function () {
			marker[this.markerNum].setMap(map);
			this.runSect = 1;		
		}; // resetSect function
		
		this.markerDifficulty = function () {
			marker[this.markerNum].setIcon({
				path: google.maps.SymbolPath.CIRCLE,
				scale: 18,
				fillColor: 'white',
				fillOpacity: 0.8,
				strokeWeight: 3,
				strokeColor: this.rcolor
			}); // creating the marker
		}; // markerDifficulty function
		
		this.markerColor = function (currentColor) {
			marker[this.markerNum].setIcon({
				path: google.maps.SymbolPath.CIRCLE,
				scale: 18,
				fillColor: 'white',
				fillOpacity: 0.8,
				strokeWeight: 3,
				strokeColor: currentColor
			});
		}; // markerFlow function		
};

// loads the Snotel Stations and adds all of the data to the allStations array
function LoadStat() {
	var strRawContents;
	$.ajax({
		url: "snow.csv",
		success: function(data){
			strRawContents = data;
			var arrLines = strRawContents.split("\n");
			for (i = 0; i < arrLines.length; i++) {
        			var tempArr = arrLines[i].split(",");
        			var tempStat = new Station(tempArr[0], tempArr[1], tempArr[2], tempArr[3], tempArr[4], tempArr[5], tempArr[6], tempArr[7])
        			tempStat.setColor()
        			allStations.push(tempStat)
        		};
		} // success	
	}); // ajax
	
	// onload command to make sure this loads after the google maps API is ready
    window.onload = function () {
        // createMarker Loop for all the stations
	    createMarker(allStations);
	    // for loop to create all of the river markers
        markerCluster = new MarkerClusterer(map, marker, clusterOptions);
        markerCluster.setMaxZoom(10);
    }; // window.onload

	
}; // LoadStat()

// initializes the clustering
var markerCluster = new Object();

// options object for the cluster
var clusterOptions = {
  'gridSize': 35,
  'averageCenter': true,
  'maxZoom': 9,
  'minimumClusterSize': 3,
  'imagePath': 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
};

// initializes the markers
var marker = [];
// initializes the infoWindow
var infoWindow = [];
// and the marker index
var markerIndex = 0;

// scale of icons on map
var iconScale = 18;
// stroke weight of icons on map
var iconStroke = 3;
// opacity of the icons
var iconOpacity = 0.65;

/*
createMark functions just creates a single marker. By abstracting this function out, we can refactor the code for more efficient operation
*/
function createMark(sect){
        marker[markerIndex] = new google.maps.Marker({
      	position: sect.position,
      	map: map,
      	snow: sect.snow,
      	snowId: sect.id,
      	infoContent: sect.infoContent,
       	label: sect.clabel,
        	title: sect.title,
        	icon: {
          	path: google.maps.SymbolPath.CIRCLE,
          	scale: iconScale,
          	strokeColor: sect.rcolor,
          	strokeWeight: iconStroke,
          	fillColor: 'white',
          	fillOpacity: iconOpacity
            } // icon details
    	}); // marker function
    // adds the info windows for each marker
    // function for creating the listener on the marker for the info window
    addInfoListener(marker, markerIndex);

    sect.markerNum = markerIndex;
    
};


/// NEED TO WORK ON THIS FUNCTION: WE NEED TO MAKE SURE THE DETAILS OF THIS FUNCTION
// HOW DOES THE INFO LISTENER WORK? DOES IT NEED TO POINT BACK TO THE OBJECT?



/* Marker function takes in a river array that is contains an array of River Section Objects. The function puts those markers on the map and then feeds the river array with the corresponding marker for later use (deletion) 
*/
function createMarker(river){
	// loop to create markers
	for (var sectIndex = 0; sectIndex < river.length; sectIndex++) {
    	marker[markerIndex] = new google.maps.Marker({
      	position: river[sectIndex].position,
      	map: map,
      	snow: river[sectIndex].snow,
      	snowId: river[sectIndex].id,
      	infoContent: river[sectIndex].infoContent,
       	label: river[sectIndex].clabel,
        	title: river[sectIndex].title,
        	icon: {
          	path: google.maps.SymbolPath.CIRCLE,
          	scale: iconScale,
          	strokeColor: river[sectIndex].rcolor,
          	strokeWeight: iconStroke,
          	fillColor: 'white',
          	fillOpacity: iconOpacity
            } // icon details
    	}); // marker function
    // adds the info windows for each marker
    // function for creating the listener on the marker for the info window
    addInfoListener(marker, markerIndex);

    river[sectIndex].markerNum = markerIndex;
    markerIndex++; // steps marker index to avoid overwriting
    }; // for loop for markers
}; // createMarker function


// create the map variable before the map initializing
var map;
// initializes the map
function initMap() {
	// zoom of map
	var mapZoom = 7;
	// center
	var mapCenter = {lat: 38.859391, lng: -107.169172};

  map = new google.maps.Map(document.getElementById('map'), {
    zoom: mapZoom,
    center: mapCenter
  });
// LOOP FOR CREATING MARKERS
}; //initMap function

// function for determining min and max snowfall and snow depth
function snowXtremes (stations){
	
	// maybe make an array of all of the snow values first - brute force
	snowfall = [];
	snowDepth = [];
	for (i=0; i < stations.length; i++ ){
	    snowfall.push(stations[i].snow);
	    snowDepth.push(stations[i].depth);
	    };
	// max and minimum snow fall
	max_snow = Math.max.apply(Math, snowfall);
	console.log(max_snow);
	min_snow = Math.min.apply(Math, snowfall);
	console.log(min_snow);
	
	// max and minimum snow depth
	max_depth = Math.max.apply(Math, snowDepth);
	console.log(max_depth);
	min_depth = Math.min.apply(Math, snowDepth);
	console.log(min_depth);
	
	
// 	console.log(Math.max.apply(Math, allStations.map(function(Obj) { return Obj.snow; })));
// 	console.log(Math.min.apply(Math, allStations.map(function(Obj) { return Obj.snow; })));
	
// 	// let's see all of the values
// 	console.log(allStations.map(function(Obj) { return Obj.snow; }));
}


// Loads station data
LoadStat();  // 

// need to delay the write to file to make sure everything loads in HTML
setTimeout(function(){snowXtremes(allStations)}, 3000);



var currentMarkers = [];


/*
Next: place all information and functions contained in the stations object into markers objects

*/


