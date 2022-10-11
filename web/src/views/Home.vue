<template>
  <h1 id="titleCustom">Bienvenido al sitio!</h1>
  <p>
    En esta página, brindaremos toda clase de información relevante acerca de inundaciones en la Plata.
    Proveemos recursos de valor, tales como, ver recorridos de evacuación, zonas inundables y puntos de encuentro, que ayudan a prevenir y controlar tales desastres por medio de la información, acción y comunicación. 
    Además, la página contiene números telefónicos de distintas jefaturas relevantes, y la opción de generar una queja o denuncia informativa.
  </p>
  <a class="btn btn-success" data-bs-toggle="offcanvas" href="#offcanvasExample" role="button" aria-controls="offcanvasExample">
    Ver servicios ofrecidos
  </a>
  <br>
  <br>
  <center><img src="https://images.adsttc.com/media/images/58e1/32b5/e58e/ceae/b200/052b/large_jpg/Centro_Hist%C3%B3rico_La_Plata.jpg?1491153580" alt="centered image" height="598"> </center>
  
</template>

<script>

export default {
  name: 'Home',
  components: {
    
  },
  created(){
    window.scrollTo(0, 0)
  }
}
</script>
