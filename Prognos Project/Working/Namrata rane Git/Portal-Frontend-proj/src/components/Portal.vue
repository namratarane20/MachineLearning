<template>
    <div class="container-fluid">
        <Header/>
        <br><br><br>
      <div class="jumbotron">
       <div class="row">
          
             <!-- ========================================= div class for nav bar with serach box=================================================== -->
          
                <div class=" offset-xl-2 col-xl-8 " id="reduce">
                  <div class="form-group">
                    <input type="text" class="form-control shadow p-3 mb-5 bg-white rounded" placeholder="Search">
                 </div>
              <!-- ========================================= div class for check boxes  =================================================== -->
      
                 <div class="col-xl-12 marginclass">
                             
                      <span>
                         <label class="form-check-label"> 
                            <input type="checkbox" class="checkbox-primary"> &nbsp &nbsp Questionnaire
                         </label> &nbsp  &nbsp &nbsp
                         <label class="form-check-label">
                            <input type="checkbox" class="checkbox-primary" value=""> &nbsp &nbsp Policy
                         </label>
                      </span> 
            </div>
        </div>
           
           
         
       <!-- =========================== div  fro button ================ -->
       <div class="offset-xl-4 col-xl-4">
           <br>
             <button type="button" class="btn btn-primary btn-md" id="shadow" @click="show">
                 Search 
             </button>
             

       </div>
       <!-- =============================== div  for table ================= -->
       </div> 
       <br>
        <div class="row">
            <div class="col-xl-12">
               <div class="table-responsive" >
                   <table class="table table-bordered tableClass" v-if="showTable">
                         <thead>
                            <tr>
                              <th>Empoyee ID</th>
                              <th>Employee Name</th>
                              <th>Email Id</th>
                              <th>Profession</th>
                              <th>Salary</th>
                            </tr>
                         </thead>
                        <tbody>
                           <tr v-for="row in users" :key="row">
                             <td>{{row.id}}</td>
                             <td>{{row.name}}</td>
                             <td>{{row.phone}}</td>
                             <td>{{row.profession}}</td>
                             <td>{{row.sal}}</td>
                           </tr>
                         </tbody>

                    </table>
                </div>
           </div>
       </div>
       
</div>
        <Footer/> 
  </div> 
 
<!-- </div> -->
</template>
<script>
export default {
    data(){
        return{
          showTable:false,
           users: [
          { id: "TC111", name: "namrata", phone: 'namrata@progons.com', profession: 'IT Manager', sal:10000},
          { id: "TC222", name: "nikita", phone: 'nikita@prognos.com', profession: 'Paleontologist', sal:10000 },
          { id: "TC333", name: "piyush", phone: 'piyush@prognos.com', profession: 'Project Lead', sal:10000 },
          { id: "TC444", name: "latiket", phone: 'latiket@prognos.com', profession: 'Head Chef', sal:10000 },
           { id: "TC555", name: "shreya", phone: 'shreya@prognos.com', profession: 'Actor', sal:10000 },
           { id: "TC666", name: "roshu", phone: 'roshani@prognos.com', profession: 'Masseuse', sal:10000 },
           { id: "TC777", name: "namrata", phone: 'namrata@progons.com', profession: 'IT Manager', sal:10000 },
           //{ id: "TC888", name: "nikita", phone: 'nikita@prognos.com', profession: 'Paleontologist' },
          // { id: "TC999", name: "piyush", phone: 'piyush@prognos.com', profession: 'Project Lead' },
          // { id: "TC000", name: "latiket", phone: 'latiket@prognos.com', profession: 'Head Chef' },
          // { id: "TC500", name: "shreya", phone: 'shreya@prognos.com', profession: 'Actor' },
          // { id: "TC888", name: "nikita", phone: 'nikita@prognos.com', profession: 'Paleontologist' },
          // { id: "TC999", name: "piyush", phone: 'piyush@prognos.com', profession: 'Project Lead' },
          // { id: "TC000", name: "latiket", phone: 'latiket@prognos.com', profession: 'Head Chef' },
          // { id: "TC500", name: "shreya", phone: 'shreya@prognos.com', profession: 'Actor' }
        ]
        };
    },
    methods:{
        show(){
           this.showTable=true;
        }
    }
    
}
</script>
<style scoped>
/* input[type=text] {
  width: 130px;
  -webkit-transition: width 0.4s ease-in-out;
  transition: width 0.4s ease-in-out;
} */
input[type=text]:focus {
  width: 100%;
}
table.table-bordered{
    border:2px solid black;
    margin-top:20px;
  }
table.table-bordered > thead > tr > th{
    border:1px solid black;
}
table.table-bordered > tbody > tr > td{
    border:1px solid black;
}
form-control{
    border-block: 5px solid black
}
hr.hrclass{
   
  border: 1px solid #508beb;
}




</style>

                 <!-- <nav class="navbar navbar-dark bg-dark">
                   <div class="form-group has-search">
                      <input type="text" class="form-control" placeholder="Search">
                   </div>
                </nav>  -->



                  <!-- <div class="col-xl-12">
                       
                <span>
                   <label class="form-check-label">
                      <input type="checkbox" class="checkbox-primary" value="">Questionary
                   </label> &nbsp  &nbsp &nbsp
                   <label class="form-check-label">
                      <input type="checkbox" class="checkbox-primary" value="">Questionary
                   </label>
                </span> 
           </div> -->
       