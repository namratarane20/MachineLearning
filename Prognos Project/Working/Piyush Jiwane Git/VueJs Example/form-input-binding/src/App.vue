<template>
  <div style="margin-left:10em">
    <div>
        <h3>Employee Form</h3>
      </div>
      <div>
        <input type="text" placeholder="Enter Name" v-model.lazy="name"><br>
        <input type="Email" placeholder="Enter Email" v-model.lazy="email"><br>
        <input type="text" placeholder="Enter Designation" v-model.lazy="desi"><br>
      </div>
      <br>
      <div>
        <button @click="sendDetails()">Submit</button>
      </div>
      <br><br>
      <h3><div>Employee Details Preview</div><br></h3>
      <div>Employee Name : {{ name }}</div><br>
      <div>Employee Email : {{ email }}</div><br>
      <div>Employee Designation : {{ desi }}</div><br>

  </div>
</template>

<script>
export default {
  data () {
    return {
     name:"",
     email:"",
     desi:""
    }
  }
}
</script>

<style>

</style>
