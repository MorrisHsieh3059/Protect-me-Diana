//for zoom_change
var Taipei = ol.proj.fromLonLat([121.555558, 25.072948])
var Keelung = ol.proj.fromLonLat([121.723801, 25.130247])
var Newtaipei = ol.proj.fromLonLat([121.596121, 25.010076])
var Yeeelan = ol.proj.fromLonLat([121.645922, 24.600284])
var Taoyuan = ol.proj.fromLonLat([121.280965, 24.884941])
var Xinchu_city = ol.proj.fromLonLat([120.942488, 24.787515])
var Xinchu = ol.proj.fromLonLat([121.166126, 24.670291])
var Miaoli = ol.proj.fromLonLat([120.905051, 24.498282])
var Taizhong = ol.proj.fromLonLat([120.937755, 24.225453])
var Zhanghua = ol.proj.fromLonLat([120.484475, 23.965178])
var Nantou = ol.proj.fromLonLat([120.981433, 23.811067])
var Jiayi_city = ol.proj.fromLonLat([120.444489, 23.483047])
var Jiayi = ol.proj.fromLonLat([120.508871, 23.474318])
var Yunlin = ol.proj.fromLonLat([120.395599, 23.727391])
var Tainan = ol.proj.fromLonLat([120.328989, 23.152469])
var Kaoshong = ol.proj.fromLonLat([120.605279, 22.971507])
var Ponghu = ol.proj.fromLonLat([119.618139, 23.566545])
var Jingman = ol.proj.fromLonLat([118.380078, 24.440651])
var Pingdon = ol.proj.fromLonLat([120.625981, 22.370858])
var Taidong = ol.proj.fromLonLat([121.052658, 22.845853])
var Hualian = ol.proj.fromLonLat([121.411609, 23.815980])
var LianJian = ol.proj.fromLonLat([119.953364, 26.180745])


// 移動到 選擇的縣市
function doPan(location) {

  view.animate({
    center: location,
    duration: 1500
  });

}

// Zoom in 到 選擇的縣市
function doZoom(location) {
  var Zoom;

  if (location == Xinchu_city || location == Jiayi_city) {
    Zoom = 12.4;
  } else if (location == Taipei || location == Keelung || location == Jingman) {
    Zoom = 11.5;
  } else if (location == Zhanghua) {
    Zoom = 11;
  } else if (location == Nantou) {
    Zoom = 9.9;
  } else if (location == Kaoshong || location == Pingdon || location == Taidong) {
    Zoom = 9.7;
  } else if (location == Hualian) {
    Zoom = 9.3;
  } else if (location == "point") {
    Zoom = 16.8
  } else if (location == "pointToPoint") {
    Zoom = 13.8
  } else {
    Zoom = 10.2;
  }
  view.animate({
    zoom: Zoom,
    duration: 1500
  });
}

function moveCity(location) {

  doPan(location);
  setTimeout(function() {
    doZoom(location);
  }, 1300);

}

function movePoint(center, zoom, done) {
  if (done == "pointToPoint") {
    doZoom(done);
  }

  setTimeout(function() {
    doPan(center);
  }, 700);
  setTimeout(function() {
    doZoom(zoom);
  }, 1500);

}


// check clear or not
var check;
//connect to table
var bridge = new Array(x);
var feature = new Array(x);

function plot(items) {

  var lat, lng, coordinate;
  var count = 0;

  if (check == 1) {
    feature = new Array(count);
  }

  for (i in items) {
    lat = parseFloat(items[i]['latitude']);
    lng = parseFloat(items[i]['longitude']);
    bridge[count] = [lng, lat];
    // console.log(bridge[count]);

    coordinate = ol.proj.fromLonLat([lng, lat]);
    feature[i] = new ol.Feature(new ol.geom.Point(coordinate));
    feature = Object.keys(feature).map(function(key) {
      return feature[key];
    });

    count = count + 1;
  }



  var source = new ol.source.Vector({
    features: feature
  });
  // l = map.getLayers().getArray()[2];
  // l.setSource(source);
  var pointLayer = new ol.layer.Vector({
    source: source
  });
  // console.log(map.getLayers().getArray()[2])
  map.getLayers().getArray()[2] = pointLayer;

  // console.log(map.getLayers());
  check = 1;
}

//-----------------------------------

var popup_check = 0;

