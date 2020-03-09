<template>
  <div>
      <form>
           <h3>Employee form </h3>
           <p>
              <label> Name:</label>
              <input type="text"   v-model="emp.name" placeholder="Enter name">
           </p>
           <p>
              <label>Desigantion:</label>
              <input type="text"  v-model="emp.desi" placeholder="Enter designation">
           </p>
           <p>
                <label> Mo No.</label>
              <input type="text"  v-model="emp.mono" placeholder="Enter contact">
           </p>
           <p>
               <button>Submit</button>
           </p>

      </form>
  </div>
</template>

<script>

export default {
    data(){
        return{
            emp{
                name:" ",
                desi:" " ,
                mono:" ",
            }
        }
    }
 
}
</script>

<style>

</style>
