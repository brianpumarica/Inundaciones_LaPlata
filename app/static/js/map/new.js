//import {Map} from '../../MapSingMarker.js'
import {Map} from '../zones/MapSingMarker.js'

const submitHandler = (event, map, is_type) => {
    if(!map.marker) {
        event.preventDefault(); 
        alert('Debes seleccionar la ubicacion del mapa.');
    }
    else{
        if((is_type=="complaint")||(is_type=="location")){
            //si es denuncia o punto de encuentro
            let lating = map.marker.getLatLng();
            let aux = lating.toString();
            let aux1 = aux.substring(1).slice(6,-1);
            document.getElementById('coordinates').value = aux1;
        }
        else{
            //si es recorrido 
            document.getElementById('coordinates').value = '['+map.arrayPoly+']';
            }
    }
}

window.onload = () => {
    var is_type = document.getElementById('is_type').value;
    let map = new Map({
        selector: 'mapid',
        addSearch: true,
        coordinates: 0,
        change: true,
        is_type: is_type 
    });
    let form = document.getElementById('create-form');
    form.addEventListener('submit', (event) => submitHandler(event, map, is_type)); 
}