<template>
  <div id="app">
   
   <!-- <Portal/> -->
   <PortalLogin/>
   
  </div>
</template>

<script>
import PortalLogin from './components/PoralLogin.vue'
// import Login1 from './components/Login1.vue'
// import Header from './components/Header.vue'
// import HelloWorld from './components/HelloWorld.vue'
// import Portal from './components/Portal.vue'

export default {
  name: 'app',
  components: {
    // HelloWorld,
    //  Portal,
   
    // Login1,
    // Header,
     PortalLogin,
    
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
 /* body {
 background-image: url("https://www.prognos.ai/wp-content/themes/prognos/images/video-placeholder-prognos.jpg");
  background-color: #cccccc; 
  
 } */
/* html, body{
    background-color:black;
} */
 /* body{
  background-image: url("https://www.prognos.ai/wp-content/themes/prognos/images/video-placeholder-prognos.jpg"); 

}*/
</style>
