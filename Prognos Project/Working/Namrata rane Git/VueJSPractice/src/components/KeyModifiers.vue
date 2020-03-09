<template>
    <div>
        <hr style="border:none; border-bottom: 3px solid red;">
          <h1>Key Modifiers</h1>
          <h3>( enter ,alt,ctrl,keyCode,delete,space)</h3>
          <input type="text" @keypress.enter="keyPressFunction" placeholder="any key press"><br/><br/>
          <input type="text" @keyup.alt.enter="keyUpFunction" placeholder="press alt + enter">
          <input type="text" @keyup.delete="keyUpDeleteFunction" placeholder="press backspace"><br/><br/>
          <input type="text" @keyup.ctrl.enter="keyUpCtrlEnter" placeholder="press ctrl + enter"><br/><br/>
          <input type="text" @keyup.space="keyUpSpace" placeholder="press spacebar">
          <input type="text" @keyup.65="keyUpKeyCode" placeholder="ascii code">
    

    </div>
</template>
<script>
export default {
    data(){
        return{

        }
    },
    methods:{
        keyPressFunction(){
            console.log("  Enter key Pressed")
        },
        keyUpFunction(){
            console.log(" alt+enter key pressed")
        },
        keyUpDeleteFunction(){
            console.log("backspace pressed")
        },
        keyUpCtrlEnter(){
            console.log("ctrl + enter pressed")
        },
        keyUpSpace(){
            console.log("spaceBar pressed")
        },
        keyUpKeyCode(){
            console.log("code is...")
        }
    }
}
</script>
<style scoped>

</style>