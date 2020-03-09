<template>
  <div style="margin-left:10em">
    <div>
        <h3>Employee Form</h3>
      </div>
      <div>
        <input type="text" placeholder="Enter Name" v-model.lazy="employee.name"><br>
        <input type="Email" placeholder="Enter Email" v-model.lazy="employee.email"><br>
       
      </div>
      <div>
        <p>
          <input type="checkbox" v-model="employee.desi" value="Developer"/>Developer
          <input type="checkbox" v-model="employee.desi" value="Designer"/>Designer
          <input type="checkbox" v-model="employee.desi" value="UI/UX"/>UI/UX
          <input type="checkbox" v-model="employee.desi" value="Trainee"/>Trainee
        </p>
      </div>
      <div>
        <p>
          <input type="radio" value="Male" v-model="employee.gender">M
          <input type="radio" value="Female" v-model="employee.gender">F
        </p>
      </div>
      <div>
        <select v-model="employee.lvl">
          <option v-for="r in employee.role">{{r}}</option>
        </select>
      </div>
      <br>
      <div>
        <button @click="sendDetails()">Submit</button>
      </div>
      <br><br>
      <h3><div>Employee Details Preview</div><br></h3>
      <div>Employee Name : {{ employee.name }}</div><br>
      <div>Employee Email : {{ employee.email }}</div><br>
      <div>
        Designation: <ul v-for="dd in employee.desi">
          <li> {{ dd }} </li>
        </ul>
      </div><br>
      <div>Gender : {{employee.gender}}</div><br>
      <div>Disignation Level : {{employee.lvl}}</div>
      

  </div>
</template>

<script>
export default {
  data () {
    return {
     employee:{
       name:"",
       email:"",
       desi:[],
       gender:"",
       role:["Senior","Junior","Sales"],
       lvl:""
     }
    }
  }
}
</script>

<style>

</style>
