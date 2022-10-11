<template>

  <!-- Titulo -->
      <h2 id="titleCustom">Puntos de encuentro y recorridos de evacuación</h2>

  <!-- Mapa -->
  <div>
    <l-map style="height:350px;width:350px;display: block;
    margin-left: auto;
    margin-right: auto;
    width: 50%;" :zoom="zoom" :center="center">
      <l-tile-layer :url="url"></l-tile-layer>
      <div v-for="(route, index) in routes" :key="`routes-${index}`">
        
        <l-polyline v-if="route.status== 'True'" :lat-lngs="route.coordinates" :color="'#00FF00'">
          <l-tooltip>{{route.name}}</l-tooltip>
        </l-polyline>

        <l-polyline v-else :lat-lngs="route.coordinates" :color="'#880808'">
          <l-tooltip>{{route.name}}</l-tooltip>
        </l-polyline>
      </div>
      <div v-for="(location, index) in locations" :key="`locations-${index}`">
        <l-marker  v-if="location.status== '1'" :lat-lng="location.mappedCoordinates">
          <l-tooltip>
            Nombre: {{location.name}}
            <br>
            Dirección: {{location.address}}
            <br>
            Teléfono: {{location.telephone}}
            <br>
            Email: {{location.email}}
            <br>
            Estado: Habilitado
            </l-tooltip>
        </l-marker>

         <l-marker  v-else :lat-lng="location.mappedCoordinates">
          <l-tooltip>
            Nombre: {{location.name}}
            <br>
            Estado: Deshabilitado</l-tooltip>
        </l-marker>
      </div>
    </l-map>
  </div>
<br>
  <!-- Tablas -->
  <div class="row justify-content-around">
    
    <!-- Recorridos de evacuación -->
    <div class="col-4">
      <h5>Recorridos de evacuacion🚦</h5>
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Nombre</th>
            <th scope="col">Descripción</th>
            <th scope="col">Estado</th>
          </tr>
        </thead>
        <tbody  v-for="(route, index) in routes" :key="`routes-${index}`">
          <tr>
            <th scope="row">{{route.name}}</th>
            <td>{{route.description}}</td>
            <td v-if="route.status== 'True'">✔️</td>
            <td v-else>❌</td>
            <!-- <td>
              <a class="btn btn-sm btn-warning" style="text-decoration:none;">
                <router-link :to="`/route/${route.id}`">
                  👁️
                </router-link>
              </a>
            </td> -->
          </tr>
        </tbody>
      </table>
      <div class="align-pagination">
        <button class="btn btn-sm btn-info" v-if="this.actual_page==1" disabled>Anterior</button>
        <button class="btn btn-sm btn-info" v-else @click="this.getData(previous_page)">Anterior</button><h6>Pagina {{actual_page}} de {{total_pages}}</h6>
        <button class="btn btn-sm btn-info" v-if="this.actual_page==this.total_pages" disabled>Siguiente</button>
        <button class="btn btn-sm btn-info" v-else @click="this.getData(next_page)">Siguiente</button>
      </div>

    </div>
    
    <!-- Puntos de encuentro-->
    <div class="col-4">
      <h5>Puntos de encuentro📍</h5>
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Nombre</th>
            <th scope="col">Teléfono</th>
            <th scope="col">Email</th>
            <th scope="col">Estado</th>
          </tr>
        </thead>
        <tbody  v-for="(location, index) in locations" :key="`locations-${index}`">
          <tr>
            <th scope="row">{{location.name}}</th>
            <td>{{location.telephone}}</td>
            <td>{{location.email}}</td>
            <td v-if="location.status== '1'">✔️</td>
            <td v-else>❌</td>
            <!-- <td>
              <a class="btn btn-sm btn-warning" style="text-decoration:none;">
                <router-link :to="`/locations/${location.id}`">
                  👁️
                </router-link>
              </a>
            </td> -->
          </tr>
        </tbody>
      </table>
      <div class="align-pagination">
        <button class="btn btn-sm btn-info" v-if="this.actual_pagePE==1" disabled>Anterior</button>
        <button class="btn btn-sm btn-info" v-else @click="this.getDataPE(previous_pagePE)">Anterior</button><h6>Pagina {{actual_pagePE}} de {{total_pagesPE}}</h6>
        <button class="btn btn-sm btn-info" v-if="this.actual_pagePE==this.total_pagesPE" disabled>Siguiente</button>
        <button class="btn btn-sm btn-info" v-else @click="this.getDataPE(next_pagePE)">Siguiente</button>
      </div>
    </div>
  </div>

