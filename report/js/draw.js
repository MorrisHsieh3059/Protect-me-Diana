


function draw(severity) {
  var classify;

  if (severity <= 100 && severity >= 90){
    classify = 'white'
  };

  if (severity < 90 && severity >= 80){
    classify = 'red1'
  };

  if (severity < 80 && severity >= 70){
    classify = 'red2'
  };

  if (severity < 70 && severity >= 60){
    classify = 'red3'
  };

  if (severity < 60 && severity >= 50){
    classify = 'red4'
  };

  if (severity < 50 && severity >= 40){
    classify = 'red5'
  };

  if (severity < 40 && severity >= 30){
    classify = 'red6'
  };

  if (severity < 30 && severity >= 20){
    classify = 'red7'
  };

  if (severity < 20 && severity >= 10){
    classify = 'red8'
  };

  if (severity < 10 && severity >= 0){
    classify = 'red9'
  };

  return classify;
}
