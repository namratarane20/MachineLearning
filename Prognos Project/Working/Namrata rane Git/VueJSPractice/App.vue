<template>
  <div id="app">
   

     <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
     <Event/>
     <Binding/>


  </div>
</template>

<script>
import Binding from './components/Binding.vue'
import Event from './components/Event.vue'
// import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'app',
  components: {
    //  HelloWorld,
      Event,
      Binding
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
</style>
