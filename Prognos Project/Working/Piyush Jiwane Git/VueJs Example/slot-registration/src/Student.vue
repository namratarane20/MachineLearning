<template>
  <div>
      <form>
          <div id="form-header">
              <slot name="form-heading"></slot>
              <slot name="form-body"></slot><br>
              <slot name="form-button"></slot><br>
          </div>
      </form>
  </div>
</template>

<script>
export default {
 
  data () {
    return {
      
    }
  }
}
</script>

<style>

</style>
