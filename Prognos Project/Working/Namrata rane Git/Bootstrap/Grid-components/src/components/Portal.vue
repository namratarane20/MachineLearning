<template>
    <div class="container">
       <div class="row">
           <div class="card">
             <div class="col-xl-10">
               <div class="table-responsive">
                  <table class="table table-bordered">
                         <thead>
                            <tr>
                              <th>Empoyee ID</th>
                              <th>Employee Name</th>
                              <th>Email Id</th>
                              <th>Profession</th>
                              <th>Salray</th>
                            </tr>
                         </thead>
                        <tbody>
                           <tr v-for="row in users">
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
        
    </div>

</template>
<script>
export default {
    data(){
        return{
             users: [
          { id: "TC111", name: "namrata", phone: 'namrata@progons.com', profession: 'IT Manager' ,sal:'10000'},
          { id: "TC222", name: "nikita", phone: 'nikita@prognos.com', profession: 'Paleontologist',sal:'10000' },
          { id: "TC333", name: "piyush", phone: 'piyush@prognos.com', profession: 'Project Lead',sal:'10000'},
          { id: "TC444", name: "latiket", phone: 'latiket@prognos.com', profession: 'Head Chef',sal:'10000' },
           { id: "TC555", name: "shreya", phone: 'shreya@prognos.com', profession: 'Actor',sal:'10000' },
           { id: "TC666", name: "roshu", phone: 'roshani@prognos.com', profession: 'Masseuse',sal:'10000' },
           { id: "TC777", name: "namrata", phone: 'namrata@progons.com', profession: 'IT Manager',sal:'10000' },
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
    
}
</script>
<style scoped>

</style>