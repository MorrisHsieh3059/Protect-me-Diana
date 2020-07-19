



function detail (items) {
  $("#table2 tbody tr").remove();

  for(i in items){
    var tr=$('#table2')
      .append($('<tr />')
      .append($('<td />').addClass('center aligned').html(items[i]["content"]))
      .append($('<td />').addClass('center aligned').html(items[i]["question"]))
      .append($('<td />').addClass('right aligned').html(items[i]["description"])))

  }
}
