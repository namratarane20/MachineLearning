<template>
     <div>
          <hr style="border:none; border-bottom: 3px solid red;">
          
          <h1>Computed property Example</h1>
          <p> {{ name()}}</p><br/>
          <input type="text" placeholder="Enter first name" v-model="fname"><br/><br/>
          <input type="text" placeholder="Enter last name " v-model="lname"><br/>
          <h2>Full Name: {{ fullname }}</h2><br>

         <input type="text" placeholder="enter meter here" v-model="meter"><br/>
         <h2>Meter in centimer: {{converToCM }}</h2><br/>
         <div>
         
          
         
           Physics:<input type="text" v-model="physics"> 
           Chemistry:<input type="text" v-model="chem">
           Math:<input type="text" v-model="math"><br/>
           <h2>Toatl marks are:== {{ totalMarks }}</h2>
         </div>
     </div>
    
</template>
<script>
export default {
    data(){
        return{
            fname:" ",
            lname:" ",
            meter:" ",
            physics:0,
            chem:0,
            math:0,
        }
    },
    methods:{
        name(){
            return "I am from method property"
        }
    },
    computed:{
       fullname(){
           return this.fname + " " +this.lname;
       },
       converToCM(){
           return this.meter * 100;
       },
       totalMarks(){
         return parseInt(this.physics)+parseInt(this.chem)+parseInt(this.math);
       }
    }

    
}
</script>
<style scoped>

</style>