function popupFunc(geojson, school, coor) {

  popup = new ol.Overlay({
    element: $("<div />").addClass('info').append( //put a table to element parameter
      $("<table />").addClass('mdl-data-table mdl-js-data-table mdl-data-table--unselectable mdl-shadow--2dp').append(
        $("<thead />").append(
          $("<tr />").append(
            $("<th />").addClass("mdl-data-table__cell--non-numeric").html("類別")
          ).append(
            $("<th />").html("學校資訊")
          )
        )
      ).append(
        $("<tbody />").append(
          $("<tr />").append(
            $("<td />").html("學校")
          ).append(
            $("<td />").html(school)
          )
        ).append(
          $("<tr />").append(
            $("<td />").html("負責人")
          ).append(
            $("<td />").html(geojson["name"])
          )
        ).append(
          $("<tr />").append(
            $("<td />").html("電話")
          ).append(
            $("<td />").html(geojson["phone"])
          )
        ).append(
          $("<tr />").append(
            $("<td />").html("地址")
          ).append(
            $("<td />").html(geojson["address"])
          )
        )
      )
    )[0]
  });
  popup.setPosition(ol.proj.fromLonLat(coor));
  map.addOverlay(popup);
  // console.log(map.getLayers());
  popup_check = 1;
}


//-----------------------------------
var lastSelect = 0;

function selectedrow() {
  var rowcount = $('#table1 tbody tr').length;
  var index, view, lat, lng, coor, center, zoom,
    table = document.getElementById('table1');

  //setView

  for (var i = 0; i < rowcount; i++) {

    table.rows[i].onclick = function() {

      index = this.rowIndex;
      // this.classList.toggle('selected');
      console.log(index);
      //console.log(feature[index-1]);

      center = feature[index - 1]["N"]["geometry"]["A"];
      zoom = "point";
      if (lastSelect != index) {
        if (map.getView().getZoom() == 16.8) {
          movePoint(center, zoom, 'pointToPoint');
        } else {
          movePoint(center, zoom, 'firstTime');
        }
      }

      lastSelect = index;

      if (popup_check == 1) {
        map.removeOverlay(popup);
      }

      // connect to geojson
      for (i in geojson) {
        lat = parseFloat(geojson[i]["latitude"]);
        lng = parseFloat(geojson[i]["longitude"]);
        coor = [lng, lat];

        if (coor[0] == bridge[index - 1][0]) {
          // console.log(geojson[i]);
          // console.log(Object.keys(geojson)[index-1]);
          // console.log(coor)
          popupFunc(geojson[i], Object.keys(geojson)[index - 1], coor);

        }
      }
    }
  };
};


//Choose City change District
function changeCity(location) {

  var City = location;
  var put = [Taipei, Keelung, Newtaipei, Yeeelan, Taoyuan, Xinchu_city, Xinchu,
    Miaoli, Taizhong, Zhanghua, Nantou, Jiayi_city, Jiayi, Yunlin,
    Tainan, Kaoshong, Ponghu, Jingman, Pingdon, Taidong, Hualian, LianJian
  ];
  var chinese = ['臺北市', "基隆市", "新北市", "宜蘭縣", "桃園縣", "新竹市", "新竹縣",
    "苗栗縣", "臺中市", "彰化縣", "南投縣", "嘉義市", "嘉義縣", "雲林縣",
    "臺南市", "高雄市", "澎湖縣", "金門縣", "屏東縣", "臺東縣", "花蓮縣", "連江縣"
  ];

  for (i = 0; i < 22; i++) {
    if (City == chinese[i]) {
      poke(City);
      moveCity(put[i]);
    }
  }
}

//-----------------------------------------------
//"pointermove geojson"
var select = new ol.interaction.Select({
  condition: ol.events.condition.pointerMove,
  style: new ol.style.Style({
    stroke: new ol.style.Stroke({
      width: 3,
      color: '#33CCFF'
    }),
    fill: new ol.style.Fill({
      color: [215, 40, 0, 0]
    })
  })
});

if (select !== null) {
  map.addInteraction(select);
}

function add_interaction() {
  //console.log(123);
  map.addInteraction(select);
}

//del_interaction
function del_interaction() {
  map.removeInteraction(select);
}


//----------------------------------------------------
//"click"
var featureName;
var displayFeatureInfo = function(pixel) {

  var feature = map.forEachFeatureAtPixel(pixel, function(feature) {
    return feature;
  });

  if (feature) {
    //console.log(feature.get('name'));
    featureName = feature.get('name');
    changeCity(featureName);
  }
};

map.on('singleclick', function(evt) {
  //change city delete popup
  if (popup_check == 1) {
    map.removeOverlay(popup);
  }

  if (evt.dragging) {
    return;
  }
  //console.log(evt.originalEvent);
  var pixel = map.getEventPixel(evt.originalEvent);
  displayFeatureInfo(pixel);
});
