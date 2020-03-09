 <template>
 <div>
     <h1>Events Example</h1>
     <button v-on:click="add"> add</button>
     
     <button @click="sub"> sub</button>
      <button v-on:click="dbadd(10)"> add double</button>
       <button v-on:click="dbsub(10)"> sub double</button>
       <button @click="say('hello welcome to alert box')"> Say </button>
      
     <p>age is now {{ age }}</p>
    
    
     <div class=" canvas" v-on:mousemove="updateXY">
         {{x}}, {{y}}
     </div>
 </div>
    
</template>

<script>
export default {
    data(){
        return{
        age:25,
        x:0,
        y:0,
       
        }
    },
    methods:{
        add(){
            return this.age++;
        },
        sub(){
            return this.age--;
        },
        dbadd(inc){
            return this.age+=inc;
        },
        dbsub(dec){
            return this.age-=dec;
        },
        updateXY(event){

          this.x = event.offsetX;
          this.y = event.offsetY;
        },
        say(message){
            return alert(message)
        }
        
    }
    
}
</script>
<style scoped>
.canvas{
    width: 600px;
    height:2px;
    padding: 200px 20px;
    text-align: center;
    border: 2px solid black;
    margin: 0 auto;

}
.styelclass{
    height: 100px;
    width: 100px;
}

</style>