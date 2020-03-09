<template>
  <div id="app">
     <!-- this for dynamic components -->
     <keep-alive>
    <component v-bind:is="component"></component>
     </keep-alive>
    <button @click="component='student' ">Submit student details</button> &nbsp &nbsp
    <button @click="component='emp' ">submit Employee details</button>
    <!-- <student/>
    <emp/> -->
  </div>
</template>

<script>
import Student from './components/Student.vue'
import Employee from './components/Employee.vue'

export default {
  data(){
    return{
      component:"student"
    }
  },
  components: {
   "student":Student,
   "emp":Employee,
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
