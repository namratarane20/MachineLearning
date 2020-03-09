<template>
  <div id="app">
   

     <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
     <Event/>
     <Binding/>
     <EventHandling/>
      <img alt="Vue logo" src="./assets/rose.jpeg" style="width:100px;height:100px;">
     <KeyboardEvent/>
     <EventModifiers/>
     <KeyModifiers/>
     <TwoWayBinding/>
     <ComputedProperty/>
     <DynamicClass/>
     <Referancing/>
   
     

  </div>
</template>

<script>
import Referancing from './components/Referancing.vue'
import DynamicClass from './components/DynamicClass.vue'
import ComputedProperty from './components/ComputedProperty.vue'
import TwoWayBinding from './components//TwoWayBinding.vue'
import KeyModifiers from './components/KeyModifiers.vue'
import EventModifiers from './components/EventModifiers.vue'
import KeyboardEvent from './components/KeyboardEvent.vue'
import EventHandling from './components/EventHandling.vue'
import Binding from './components/Binding.vue'
import Event from './components/Event.vue'
// import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'app',
  components: {
    //  HelloWorld,
      Event,
      Binding,
      EventHandling,
      KeyboardEvent,
      EventModifiers,
      KeyModifiers,
      TwoWayBinding,
      ComputedProperty,
      DynamicClass,
      Referancing,
     
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
