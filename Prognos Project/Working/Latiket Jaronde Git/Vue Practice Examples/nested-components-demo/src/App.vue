<template>
  <div>
    <header1 :authorname="name"></header1>

    <content1 :myplaylist="playlist" :studentlist="students"></content1>

    <footer1></footer1>

    <br />
    <hr >
    <br />

    <refrnc :studentlist="students"></refrnc>

    <br><hr><br>
    <primtp :authorname="name"></primtp>

    <br><hr><br>
    <fireevent :message="msg" @updateMsg="updateMsgFn($event)" ></fireevent>

  </div>
</template>

<script>
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";
import Content from "./components/Content.vue";
import ReferenceType from "./components/ReferenceType.vue";
import PrimitiveType from "./components/PrimitiveType.vue";
import FireEventFromChildToParent from "./components/FireEventFromChildToParent.vue";

export default {
  name: "app",
  components: {
    header1: Header,
    footer1: Footer,
    content1: Content,
    refrnc: ReferenceType,
    primtp : PrimitiveType,
    fireevent : FireEventFromChildToParent
  },
  data() {
    return {
      msg : "this is msg from parent APP.vue",
      name: "Anonymous",
      playlist: [
        {
          link1: "https://www.youtube.com/watch?v=bOTAZV_Gwq8",
          name1: "A Curious New Smartphone Gadget..."
        },
        {
          link1: "https://www.youtube.com/watch?v=ORaO5PBCt74",
          name1: "apple  watch series"
        },
        {
          link1: "https://www.youtube.com/watch?v=8RmvFk2mp2g",
          name1: "unboxing one+ 7T"
        }
      ],
      students : ["lebron","dwayne","kobe","chrish","stephen"]
    }
  },
  methods : {
    updateMsgFn : function(updatedMsg) {
      this.msg = updatedMsg
    }
  }
}
</script>

<style>
</style>
