<template>
<!-- Titulo -->
    <h2 id="titleCustom">Zonas inundables</h2>
<!-- Mapa -->
<div>
  <l-map style="height:350px;width:350px;display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;" :zoom="zoom" :center="center">
    <l-tile-layer :url="url"></l-tile-layer>
    <div v-for="(zone, index) in zones" :key="`zones-${index}`">
      <l-polygon :lat-lngs="[JSON.parse(zone.coordinates)]" :color="zone.color" :fill="true" :fillColor="zone.color" :fillOpacity="0.5"/>
    </div>
  </l-map>
</div>

<!-- Tabla -->
<table class="table">
  <thead>
    <tr>
      <th scope="col">Codigo</th>
      <th scope="col">Nombre</th>
      <th scope="col">Color</th>
      <th scope="col">Estado</th>
    </tr>
  </thead>
  <tbody  v-for="(zone, index) in zones" :key="`zones-${index}`">
    <tr>
      <th scope="row">{{zone.code}}</th>
      <td>{{zone.name}}</td>
      <td>
        <input type="color" :value="zone.color" disabled>
      </td>
      <td v-if="zone.status== 'True'">✔️</td>
      <td v-else>❌</td>
      <td>
        <a class="btn btn-sm btn-warning" style="text-decoration:none;">
          <router-link :to="`/inundable/${zone.id}`">
            👁️
          </router-link>
        </a>
      </td>
    </tr>
  </tbody>
</table>

<div>
  <button class="btn btn-sm btn-info" v-if="this.actual_page==1" disabled>Anterior</button>
  <button class="btn btn-sm btn-info" v-else @click="this.getData(previous_page)">Anterior</button><h6>Pagina {{actual_page}} de {{total_pages}}</h6>
  <button class="btn btn-sm btn-info" v-if="this.actual_page==this.total_pages" disabled>Siguiente</button>
  <button class="btn btn-sm btn-info" v-else @click="this.getData(next_page)">Siguiente</button>
</div>


<br>

<div>
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
    };
  },
  created() {
    fetch(`${process.env.VUE_APP_API}/api/zonas-inundables/?page=${this.actual_page}&per_page=${this.per_page}`).then((response) => {
      return response.json();
    }).then((json) => {
      this.zones=json.inundables

      this.total_elements=parseInt(json.total)
      this.total_pages=Math.ceil(this.total_elements/this.per_page)

      if (this.total_pages > this.actual_page){
        this.next_page=parseInt(json.pagina) + 1
      }
      
      if (this.actual_page > 1){
        this.previous_page=parseInt(json.pagina) - 1
      }
      
      this.actual_elements = 0

      for (let index = 1; index < this.total_pages-this.actual_page; index++) {
        this.actual_elements = this.actual_elements+this.per_page
      }
      this.actual_elements=this.actual_elements + parseInt(json.inundables.length)
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
        
        this.actual_page=parseInt(json.pagina)
        if (this.total_pages > this.actual_page){
          this.next_page=parseInt(json.pagina) + 1
        }
        
        if (this.actual_page > 1){
          this.previous_page=parseInt(json.pagina) - 1
        }

      }).catch((e) => {
        console.log(e)
      })
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
