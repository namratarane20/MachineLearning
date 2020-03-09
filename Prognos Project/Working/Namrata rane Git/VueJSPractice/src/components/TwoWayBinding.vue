<template>
 <div>
<hr style="border:none; border-bottom: 3px solid red;">
    <h1>Two way data binding</h1>
    <h3>( v-model directive)</h3>
     <div>
         <input type="text" v-model=" char">
        
        <h2> {{ char }} </h2><br/>
        <form class=" ">
             <input type="text" placeholder="Enter Name" v-model="name">  <br/>
             <h2> {{name}}</h2>
             <input type="text" placeholder="Enter email" v-model="email"><br/>
             <h2>{{email}}</h2>
        </form>
     </div>
 </div>
    
</template>
<script>
export default {
    data(){
        return{
            char:" " ,
            name:"",
            email:"",
        }
    },
    methods:{
        keyPressed(event){
            this.char = event.key;
        }
    }
    
}
</script>
<style scoped>

</style>