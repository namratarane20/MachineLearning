<template>
<div>
    {{ message }} <br>
    <button @click="updateMsg">Updated in Child</button>
</div>
</template>

<script>
export default {
props:["message"],
  data () {
    return {
     
    }
  },
  methods:{
      updateMsg:function(){
          this.$emit("updateParentVariable","Updated final Value")
      }
  }
}
</script>

<style>

</style>
