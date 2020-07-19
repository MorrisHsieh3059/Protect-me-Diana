function loadEvent() { // load event data via ajax

    var url_load = "https://pmdiana.hcilab.katrina.tw/event";
    $.ajax({
        url: url_load,
        dataType: "json",
        success: function(items) {
            event(items);
            loadOverall($('#eventSel1').val()); // load Overall
            loadFetch($('#countySel2 option:selected').text());
        }
    });
}

function event(items) {
    for (i in items) {
        var tr = $('.eventSel').append($('<option />').attr("value", items[i]["assessment_id"]).html(items[i]["event"]));
    }

    $(".eventSel").val(items[1]["assessment_id"]);
}

function loadOverall(ass_id) { // load event data via ajax

    var url_load = "https://pmdiana.hcilab.katrina.tw/overall?assessment_id=" + ass_id;
    $.ajax({
        url: url_load,
        dataType: "json",
        success: function(items) {
            overallData = items;
            loadChart(); // load Crossfilter
            mapInit();
        }
    });
}

function loadFetch(county) {

    var ass_id;
    if ($('#eventSel2').val()) {
        ass_id = $('#eventSel2').val();
    }

    var url_fetch = "https://pmdiana.hcilab.katrina.tw/fetch?county=" + county + "&assessment_id=" + ass_id;

    $.ajax({
        url: url_fetch,
        dataType: "json",
        success: function(items) {
            items = sort(items);
            detailTable(items);
            plotPoint(items);
        }
    });
}


function loadBuilding(school_id, userid) {

    var url_building = "https://pmdiana.hcilab.katrina.tw/building?school_id=" + school_id + "&assessment_id=" + $('#eventSel2').val();

    $.ajax({
        url: url_building,
        dataType: "json",
        success: function(items) {
            buildingModal(items, userid);
        }
    });
}

function loadDetail(userid, ass_id, building_id, building_name) {

    var url_detail = "https://pmdiana.hcilab.katrina.tw/detail?userid=" + userid + "&assessment_id=" + ass_id + "&building_id=" + building_id;

    $.ajax({
        url: url_detail,
        dataType: "json",
        success: function(items) {
            detailModal(items, building_name);
        }
    });
}
