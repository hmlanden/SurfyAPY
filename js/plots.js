//process data
var stationArray = [];
stationDataset.forEach(function (data) {
    stationArray.push(data.name);
});

var latitudeArray = [];
stationDataset.forEach(function (data) {
    latitudeArray.push(data.latitude);
});

var longitudeArray = [];
stationDataset.forEach(function (data) {
    longitudeArray.push(data.longitude);
});


//plot data
var data = [{
    type: 'scattermapbox',
    lat: latitudeArray,
    lon: longitudeArray,
    mode: 'markers',
    marker: {
        size: 14
    },
    text: stationArray
}];

var layout = {
    autosize: true,
    hovermode: 'closest',
    title: 'Weather Stations in Dataset',
    mapbox: {
        bearing: 0,
        center: {
            lat: latitudeArray[0],
            lon: longitudeArray[0]
        },
        pitch: 0,
        zoom: 5,
        style: 'dark',
    },
    annotations: [{
        x: 0,
        y: 0,
        text: 'Source: Trilogy Education',
        showarrow: false
	 }]
}

Plotly.setPlotConfig({
    mapboxAccessToken: mapbox_access_token
});

Plotly.plot('plot', data, layout)
