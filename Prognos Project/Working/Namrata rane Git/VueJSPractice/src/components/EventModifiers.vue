<template>
   <div> 
        <GlobalComponent/>
      <hr style="border:none; border-bottom: 3px solid red;">

       <h1>Event modifiers </h1>
       <h3>(once , prevent, stop ,capture)</h3>
        <button @click.once="pressOnce"> click me once</button><br/>
        <!-- <button @click="preventFunction"> Click for prevent</button> -->
       
        <p>counter:=> {{counter}}</p><br/>
         <a href="https://www.google.com" @click.prevent> go to Google</a><br/>
         <form action="#" method="post" @submit.prevent><br/>
             <button type="submit" >Submit</button>
         </form><br/>
         <div id="parent-Div" @click="parentDivFunction">
             <button id="child-div" @click.stop="parentDivFunction"> Click Here</button>
         </div>
         <br/>
         <div class="parent-class" @click.capture="parentClass">
             <button @click="btnClick">Click me Again</button>
         </div>
   </div>
    
</template>
<script>
export default {
    data(){
        return{
            counter:0,
            }

    },
    methods:{
        pressOnce(){
            this.counter+=1;
        },
        preventFunction(){

        },
        parentDivFunction(){
            console.log("clicked")
        },
        parentClass(){
            console.log("parent class")
        },
        btnClick(){
            console.log("child button")
        }
    }
    
}
</script>
<style scoped>
button{
    height: 30px;
   
    border-radius: 50px;
    animation-delay: 10s;
}

</style>