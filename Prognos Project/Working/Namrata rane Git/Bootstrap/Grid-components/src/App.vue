<template>
  <div id="app">
    <!-- <Portal/> -->
    <!-- <GridComponents/> -->
    <!-- <MediaObject/> -->
    <!-- <Cards/> -->
    <!-- <ProgressBar/> -->
      <!-- <Login/> -->
      <!-- <Login2/> -->
      <PortLog/>
        <!-- <marquee behavior="" direction=""> <img alt="Vue logo" src="./assets/prognos.png" style="width:100px;height:100px;"></marquee> -->
  </div>
</template>

<script>
import PortLog from'./components/PortLog.vue'
// import Portal from './components/Portal.vue'
// import ProgressBar from './components/ProgressBar.vue'
// import MediaObject from './components/MediaObject.vue'
// import Cards from './components/Cards.vue'
// import GridComponents from './components/GridComponents.vue'
// import HelloWorld from './components/HelloWorld.vue'
//  import Login from './components/Login.vue'
// import Login2 from './components/Login2.vue'
export default {
  name: 'app',
  components: {
    // Login,
    // Login2,
    // GridComponents,
    // MediaObject,
    // Cards,
    // ProgressBar,
      //  Portal,
       PortLog,

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
    body{
    background-image: url('https://www.prognos.ai/wp-content/themes/prognos/images/video-placeholder-prognos.jpg');
    }

</style>
