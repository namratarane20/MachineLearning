<template>
  <div>
    <student>
      <div slot="form-heading">
        <h3>Student Form</h3>
      </div>
      <div slot="form-body">
        <input type="text" placeholder="Enter Name"><br>
        <input type="Email" placeholder="Enter Email"><br>
        <input type="text" placeholder="Enter Designation"><br>
      </div>
      <div slot="form-button">
        <button @click="sendDetails()">Submit</button>
      </div>
    </student>
  </div>
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
