<template>
  <div >

    <keep-alive>
      <component :is="comp"></component>
    </keep-alive>
    

    <button @click="comp = 'std'">student form</button>
    <button @click="comp = 'emp'">employee form</button>
  </div>
</template>

<script>

import Employee from './components/Employee.vue'
import Student from './components/Student.vue'

export default {
  data() {
    return {
      comp : "std"
    }
  },
  components: {
    "emp" : Employee,
    "std" : Student
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
