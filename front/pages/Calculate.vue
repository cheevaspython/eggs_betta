<template>
  <calculate />
</template>

<script>
export default {
  name: 'CalculatePage',
  components: {
    calculate: () => import("@/components/tasks/calculate")
  },
  data() {
    return {

    }
  },
  methods: {
    
  },
  computed: {
    currentCalc() {
      return this.$store.state.eggs.currentCalculate
    }
  },
  created() {
    if (!this.currentCalc) {
      this.$router.push('/')
    }
  }
}
</script>
