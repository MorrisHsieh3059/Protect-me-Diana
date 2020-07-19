
function sort(json) {
    var sortable = [];
    for (let school in json) {
        if (json[school]["YN"][0] != 0) {
            sortable.push([school, json[school]["severity"]]);
        }
    }

    sortable.sort(function(a, b) {
        return b[1] - a[1];
    });

    //append 未填答
    for (let school in json) {
        if (json[school]["YN"][0] == 0) {
            sortable.push([school, json[school]["severity"]]);
        }
    }

    var newItems = new Array;
    var obj = {};

    for (i in sortable) {
        for (school in json) {
            if (school == sortable[i][0]) {
                obj[school] = json[school];
                // newItems.push(j);
            }
        }
    }

    return obj;
}


var x = 0;
var geojson;
var userid = new Object;

function detailTable(items) {
    geojson = items;
    $("#detailTable tbody tr").remove();

    for (i in items) {
        var one, two, three;
        one = items[i]['name'];
        two = items[i]['phone'];
        three = items[i]['YN'];
        userid[i] = items[i]["userid"];
        severity = draw(items[i]["severity"]);

        var tr = $('#detailTable').append($('<tr />').addClass(severity)
            .click(function() {
                loadBuilding(geojson[$(this).find('td').html()]['school_id'], geojson[$(this).find('td').html()]['userid']);
            })
            .append($('<td />').addClass('mdl-data-table__cell--non-numeric').html(i))
            .append($('<td />').html(one).attr('style', 'text-align: center;'))
            .append($('<td />').html(two))
            .append($('<td />').html(three).attr('style', 'text-align: center;'))
            .append($('<td />').html(items[i]["severity"]).attr('style', 'text-align: center;')));

        x = x + 1;
    }

    hoverRow();
    x = 0;
}
