<template>
  <div>
    <student1></student1>
    <employee></employee>
  </div>
</template>

<script>
import Employee from './Employee.vue'
export default {
  components:{
    "employee":Employee
  },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<style>
</style>
