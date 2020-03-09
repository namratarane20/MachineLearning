<template>
    <button @click="changeColor()" v-bind:class="{redClass:isActive}">click here</button>
</template>

<script>
export default {
 
  data () {
    return {
      isActive:false,
    }
  },
  methods:{
    changeColor(){
      this.isActive=true
    }
  }
}
</script>

<style>
.redClass{
  background:red;
  color: white 
}
button{
  background:blue;
  color: white 
}
</style>
