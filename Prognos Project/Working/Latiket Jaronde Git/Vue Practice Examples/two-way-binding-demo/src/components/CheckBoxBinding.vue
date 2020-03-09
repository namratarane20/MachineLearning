<template>
    <div>
        <h1>Checkbox binding example (lazy modifier)</h1>

    <form style="text-align:left; margin-left:20%">
        <h2>Input form</h2>
      <p>
        <label>Name :</label>
        <input type="text" placeholder="full name" v-model.lazy="name" />
      </p>

      <p>
        <label>Email :</label>
        <input type="text" placeholder="email" v-model.lazy="mail" />
      </p>

      <p>
        <label>Mobile No. :</label>
        <input type="nnumber" placeholder="mobile number" v-model.lazy="mobileNo" />
      </p>

        <!-- checkbox binding -->
        <h4 >Select designation</h4>
        <p >
            Developer : <input type="checkbox" value="developer" name="developer" v-model="posts"> 
            Tester : <input type="checkbox" value="tester" name="developer" v-model="posts"> 
            Data engineer : <input type="checkbox" value="data engineer" name="developer" v-model="posts"> 
            Data scientist : <input type="checkbox" value="data scientist" name="developer" v-model="posts">
        </p>

        <!-- radio button binding -->
        <h4 >Select Gender</h4>
        <p >
            Male : <input type="radio" value="Male" v-model="gender"> 
            Female : <input type="radio" value="Female" v-model="gender">
            Other : <input type="radio" value="Other" v-model="gender"> 
        </p>

        <!-- select box (dropdown) binding -->
        <h4>select level : 
            <select v-model="level">
                <option v-for="level in levels" :key="level"> {{ level }} </option>
            </select>
        </h4>
    </form>

    <div style="text-align:left; margin-left:20%">
        <h2>Details : </h2>
      <p>
          Name :  {{ name }}
        </p>
      <p>MailID :  {{ mail }}</p>
      <p>Mobile no: : {{ mobileNo }}</p>
      
      <!-- checkbox binding -->
      <p>Posts : 
          <ul>
              <li v-for="post in posts" :key="post">
                  {{ post }}
              </li>
          </ul>
      </p>

    <!-- radio button binding -->
      <p> Gender : {{ gender }} </p>

       <!--select box binding  -->
      <p> Level : {{ level }} </p>
    </div>


    </div>
</template>

<script>
export default {
    data() {
        return {
            posts : [],
            name: "",
            mail: "",
            mobileNo: '',
            gender : '',
            levels : ["senior","junior","team leader"], 
            level : ""
        }
    }
}
</script>

<style scoped>
form {
    text-align: left;
    margin-left: 20%;
}
</style>