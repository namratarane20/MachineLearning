<template>
     <div>
        
         <h1>Nested Compinents</h1>
         <hr>
          <h2>This our header part</h2>
          <header>
              <div class="divClass">
                   <span class="more">
                  <a href="">Home</a>&nbsp&nbsp &nbsp&nbsp &nbsp&nbsp &nbsp&nbsp &nbsp&nbsp &nbsp&nbsp &nbsp&nbsp &nbsp&nbsp
                   <a href="">About us</a>&nbsp&nbsp &nbsp&nbsp &nbsp&nbsp &nbsp&nbsp &nbsp&nbsp &nbsp&nbsp &nbsp&nbsp
                    <a href="">Contact us</a>&nbsp&nbsp &nbsp&nbsp &nbsp&nbsp &nbsp&nbsp &nbsp&nbsp &nbsp&nbsp 
                     <a href="">Carrier</a>
                   </span>
              </div><br/>
              <hr>
              
          </header>
 <Content/>
     </div>
</template>
<script>
export default {
    
}
</script>
<style scoped>
.divClass{
    background-color: aquamarine;
    width: 100%;
    height: 50px;
}

    
.more {
    
    left: 0px;
    top: 20px;
    position:relative;
}


</style>