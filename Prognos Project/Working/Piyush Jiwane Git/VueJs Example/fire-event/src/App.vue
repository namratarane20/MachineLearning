<template>
  <student @updateParentVariable="updateValueFun($event)" :message="msg"></student>
</template>

<script>
export default {
 
  data () {
    return {
    msg : "Hello"
    }
  },
  methods:{
    updateValueFun:function(updated){
      this.msg=updated
    }
  }
}
</script>

<style>

</style>

