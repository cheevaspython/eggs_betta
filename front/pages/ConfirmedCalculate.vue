<template>
  <transition name="fade">
    <confirmedCalculate v-show="currentConfCalc" />
  </transition>
</template>
  
<script>
export default {
  name: 'ConfirmedCalculateCard',
  components: {
    confirmedCalculate: () => import("@/components/tasks/confirmedCalculate")
  },
  data() {
    return {
      showConfCalc: false
    }
  },
  computed: {
    currentConfCalc() {
      return this.$store.state.eggs.currentConfCalculate
    }
  },
  created() {
    if (!this.currentConfCalc) {
      this.$router.push('/')
    }
  }
}
</script>

<style lang="scss" scoped>
.fade-enter-active {
  transition: all .4s ease;
}
.fade-leave-active {
  transition: all .4s ease;
}
.fade-enter, .fade-leave-to {
  transform: translateX(50px);
  opacity: 0;
}
</style>
