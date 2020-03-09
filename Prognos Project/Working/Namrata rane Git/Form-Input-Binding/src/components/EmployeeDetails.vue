<template>
  <div>
      <form>
           <h3>Employee form </h3>
           <p>
              <label> Name:</label>
              <input type="text"   v-model.lazy="emp.name" placeholder="Enter name">
           </p>
           <p>
              <label>Desigantion:</label>
              <input type="text"  v-model.lazy="emp.desi" placeholder="Enter designation">
           </p>
           <p>
                <label> Mo No.</label>
              <input type="text"  v-model.lazy="emp.mono" placeholder="Enter contact">
           </p>
           <p>
               <button>Submit</button>
           </p>
           <label> <input type="checkbox" v-model="emp.posts" value="Developer"/> Developer </label>
           <label> <input type="checkbox" v-model="emp.posts" value="Programmer"/> Programmer </label>
           <label> <input type="checkbox" v-model="emp.posts" value="Manager"/> Manager </label>
           <label> <input type="checkbox" v-model="emp.posts" value="CEO"/> CEO </label>
          <p>
              <label>Select Gender</label>
              <label> <input type="radio" value="Male" v-model="emp.gender"/>Male</label>
              <label> <input type="radio" value="Female" v-model="emp.gender"/>Female</label>
              <label> <input type="radio" value="Others" v-model="emp.gender"/>Others</label>

          </p>
          <p>
              <select v-model="emp.level">
                  <option v-for=" lavel in levels">{{lavel}}</option>
              </select>
          </p>
      </form>
      <div id="emppreview">
          <h2>submited employee details</h2>
          <p>Name: {{ emp.name}}</p>
          <p>Desigantion:{{ emp.desi}}</p>
          <p>Mo No:{{ emp.mono}}</p>
          <p>Employee post: 
              <ul>
                  <li v-for="p in emp.posts">
                      {{p}}
                  </li>
              </ul>
          </p>
          <p>Employee Gender:{{ emp.gender}}</p>
          <p>Employee lavel is:{{emp.level}}</p>

      </div>
  </div>
</template>

<script>

export default {
     data(){
         return{
             emp:{
                 name:" ",
                 desi:" ",
                 mono:" ",
                 posts:[],
                 gender:" ",
                 level:"",
             },
             levels:[ "Senior","Junior","Team Leader","Motivators"]
         }
     }
 
}
</script>

<style>

</style>
