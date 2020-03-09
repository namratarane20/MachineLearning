<template>
     <div>
       
          <h2>This our content part</h2>
          <header>
              <div class="divClass">
                   <span class="more">
                  <img src="../assets/java.png"  id="image"/>&nbsp&nbsp &nbsp&nbsp  &nbsp&nbsp
                  <img src="../assets/scala.png" id="image"/>&nbsp&nbsp &nbsp&nbsp &nbsp&nbsp
                  <img src="../assets/vueimg.png"  id="image"/>&nbsp&nbsp &nbsp&nbsp  &nbsp&nbsp
                  <img src="../assets/angular.png" id="image"/>&nbsp&nbsp &nbsp&nbsp  &nbsp&nbsp
                  <img src="../assets/python.png"  id="image"/>
                   </span>
              </div><br/>
              <hr>
              
          </header>

     </div>
</template>
<script>
export default {
    
}
</script>
<style scoped>
.divClass{
    background-color:lightpink;
    width: 100%;
    height: 400px;
}

    
.more {
    
    left: 0px;
    top: 80px;
    position:relative;
}

#image{
    width:200px;
    height:200px;
}

#image:hover{
    width:300px;
    height:300px;
}

</style>