<br>

<div>
    <router-link to="/" class="btn btn-info">Volver al inicio</router-link>
</div>
</template>

<script>
  import {LMap, LTileLayer, LMarker, LPolyline, LTooltip} from "@vue-leaflet/vue-leaflet";

  export default {
    components: {
      LMap,
      LTileLayer,
      LMarker,
      LPolyline,
      LTooltip
    },
    data () {
      return {
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        zoom: 10,
        center: [-34.92149, -57.954597],
        routes: [],
        locations: [],
        actual_page: 1,
        per_page: 2,
        total_elements: 0,
        actual_elements: 0,
        total_pages: 0,
        
        actual_pagePE: 1,
        per_pagePE: 2,
        total_elementsPE: 0,
        actual_elementsPE: 0,
        total_pagesPE: 0,
      };
    },
    created() {
      fetch(`${process.env.VUE_APP_API}/api/routes/?page=${this.actual_page}&per_page=${this.per_page}`).then((response) => {
        return response.json();
      }).then((json) => {
        this.routes=json.recorridos.map((route) =>
        ({
          ...route,
          coordinates:
          JSON.parse(route.coordinates),
        }))
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
  // loctions-puntos de encuentro
      fetch(`${process.env.VUE_APP_API}/api/locations/?page=${this.actual_pagePE}&per_page=${this.per_pagePE}`).then((responsePE) => {
            return responsePE.json();
          }).then((jsonPE) => {
            this.locations=jsonPE.locations.map((loc) =>
            ({
              ...loc,
              mappedCoordinates:
              loc.coordinates.split(','),
            }))

            this.total_elementsPE=parseInt(jsonPE.total)
            this.total_pagesPE=Math.ceil(this.total_elementsPE/this.per_pagePE)

            if (this.total_pagesPE > this.actual_pagePE){
              this.next_pagePE=parseInt(jsonPE.pagina) + 1
            }
            
            if (this.actual_pagePE > 1){
              this.previous_pagePE=parseInt(jsonPE.pagina) - 1
            }
            
            this.actual_elementsPE = 0

            for (let index = 1; index < this.total_pagesPE-this.actual_pagePE; index++) {
              this.actual_elementsPE = this.actual_elementsPE+this.per_pagePE
            }
            this.actual_elementsPE=this.actual_elementsPE + parseInt(jsonPE.inundables.length)
          }).catch((e) => {
            console.log(e)
          })

    },
    methods: {
      getData(page){
        fetch(`${process.env.VUE_APP_API}/api/routes/?page=${page}&per_page=${this.per_page}`).then((response) => {
          return response.json();
        }).then((json) => {
          this.routes=json.recorridos.map((route) =>
          ({
            ...route,
            coordinates:
            JSON.parse(route.coordinates),
          }))      

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
      getDataPE(page){
        fetch(`${process.env.VUE_APP_API}/api/locations/?page=${page}&per_page=${this.per_page}`).then((responsePE) => {
          return responsePE.json();
        }).then((jsonPE) => {
            this.locations=jsonPE.locations.map((loc) =>
            ({
              ...loc,
              mappedCoordinates:
              loc.coordinates.split(','),
            }))

          this.actual_pagePE=parseInt(jsonPE.pagina)
          if (this.total_pagesPE > this.actual_pagePE){
            this.next_pagePE=parseInt(jsonPE.pagina) + 1
          }
          
          if (this.actual_pagePE > 1){
            this.previous_pagePE=parseInt(jsonPE.pagina) - 1
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
