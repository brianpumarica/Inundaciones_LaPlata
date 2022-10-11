<template>
<!-- Titulo -->

    <h2 id="titleCustom">Realizar denuncia</h2>

<!-- Mapa -->

<div>
  <l-map style="height: 300px" :zoom="zoom" :center="center" @click="setlatlng">
    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
    <l-marker :lat-lng="markerLatLng"></l-marker>
  </l-map>
</div>

<br>

<!-- Formulario -->
  <form>
    <!-- titulo -->

  <div class="mb-3">
    <label for="title" class="form-label">Título</label>
    <input type="text" class="form-control" placeholder="Titulo de la denuncia" v-model="title"/>
  </div>

    <!-- Descripcion -->

  <div class="mb-3">
    <label for="description" class="form-label">Descripción</label>
    <input type="text" class="form-control" placeholder="Descipcion de la denuncia" v-model="description"/>
  </div>

    <!-- Categoría -->

  <div class="mb-3">
    <label for="category" class="form-label">Categoría</label>
    <select v-model="category" class="form-select" aria-label=".form-select-lg example">
      <option value="-1">Seleccione</option>
      <option v-for="category in categorys" v-bind:key="category" v-bind:value="category.id">{{category.description}}</option>
    </select>
  </div>

  <!-- Apellido -->

  <div class="mb-3">
    <label for="surname_user" class="form-label">Apellido</label>
    <input type="text" class="form-control" placeholder="Apellido del denunciante" v-model="surname_user"/>
  </div>

  <!-- Nombre -->
  
  <div class="mb-3">
    <label for="name_user" class="form-label">Nombre</label>
    <input type="text" class="form-control" placeholder="Nombre del denunciante" v-model="name_user"/>
  </div>
  
  <!-- Teléfono -->

  <div class="mb-3">
    <label for="telephone" class="form-label">Teléfono</label>
    <input type="tel" class="form-control" placeholder="Telefono del denunciante" v-model="telephone"/>
  </div>
  
  <!-- Email -->

  <div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input type="email" class="form-control" placeholder="Email del denunciante" v-model="email"/>
  </div>

  <!-- Guardar -->
  
  <button class="btn btn-primary" @click="sendform">Guardar</button>
  &nbsp;
    <router-link to="/" class="btn btn-info">Volver al inicio</router-link>

</form>

</template>

<script>
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 10,
      center: [-34.91, -57.95],
      markerLatLng: [],
      title:"",
      description:"",
      category:"-1",
      surname_user:"",
      name_user:"",
      telephone:"",
      email:"",
      coordinates:"",
      dict:[],

      categorys: [
        {
          id:0,
          description: 'Alcantarillas tapadas'
        },
        {
          id:1,
          description: 'Basurales'
        },
        {
          id:2,
          description: 'Otros'
        }
      ]
    };
  },
  methods:{
    setlatlng(e){
      if (e.latlng){
        this.markerLatLng = e.latlng;
      }
    },
      post_api() {
      const requestOptions = { 
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.dict),
      };
      
      alert(requestOptions.body["coordinates"])
      fetch(`${process.env.api}/api/complaints/`, requestOptions)
        .then((response) => response.json())
        .catch((err) => console.log('hubo un problema', err))
    },
    sendform() {
      if(this.category == -1)
      {
        alert('Debe seleccionar una categoria')
      }
      else
      {
        this.dict["title"] = this.title;
        this.dict["description"] = this.description; 
        this.dict["category"] = this.category; 
        this.dict["surname_user"] = this.surname_user; 
        this.dict["name_user"] = this.name_user;
        this.dict["telephone"] = this.telephone; 
        this.dict["email"] = this.email; 
        this.dict["coordinates"] = this.markerLatLng; 
        this.post_api();
      }
    }
  }
}
</script>
