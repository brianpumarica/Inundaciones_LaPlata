<template>
<body id="body">
  <!-- Barra superior de navegación -->
  <nav class="navbar navbar-expand-lg navbar-dark" id="customBar">
    <div class="container-fluid">
      <a class="navbar-toggler navbar-brand" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
      </a>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <!-- Desplegable lateral (Menú de opciones) -->
            <li class="nav-item">
              <a class="btn btn-success" data-bs-toggle="offcanvas" href="#offcanvasExample" role="button" aria-controls="offcanvasExample">
                <span class="navbar-toggler-icon"></span>
              </a>
            </li>
        </ul>
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <router-link to="/" class="navbar-brand"><h2>Centro de prevención de inundaciones</h2></router-link>
        </ul>

      </div>
    </div>
  </nav>
  <!-- Desplegable -->
  <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasExample" aria-labelledby="offcanvasExampleLabel">
    <!-- Encabezado -->
    <div class="offcanvas-header">
      <h5 class="offcanvas-title" id="offcanvasExampleLabel">Servicios</h5>
      <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <hr>
    <!-- Body -->
    <div class="offcanvas-body">
      <!-- Denuncias -->
      <div>
        Ver las denuncias realizadas y denunciar sobre alcantarillas tapadas, basurales e irregularidades.
      </div>
      <div class="dropdown mt-3">
        <button class="btn btn-success dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
          Denuncias
        </button>
        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
          <li><router-link to="/denuncias" class="nav-link">Realizar denuncia</router-link></li>
          <li><router-link to="/getdenuncias" class="nav-link">Ver denuncias</router-link></li>
        </ul>
      </div>

      <br>
      <hr>

      <!-- Zonas inundables -->
      <div>
        Ver las zonas inundables registradas en la ciudad y la zona
      </div>
      <div class="mt-3">
        <router-link to="/inundables" class="btn btn-success">Ver Zonas inundables</router-link>
      </div>

      <br>
      <hr>

      <!-- Puntos de encuentro -->
      <div>
        Ver los puntos de encuentro cercanos de acuerdo a su ubicación.
      </div>
      <div class="mt-3">
        <router-link to="/locations" class="btn btn-success">Ver puntos de encuentro</router-link>
      </div>
      
      <br>
      <hr>
      
      <!-- Recorridos de evacuacion -->
      <div>
        Ver los recorridos de evacuación cercanos de acuerdo a su ubicación
      </div>
      <div class="mt-3">
        <a href="/locations" class="btn btn-success">Ver recorridos de evacuación</a>
      </div>

      <!-- Cerrar -->
      <div class="position-absolute bottom-0 start-50 translate-middle-x pb-4">
        <button type="button" class="btn btn-danger" data-bs-dismiss="offcanvas" aria-label="Close">
          Cerrar
        </button>
      </div>

    </div>

  </div>
  <!-- Título -->
  <br>
  <!-- Template -->
  <div class="container" id="containerVue">  <router-view/></div>

  <br>
  <br>
  <br>
  <div id="footer">
    <!-- Footer -->
    <hr>
    <footer class="page-footer font-small indigo">
    
      <!-- Footer Links -->
      <div class="container text-center text-md-left">
    
        <!-- Grid row -->
        <div class="row">

          <!-- Grid column -->
          <div class="col-md-3 mx-auto">
    
            <!-- Links -->
            <h5 class="font-weight-bold text-uppercase mt-3 mb-4"><i class="fa fa-phones" aria-hidden="true"></i></h5> <!-- Para que aparezca el logo, sacar la s de phoneS -->
    
            <ul class="list-unstyled">
              <li>
                <button type="button" class="btn btn-outline-primary custom-button-footer"> 100 <br><small>Bomberos</small></button>
              </li>
              <hr>
              <li>
                <button type="button" class="btn btn-outline-primary custom-button-footer">130<br><small>Defensa civil</small></button>
              </li>
            </ul>
    
          </div>
          <!-- Grid column -->
    
          <hr class="clearfix w-100 d-md-none">
    
          <!-- Grid column -->
          <div class="col-md-3 mx-auto">
    
            <!-- Links -->
            <h5 class="font-weight-bold text-uppercase mt-3 mb-4"><i class="fa fa-phone" aria-hidden="true"></i></h5>
    
            <ul class="list-unstyled">
              <li>
                <button type="button" class="btn btn-outline-primary custom-button-footer"> 106 <br><small>Prefectura</small></button>
              </li>
              <hr>
              <li>
                <button type="button" class="btn btn-outline-primary custom-button-footer"> 107 <br><small>Ambulancia</small></button>
              </li>
            </ul>
    
          </div>
          <!-- Grid column -->
    
          <hr class="clearfix w-100 d-md-none">
    
          <!-- Grid column -->
          <div class="col-md-3 mx-auto">
    
            <!-- Links -->
            <h5 class="font-weight-bold text-uppercase mt-3 mb-4"><i class="fa fa-phones" aria-hidden="true"></i></h5> <!-- Para que aparezca el logo, sacar la s de phoneS -->
    
            <ul class="list-unstyled">
            <li>
                <a type="button" href="tel:107" class="btn btn-outline-primary custom-button-footer"> 107 <br><small>Atención al vecino</small></a>
            </li>
            <hr>
            <li>
                <button type="button" class="btn btn-outline-primary custom-button-footer"> 911 <br><small>Policía</small></button>
            </li>
            </ul>
    
          </div>
          <!-- Grid column -->
    
        </div>
        <!-- Grid row -->
    
      </div>
      <!-- Footer Links -->
    
      <!-- Copyright -->
      <div class="footer-copyright text-center py-3">© 2021 Grupo 29 - Proyecto de Software:
        <a href="https://gitlab.catedras.linti.unlp.edu.ar/proyecto2021/proyectos/grupo29/"> GitLab</a>
      </div>
      <!-- Copyright -->
    
    </footer>
    <!-- Footer -->
    </div>
  </body>
</template>

<style>
  @import './assets/styles/style.css';
</style>

<script>
export default {
  data: () => ({
    info: null,
  }),
  created() {
     fetch(`https://127.0.0.1:5000/api/configuration/`).then((response) => {
        return response.json();
      }).then((json) => {

        // Obtengo la paleta de colores de la aplicación privada
        var aux = json.color_public.split(",")

        // Asigno el color de fondo (priv)
        document.getElementById("body").style.setProperty('background-color', aux[0]);
        
        // Asigno el color de fuente (priv)
        document.getElementById("titleCustom").style.setProperty('color', aux[1])
        // Asigno el color de la barra de navegación (priv)
        document.getElementById("customBar").style.setProperty('background-color', aux[2]);

      }).catch((e) => {
        console.log(e)
      })
  }
};
  </script>