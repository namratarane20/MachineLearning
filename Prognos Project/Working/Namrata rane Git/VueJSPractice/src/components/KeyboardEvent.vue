<template>
    <div>
        <hr style="border:none; border-bottom: 3px solid red;">
        <h1>Keyboard event</h1>
        <h3>( keyup, keypress,keydown )</h3>
        <input type="text" @keypress="keypressFunction" placeholder="key pressed"><br/><br/> 
        <input type="text" @keyup="keyupFunction"><br/><br/> 
        <input type="text" @keydown="keuDownFunction">

        <!-- <p v-on="keyupFunction">{{ msg }}</p> -->
    </div>
    
</template>
<script>
export default {
    data(){
        return{
          msg:"keyPress"
        }
    },
    methods:{
        keypressFunction(){
          console.log("key pressed")
        },
        keyupFunction(){
            console.log("keyUp")
        },
        keuDownFunction(){
            console.log("keyDown")
        }

    }
}
</script>
<style scoped>



</style>