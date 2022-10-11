// constantes
let initialLat = -34.9187;
let initialLng = -57.956;
let arrayPoly= [];

const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

export function Map({selector, addSearch, coordinates, change, is_type}) {
    //Propiedades
    let marker;
    let map;

    //Instanciación de mapa.
    initializeMap(selector);
    
    if(addSearch) {
        //si hay que poner el search en el mapa 
        //esto seria solo para un new, en el view no.
        addSearchControl();
    };    
    //creacion del mapa
    function initializeMap(selector) {
        //RENDERIZAR EL MAPA CON SU VISTA PRINCIPAL - Que se visualize el mapa
        if(((is_type=="complaint")||(is_type=="location"))&&(change== false)){
            //Si es un template "vista",
            //del tipo, "punto de encuentro" o "denuncia",
            //visualizar el map con cordenadas del maker)
            var arrayDeCoordenadas = coordinates.split(',');
            var lat = arrayDeCoordenadas[0];
            var long = arrayDeCoordenadas[1];
            map = L.map(selector).setView([lat, long], 13);
        }
        else{
            //Si no tiene coordenadas anteriormente seteadas, se setea en el centro de LP.
            map = L.map(selector).setView([initialLat, initialLng], 13);
        }
        L.tileLayer(mapLayerUrl).addTo(map); 
        
        //LOGICA PARA MANEJAR LOS MAKERS, POLYGON Y POLILINE
        if(change){
            //si hay que "cambiar"/ ya que es un new o un edit, entra aca
            if(is_type=="polyline"){
                if(coordinates!=0){
                    //si es un edit, ya que coordinates es distinto a 0
                    //seria 0 si es un new
                    //al ser un edit, hay que setear los anteriores markers
                    var coord = list_converter(coordinates); 
                    var polyline = L.polyline(coord).addTo(map);
                    map.fitBounds(polyline.getBounds());
                }
                //agrega los markers, sea para un new o edit
                map.addEventListener('click', (e) => {addMarkerPolyline(e.latlng)});
            }
            else if((is_type=="complaint")||(is_type=="location")){
                if(coordinates!=0){
                    //si es un edit, ya que coordinates es distinto a 0
                    //seria 0 si es un new
                    //al ser un edit, hay que setear el anterior marker
                    var arrayDeCoordenadas = coordinates.split(',');
                    var lat = arrayDeCoordenadas[0];
                    var long = arrayDeCoordenadas[1];
                    marker = L.marker([lat,long]).addTo(map);
                }
                //agrega el marker, sea para un new o edit
                map.addEventListener('click', (e) => {addMarker(e.latlng)});   
            }
        }
        else{
            //si no hay que "cambiar"/ ya que es un view
            if (is_type=="polyline"){
                //si es view de un polyline
                var coord = list_converter(coordinates); 
                var polyline = L.polyline(coord, {color: 'green'}).addTo(map);
                map.fitBounds(polyline.getBounds());
            }
            else if((is_type=="complaint")||(is_type=="location")){
                //si es un view de un marker (punto de encuentro)
                var arrayDeCoordenadas = coordinates.split(',');
                var lat = arrayDeCoordenadas[0];
                var long = arrayDeCoordenadas[1];
                marker = L.marker([lat,long]).addTo(map);
            }
        }
    };

    function list_converter(coord) {
        // Le saco los caracteres [ y ] del principio y del final respectivamente
        var aux = coord.substring(1).slice(0,-1);
        aux = aux.split(", ");
        const resultado = [];
        for (let i in aux) {
          var temp = aux[i].split(",");
          var latlng = L.latLng(temp[0].substring(1), temp[1].slice(0, -1));
          resultado.push(latlng);
        }
        return resultado;
    };

    //comportamiento
    function addMarker({lat, lng}) {
        if(marker) {
            marker.remove();
        };
        marker = L.marker([lat, lng]).addTo(map);
    };
    function addMarkerPolyline({lat, lng}) {
        //agrega el maker en el mapa
        marker = L.marker([lat, lng]).addTo(map);
        //agregar al arreglo cada marker en forma de [lat,long]
        if (arrayPoly.length == 0){
            arrayPoly.push('['+lat+','+lng+']');
        }
        else{
            arrayPoly.push(' ['+lat+','+lng+']');
        }
    };
    function addSearchControl() {
        L.control.scale().addTo(map);
        let searchControl = new L.esri.Controls.Geosearch().addTo(map);

        let results = new L.LayerGroup().addTo(map);

        searchControl.on('results', (data) => {
            results.clearLayers();
            if (data.results.length > 0) {
                addMarker(data.results[0].latlng);
            }
        });
    };
    return{
        get marker() {return marker},
        addMarker: addMarker,
        arrayPoly: arrayPoly
    };

}