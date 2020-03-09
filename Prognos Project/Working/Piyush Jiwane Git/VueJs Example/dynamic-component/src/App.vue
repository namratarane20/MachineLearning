<template>
  <div>
    <keep-alive>
      <component v-bind:is="comp"></component>
    </keep-alive>
    <button @click="comp='student'">Student Form</button>
    <button @click="comp='employee'">Employee Form</button>
  </div>
</template>

<script>
import Student from "./Student.vue"
import Employee from "./Employee.vue"
export default {
  components:{
    "student":Student,
    "employee":Employee
  },
  data () {
    return {
      comp:"student"
    }
  }
}
</script>

<style>

</style>
