$(function() {
    var overallData;
    loadEvent(); // request for event
})

// show detail table
// function show() {
//     $('#dialog1').modal('show');
// }

function changeEvent(cat) {
    if (cat == 'overview') {
        loadOverall($('#eventSel1').val());
    } else if (cat == 'details') {
        loadFetch($('#countySel2').val());
    }
}

$('#scroll-tab-1').click(() => {
    setTimeout( function() { mapDraw.updateSize();}, 100);
});
$('#scroll-tab-2').click(() => {
    setTimeout( function() { map.updateSize();}, 100);
});

$(window).resize(function(){
    loadChart();    // chart resize
})
