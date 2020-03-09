<template>
  <div>
    <div>
      <h3>Employee Form</h3>
    </div>
    <div>
      <input type="text" placeholder="Enter Name" v-model.lazy="name" />
      <br />
      <input type="Email" placeholder="Enter Email" v-model.lazy="email" />
      <br />
      <input type="text" placeholder="Enter Designation" v-model.lazy="desi" />
      <br />
    </div>
    <br />
    <div>
      <button @click="sendDetails()">Submit</button><br><br>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  }
};
</script>

<style>
</style>
