<template>
  <div>
  <h1>{{ message }}</h1> 
  <button v-on:click="updateMsg">update from child</button>


  </div>
</template>

<script>
export default {
    props:["message"],
    data(){
     return{

     }
 },
 methods:{
    updateMsg(){
     this.$emit("updateParentVariable", "value has been updated from parent")
    }
  }
  
}
</script>

<style>

</style>
