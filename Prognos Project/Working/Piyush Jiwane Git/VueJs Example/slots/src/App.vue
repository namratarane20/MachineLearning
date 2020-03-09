<template>
  <student>
      <h4 slot="header">This is heading tag</h4>
      <p slot="para">This is a simple paragraph </p>
  </student>
</template>

<script>
import Student from "./Student.vue"
export default {
 components:{
   "student":Student
 },
  data () {
    return {
      
    }
  }
}
</script>

<style>

</style>
