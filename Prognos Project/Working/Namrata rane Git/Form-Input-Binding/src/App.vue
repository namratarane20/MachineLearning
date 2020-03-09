<template>
  <div id="app">
  <emp/>
  <EmployeeDetails/>
  </div>
</template>

<script>
 import EmployeeDetails from './components/EmployeeDetails.vue'
 export default {
  name: 'app',
  components: {
   EmployeeDetails,
      
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
