<template>
<!-- Titulo -->
    <h1 id="titleCustom">Zona inundable #{{ $route.params.id }}</h1>
<!-- Mapa -->

  <!-- Mapa -->
<l-map style="height:250px;width:250px;display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;"
  :zoom="zoom" :center="center">
  <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
  <l-polygon :lat-lngs="JSON.parse(zone.coordinates)" :color="zone.color" :fill="true" :fillColor="zone.color" :fillOpacity="0.5"></l-polygon>
</l-map>
  <div class="card-body">
    <h5 class="card-title">{{ this.zone.name }}</h5>
    <p class="card-text">Para exportar la lista de coordenadas, <a href="" @click="imprimir()" >click aqui</a>.</p>
  </div>
    <li class="list-group-item list-group-item-action">Código: {{ this.zone.code }}</li>
    <li class="list-group-item list-group-item-action">
              <input type="color" :value="this.zone.color" disabled>
</li>

<br>

<div>
    <a @click="$router.go(-1)" class="btn btn-warning">Volver atrás</a>
    &nbsp;
    <router-link to="/" class="btn btn-info">Volver al inicio</router-link>
</div>

</template>

<script>
import {LMap, LTileLayer, LPolygon} from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LPolygon
  },
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 10,
      center: [-34.92149, -57.954597],
      zones: [],
      actual_page: 1,
      per_page: 2,
      total_elements: 0,
      actual_elements: 0,
      total_pages: 0,

      actual_route: this.$route.params.id,
      code: 0,
      color: "",
      coordinates: [],
      name: "",
      status: "",
      zone:"",
    };
  },
  created() {
    fetch(`${process.env.VUE_APP_API}/api/zonas-inundables/${this.actual_route}`).then((response) => {
      return response.json();
    }).then((json) => {
      this.zone=json.inundable
      this.code=json.code
      this.color=json.color
      this.coordinates=json.coordinates
      this.name=json.name
      this.status=json.status
    }).catch((e) => {
      console.log(e)
    })
  },
  methods: {
    getData(page){
      fetch(`${process.env.VUE_APP_API}/api/zonas-inundables/?page=${page}&per_page=${this.per_page}`).then((response) => {
        return response.json();
      }).then((json) => {
        this.zones=json.inundables

      }).catch((e) => {
        console.log(e)
      })
    },
    imprimir(){
      var win = window.open();
      self.focus();
      win.document.open();
      win.document.write('<'+'html'+'><'+'body'+'>');
      win.document.write(this.zone.coordinates);
      win.document.write('<'+'/body'+'><'+'/html'+'>');
      win.document.close();
      win.print();
      win.close();
    }
  }
}
</script>

<style scoped>
.align-pagination {
  height:      40px;  
  line-height: 40px; /* Same as height  */
}
</style>