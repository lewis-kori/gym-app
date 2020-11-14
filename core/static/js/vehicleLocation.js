const mapContainer = document.getElementById('map'),
    tableBody = $("#records-table-body"),
    violationsBody = $("#violations-table-body"),
    // const reportSocket = new WebSocket(`ws://${window.location.host}/ws/reports/${reg}`),
    reg = $(mapContainer).attr("data-reg"),
    reportSocket = new WebSocket(`ws://167.172.136.85/ws/reports/${reg}`);

let map, marker, recent_reports_json = [];


function initMap() {
    map = new google.maps.Map(mapContainer, {
        center: {lat: 9.01617, lng: 38.79053},
        zoom: 17
    });
}


function setMarker(report) {
    let coords = {lat: parseFloat(report.latitude), lng: parseFloat(report.longitude)};
    marker = new google.maps.Marker({position: coords, map: map});
    if (map) {
        map.setCenter(coords);
    }
}


tableBody.html("<tr class='text-center'><td colspan='5'>Loading...</td></tr>");


reportSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const recent_reports = data['recent_reports'];
    const new_report = data['new_report'];
    let bodyContent = "";

    if (recent_reports) {
        recent_reports_json = JSON.parse(recent_reports).map(report => report.fields);
    } else if (new_report) {
        if (recent_reports_json.length > 9) {
            recent_reports_json.pop();
        }
        recent_reports_json.unshift(JSON.parse(new_report));
    }

    recent_reports_json.forEach(report => {
        bodyContent += `<tr>
                        <td>${report.date}</td>
                        <td>${report.time}</td>
                        <td>${report.speed}</td>
                        <td>${report.latitude} ${report.latitude_dir}</td>
                        <td>${report.longitude} ${report.longitude_dir}</td>
                    </tr>`
    });

    tableBody.html(bodyContent);
    if (recent_reports_json.length === 0) {
        tableBody.html("<tr class='text-center'><td colspan='5'>No reports found.</td></tr>");
    } else {
        initMap();
        setMarker(recent_reports_json[0]);
    }
};


reportSocket.onclose = function (e) {
    console.error("Reports socket closed.");
};


$(window).bind('beforeunload', function () {
    console.log("unloading");
    reportSocket.close(1000, 'Page unloading');
});


$.ajax({
    url: `http://omata.skyetechgroup.com/violations/${reg}`,
    dataType: "json",
    success: function (violations) {
        const rows = violations.slice(0, 10).map(violation => {
            return "<tr>" +
                `<td>${violation.report.date}</td>` +
                `<td>${violation.report.time}</td>` +
                `<td>${violation.report.speed}</td>` +
                `<td>${violation.report.latitude} ${violation.report.latitude_dir}</td>` +
                `<td>${violation.report.longitude} ${violation.report.longitude_dir}</td>` +
                `<td>${violation.type}</td>` +
                "</tr>";
        });
        if (violations.length > 0) {
            $(violationsBody).html(rows);
        }
    }
})
