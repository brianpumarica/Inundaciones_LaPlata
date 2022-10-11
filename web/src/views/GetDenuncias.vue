<template>
<!-- Titulo -->
    <h2 id="titleCustom">Denuncias realizadas</h2>
<!-- Mapa -->
<div id="app">
  <l-map style="height:350px;width:350px;display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;" :zoom="zoom" :center="center">
    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
    <div v-for="(complaint, index) in complaints" :key="`${index}`">
      <l-marker
        :key="'marker-' + index"
        :lat-lng="complaint.mappedCoordinates">
        <l-tooltip>{{complaint.title}}</l-tooltip>
      </l-marker>
    </div>
  </l-map>
</div>

<!-- Tabla -->
<table class="table">
  <thead>
    <tr>
      <th scope="col">Categoría</th>
      <th scope="col">Titulo</th>
      <th scope="col">Descripcion</th>
      <th scope="col">Denunciante</th>
      <th scope="col">Estado</th>
    </tr>
  </thead>
  <tbody  v-for="(complaint, index) in complaints" :key="`complaints-${index}`">
    <tr>
      <!-- <th scope="row">{{complaint.category}}</th> -->
      <th scope="row">{{this.parseCategory(complaint.category)}}</th>
      <td>{{complaint.title}}</td>
      <td>{{complaint.description}}</td>
      <td>{{complaint.name_user}} {{complaint.surname_user}}</td>
      <td>{{this.parseStatus(complaint.status)}}</td>
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
import {LMap, LTileLayer, LMarker, LTooltip} from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LTooltip
  },
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 10,
      center: [-34.92149, -57.954597],
      markerLatLng: [47.313220, -1.319482],
      complaints: [],
      actual_page: 1,
      per_page: 2,
      total_elements: 0,
      actual_elements: 0,
      total_pages: 0,
    };
  },
  created() {
    fetch(`${process.env.VUE_APP_API}/api/complaints/?page=${this.actual_page}&per_page=${this.per_page}`).then((response) => {
      return response.json();
    }).then((json) => {
      this.complaints=json.complaints.map((complaint) =>
          ({
            ...complaint,
            mappedCoordinates:
              complaint.coordinates.split(',')
          })
        )

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
      this.actual_elements=this.actual_elements + parseInt(json.complaints.length)
    }).catch((e) => {
      console.log(e)
    })
  },
  methods: {
    getData(page){
      fetch(`${process.env.VUE_APP_API}/api/complaints/?page=${page}&per_page=${this.per_page}`).then((response) => {
        return response.json();
      }).then((json) => {
        this.complaints=json.complaints.map((complaint) =>
          ({
            ...complaint,
            mappedCoordinates:
              complaint.coordinates.split(',')
          })
        )
        
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
    },
    parseCategory(cat)
    {
      if (cat == 0)
      {
        return "Alcantarillas tapadas"
      }
      else if (cat == 1)
      {
        return "Basurales"
      }
      else
      { return "Otros"}
    },
    parseStatus(stat)
    {
      if (stat == 0)
      {
        return "Sin confirmar"
      }
      else if (stat == 1)
      {
        return "En curso"
      }
      else if (stat == 2)
      {
        return "Resuelta"
      }
      else
      { return "Cerrada"}
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
