<template>
    <div>
          <hr/>
        <h1>Event Handling with click and double click </h1>
        <h3> (mouseover , mousemove, mouseout)</h3>
        <p> counter :={{ counter }}</p>
        <button @click="increament">increament By 1</button>
        <button @click="decreament">Decreaments by 1</button>
        <button @click="decBy(10)">Decrement by 10 imes</button>
        <button @click="incBy(10)">Increament by 10 times</button>
        <button>Mouseover</button><br/><br/>
        <button @mouseover="mouseOver">mouseover with mouseover function</button>
        <span>
    Hover me to change the background!
  </span>
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
       increament(){
           this.counter++;
       },
       decreament(){
           this.counter--;
       },
       incBy(num1){
           this.counter +=num1;
       },
       decBy(num2){
            this.counter -=num2;
       },
       mouseOver(){
        //  console.error("this is mouseover");
       }
       



    }
    
}
</script>
<style  scoped>
span:hover {
  background: green;
}
button:hover{
    background: red;
}

</style>

