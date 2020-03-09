<template>
    <div>
        <hr style="border:none; border-bottom: 3px solid red;">
          <h1>Print array element</h1>
          <ul>
              <li v-for="stud in students">{{ stud}}</li>
              <li>{{  addedUser}}</li>
          </ul>
         Add name: <input type="text" placeholder=" enter name to add user" v-model="newUser">
        Remove name:  <input type="text" placeholder=" enter name to remover" v-model="removeUser">
          <button @click="removeUser">Remove </button><br/> <br/>
          <button @click="addUser">Add user</button>
    </div>
</template>
<script>
export default {
    data(){
        return{
          newUser:"",
          students:["Namrata"," Nikita","Latiket","Piyush"]
        }
    },
    methods:{
         addUser(){
          this.addedUser=this.students.push(this.userremovename);
          this.newUser=" ";
         }
    }
}
</script>
<style scoped>


</style>