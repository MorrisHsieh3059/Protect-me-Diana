

function buildingModal(data, userid) {
    console.log(data);
    var assessment_id = data["assessment_id"];
    var dialog = document.querySelector('#building-modal');
    dialog.showModal();

    $('.close1').click(function () {
        dialog.close();
    });


    $('#buildingTitle').html(data['school_name'])
    $("#buildingTable tbody tr").remove();

    var one, two, three, color, severity;
    for (var i = 0; i < data['building_id'].length; i++) {
        one = data['school_name'];
        two = data['building_name'][i];
        three = data['yn'][i] == true ? "已填答" : "未填答";
        severity = data['severity'][i];

        // color = draw(data["severity"][i]);

        var tr = $('#buildingTable tbody').append($('<tr />').addClass(color)
            .click(function() {
                loadDetail(userid, assessment_id, data["building_id"][$(this).index()], $(this).find('td:nth-child(2)').text());
            })
            .append($('<td />').addClass('mdl-data-table__cell--non-numeric').html(one))
            .append($('<td />').html(two).attr('style', 'text-align: center;'))
            .append($('<td />').html(three))
            .append($('<td />').html(severity).attr('style', 'text-align: center;')));
    }
}




function detailModal(data, building_name) {
    // console.log(data);
    // console.log(geojson);
    var dialog2 = document.querySelector('#detail-modal');
    dialog2.showModal();

    $('.close2').click(function () {
        dialog2.close();
    });

    $('#detail-title').html($('#buildingTitle').text() + "  " + building_name);
    $("#modal-detail-table tbody tr").remove();


    var problemNumbers = Object.keys(data);
    var one, two, three, color, severity;
    for (var i in data) {
        one = data[i]['question'];
        two = data[i]['content'];
        three = data[i]['description'];
        four = data[i]['img_url'];
        five = data[i]['pos'];

        // color = draw(data["severity"][i]);

        var tr = $('#modal-detail-table tbody').append($('<tr />').addClass(color)
            .append($('<td />').addClass('mdl-data-table__cell--non-numeric').html(one))
            .append($('<td />').html(two).attr('style', 'text-align: center;'))
            .append($('<td />').html(three).attr('style', 'text-align: center;'))
            .append($('<td />').append($('<a />').attr('href', four).attr('target', '_blank').html('link'))
                .attr('style', 'text-align: center;'))
            .append($('<td />').html(five).attr('style', 'text-align: center;')));
    }
}
