import {Map} from '../zones/MapSingMarker.js'

window.onload = () => {
    const lista_aux = document.getElementById('coordinates').value;
    var is_type = document.getElementById('is_type').value;
    const map = new Map({
        selector: 'mapid',
        addSearch: false,
        coordinates: lista_aux,
        change: false,
        is_type: is_type        
    });
}
