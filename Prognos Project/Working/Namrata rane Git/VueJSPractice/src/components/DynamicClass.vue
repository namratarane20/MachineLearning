<template>
    <div>
        <hr style="border:none; border-bottom: 3px solid red;">
          <h1>Add dynamic classes to css</h1>
         <button v-bind:class="{redClass:isActive}" @click="toggleClass"> CLICK HERE</button><br/><br/>
         <!-- <button v-bind:class="{redClass:isActive}" @click="isActive= !isActive"> CLICK HERE</button> -->
    </div>
</template>
<script>
export default {
    data(){
        return{
         isActive:false,
        }
    },
    methods:{
       toggleClass(){
           this.isActive =!this.isActive
       }
    }
}
</script>
<style scoped>
button.redClass{
    background: red;
    border-radius: 20px;
    border: solid maroon;
    height: 40px;
    color:yellow;
    

}
button{
    background: green;
    border: darkgreen;
    height: 40px;
    color:white;
}


</style>