<template>
  <div><h3>
      {{ employeeStatement }}
     </h3> 
     <ul>
         <li v-for="emp in employeeList">
             {{ emp }}
         </li>
     </ul>
     </div>  
</template>
<script>
export default {
    data(){
        return{
             employeeStatement:"This is our simple employee message",
             employeeList:["employee1","employee2","employee3","employee4"]
        }
    }
}
</script>
<style scoped>

</style>