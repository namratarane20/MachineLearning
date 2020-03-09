<template>
  <div >
    <student v-bind:message="msg" v-on:updateParentVariable="upadateValueFun($event)"></student>
  </div>
</template>

<script>
import Student from './components/Student.vue'
export default {
  name: 'app',
  components: {
   "student":Student,
  },
  data(){
    return{
      msg:'passing data from parent to child compenents'
    }
  },
  methods:{
     upadateValueFun(){
       this.msg="upadted value"
     }
  }
  
}
</script>

<style>

</style>
