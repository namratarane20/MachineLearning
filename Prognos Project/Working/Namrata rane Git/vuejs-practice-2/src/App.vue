<template>
  <div id="app">
    <Header/>
    <!-- <Content/> -->
    <Footer/>
  </div>
</template>

<script>
import Footer from './components/Footer.vue'
import Header from './components/Header.vue'
// import Content from './components/Content.vue'
export default {
  name: 'app',
  components: {
    Header,
   
    Footer
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
