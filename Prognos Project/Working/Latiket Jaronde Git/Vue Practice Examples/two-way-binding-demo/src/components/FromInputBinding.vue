<template>
  <div>
    <h1>Form input binding example (lazy modifier)</h1>

    <form>
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

      <p>
        <button>submit</button>
      </p>
    </form>

    <div style="text-align:left; margin-left:20%">
        <h2>Details : </h2>
      <p>
          Name :  {{ name }}
        </p>
      <p>MailID :  {{ mail }}</p>
      <p>Mobile no: : {{ mobileNo }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: "",
      mail: "",
      mobileNo: 0
    };
  }
};
</script>

<style scoped>
form {
  text-align: left;
  margin-left: 20%;
}
</style>