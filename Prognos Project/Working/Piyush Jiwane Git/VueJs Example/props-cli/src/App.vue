<template>
  <Child name="Piyush Jiwane" v-bind:myPlayList="playList" channel-name="owt"></Child>
</template>

<script>
import Child from "./Child.vue"
export default {
 components:{
   Child
 },
  data () {
    return {
     playList:["Piyush","Gaurav","Jiwane"]
    }
  }
}
</script>

<style>

</style>
