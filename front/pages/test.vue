<template>
<b-button @click="testClick">test</b-button>
</template>

<script>
export default {
  name: "test",
  methods:{
    testClick(){
      console.log('####### this.$auth ', this.$auth)
    }
  }
}
</script>

<style scoped>

</style>
