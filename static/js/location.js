var markers = [];
    
var mapContainer = document.getElementById('map1'),
    mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567),
        level: 3
    };  

var ps = new kakao.maps.services.Places();  

var infowindow = new kakao.maps.InfoWindow({zIndex:1});

searchPlaces();

function searchPlaces() {
    document.getElementById('placesList').style.display = 'block';
    var keyword = document.getElementById('search_input').value;

    if (!keyword.replace(/^\s+|\s+$/g, '')) {
        alert('키워드를 입력해주세요!');
        return false;
    }

    ps.keywordSearch( keyword, placesSearchCB); 
}

function placesSearchCB(data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {
        displayPlaces(data);

        displayPagination(pagination);

    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {

        alert('검색 결과가 존재하지 않습니다.');
        return;

    } else if (status === kakao.maps.services.Status.ERROR) {

        alert('검색 결과 중 오류가 발생했습니다.');
        return;

    }
}

function displayPlaces(places) {

    var listEl = document.getElementById('placesList'), 
    menuEl = document.getElementById('search_input_box1'),
    fragment = document.createDocumentFragment(), 
    bounds = new kakao.maps.LatLngBounds(), 
    listStr = '';

    removeAllChildNods(listEl);

    removeMarker();

    for ( var i=0; i<places.length; i++ ) {
        var placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
            marker = addMarker(placePosition, i), 
            itemEl = getListItem(i, places[i]);
        bounds.extend(placePosition);
        (function(marker, title) {
            kakao.maps.event.addListener(marker, 'mouseover', function() {
                displayInfowindow(marker, title);
            });

            kakao.maps.event.addListener(marker, 'mouseout', function() {
                infowindow.close();
            });

            itemEl.onmouseover =  function () {
                displayInfowindow(marker, title);
            };

            itemEl.onmouseout =  function () {
                infowindow.close();
            };
        })(marker, places[i].place_name);

        fragment.appendChild(itemEl);
    }

    listEl.appendChild(fragment);
    menuEl.scrollTop = 0;
}

function getListItem(index, places) {

    var el = document.createElement('li'),
    itemStr = '<div class="info" onclick=" location.replace('+"'/location/latitude="+places.y+"/longitude="+places.x +'/'+places.place_name+"')"+'"'+">" +
                '   <span style="font-size:20px;">' + places.place_name + '</span>';

    if (places.road_address_name) {
        itemStr += '  <br>  <span style="font-size:15px; color:grey;">' + places.road_address_name + '</span>'
    } else {
        itemStr += '  <br>  <span style="font-size:15px; color:grey;">' +  places.address_name  + '</span>'; 
    }
                 
      itemStr += '</div>'

    el.innerHTML = itemStr;
    el.className = 'item';

    return el;
}

function addMarker(position, idx, title) {
    var imageSrc = 'http://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png',
        imageSize = new kakao.maps.Size(36, 37),
        imgOptions =  {
            spriteSize : new kakao.maps.Size(36, 691),
            spriteOrigin : new kakao.maps.Point(0, (idx*46)+10),
            offset: new kakao.maps.Point(13, 37)
        },
        markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions),
            marker = new kakao.maps.Marker({
            position: position,
            image: markerImage 
        });    
    return marker;
}

function removeMarker() {
    for ( var i = 0; i < markers.length; i++ ) {
        markers[i].setMap(null);
    }   
    markers = [];
}

function displayPagination(pagination) {
    var paginationEl = document.getElementById('pagination'),
        fragment = document.createDocumentFragment(),
        i; 

    while (paginationEl.hasChildNodes()) {
        paginationEl.removeChild (paginationEl.lastChild);
    }

    for (i=1; i<=pagination.last; i++) {
        var el = document.createElement('a');
        el.href = "#";
        el.innerHTML = i;

        if (i===pagination.current) {
            el.className = 'on';
        } else {
            el.onclick = (function(i) {
                return function() {
                    pagination.gotoPage(i);
                }
            })(i);
        }

        fragment.appendChild(el);
    }
    paginationEl.appendChild(fragment);
}

function displayInfowindow(marker, title) {
    var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

    infowindow.setContent(content);
}

function removeAllChildNods(el) {   
    while (el.hasChildNodes()) {
        el.removeChild (el.lastChild);
    }
}
